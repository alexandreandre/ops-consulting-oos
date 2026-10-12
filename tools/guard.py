#!/usr/bin/env python3
"""Confidentiality guard for this repository (see DATA_POLICY.md).

Blocks client data files, notebook outputs and real client names from entering Git.
It runs automatically through the Git hooks in .githooks/ and the GitHub check.
Standard library only, so it works with any Python >= 3.8.

Usage:
  python3 tools/guard.py staged             check staged changes (pre-commit hook)
  python3 tools/guard.py message FILE       check a commit message (commit-msg hook)
  python3 tools/guard.py branch NAME        check a branch name (pre-push hook)
  python3 tools/guard.py range BASE HEAD    check commits between two revisions (pre-push, CI)
  python3 tools/guard.py all                check every tracked file
  python3 tools/guard.py update-terms       rebuild the blocked-name list from private/KEY.md

Real names are never stored in the repository: tools/blocked_terms.sha256 only holds
SHA-256 hashes of the normalized names listed in private/KEY.md.
"""
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import PurePosixPath

TERMS_FILE = "tools/blocked_terms.sha256"
KEY_FILE = "private/KEY.md"
BEGIN_TERMS = "<!-- BEGIN BLOCKED TERMS -->"
END_TERMS = "<!-- END BLOCKED TERMS -->"
MAX_BYTES = 1_000_000
MAX_WORDS = 4
ZERO_SHA = "0" * 40

BLOCKED_EXTENSIONS = {
    # data
    ".csv", ".tsv", ".xlsx", ".xlsm", ".xls", ".xlsb", ".parquet", ".feather", ".pkl",
    ".pickle", ".h5", ".db", ".sqlite", ".json", ".zip", ".7z", ".gz",
    # documents
    ".pdf", ".pptx", ".ppt", ".docx", ".doc", ".pages", ".key", ".numbers",
    # images and media (charts or recordings can reveal client data)
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".html", ".mp3", ".mp4", ".m4a", ".wav",
}
ALLOWED_PATHS = {".claude/settings.json"}


def git(*args):
    return subprocess.run(
        ["git", "-c", "core.quotePath=false", *args], capture_output=True, check=True
    ).stdout


def normalize(text):
    """Lowercase, strip accents, turn punctuation into spaces, split into words."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).split()


def digest(words):
    return hashlib.sha256(" ".join(words).encode()).hexdigest()


def load_terms():
    try:
        with open(TERMS_FILE, encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip() and not line.startswith("#")}
    except FileNotFoundError:
        return set()


def contains_name(text, terms):
    words = normalize(text)
    for n in range(1, MAX_WORDS + 1):
        for i in range(len(words) - n + 1):
            if digest(words[i:i + n]) in terms:
                return True
    return False


def path_problem(path):
    p = PurePosixPath(path)
    if path in ALLOWED_PATHS:
        return None
    if p.parts[0] == "data" and p.name not in ("README.md", ".gitkeep"):
        return "file inside data/ (client data never goes to Git)"
    if p.parts[0] == "private" and path != "private/README.md":
        return "file inside private/ (local only)"
    if p.suffix.lower() in BLOCKED_EXTENSIONS:
        return f"blocked file type ({p.suffix})"
    return None


def notebook_problem(content):
    try:
        notebook = json.loads(content)
    except ValueError:
        return "notebook could not be read"
    if any(cell.get("outputs") for cell in notebook.get("cells", [])):
        return "notebook still contains outputs (they can contain client data)"
    return None


def added_lines(diff):
    """Yield (path, line number, text) for every added line of a unified diff."""
    path, lineno = None, 0
    for line in diff.decode("utf-8", "replace").splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("@@"):
            match = re.search(r"\+(\d+)", line)
            lineno = int(match.group(1)) if match else 0
        elif line.startswith("+") and path:
            yield path, lineno, line[1:]
            lineno += 1


def check_files(paths, read, size, terms):
    problems = []
    for path in paths:
        problem = path_problem(path)
        if problem is None and size(path) > MAX_BYTES:
            problem = f"file larger than {MAX_BYTES // 1_000_000} MB"
        if problem is None and path.endswith(".ipynb"):
            problem = notebook_problem(read(path))
        if problem is None and contains_name(path, terms):
            problem = "file path contains a real client name"
        if problem:
            problems.append(f"{path}: {problem}")
    return problems


def check_diff(diff, terms):
    return [
        f"{path}:{lineno}: contains a real client name, use the codes instead"
        for path, lineno, text in added_lines(diff)
        if contains_name(text, terms)
    ]


def check_staged(terms):
    paths = [p for p in git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z")
             .decode().split("\0") if p]
    problems = check_files(
        paths,
        read=lambda p: git("show", f":{p}"),
        size=lambda p: int(git("cat-file", "-s", f":{p}")),
        terms=terms,
    )
    return problems + check_diff(git("diff", "--cached", "-U0", "--no-color", "--no-ext-diff"), terms)


def check_range(base, head, terms):
    if base == ZERO_SHA or not base:
        return check_all(terms, rev=head)
    paths = [p for p in git("diff", "--name-only", "--diff-filter=ACMR", "-z", f"{base}...{head}")
             .decode().split("\0") if p]
    problems = check_files(
        paths,
        read=lambda p: git("show", f"{head}:{p}"),
        size=lambda p: int(git("cat-file", "-s", f"{head}:{p}")),
        terms=terms,
    )
    problems += check_diff(git("diff", "-U0", "--no-color", "--no-ext-diff", f"{base}...{head}"), terms)
    messages = git("log", "--format=%H%x00%B%x01", f"{base}..{head}").decode("utf-8", "replace")
    for entry in messages.split("\x01"):
        sha, _, body = entry.strip().partition("\x00")
        if sha and contains_name(body, terms):
            problems.append(f"commit {sha[:8]}: message contains a real client name")
    return problems


def check_all(terms, rev=None):
    if rev:
        paths = [p for p in git("ls-tree", "-r", "--name-only", "-z", rev).decode().split("\0") if p]
        read = lambda p: git("show", f"{rev}:{p}")
    else:
        paths = [p for p in git("ls-files", "-z").decode().split("\0") if p]
        read = lambda p: open(p, "rb").read()
    problems = check_files(paths, read=read, size=lambda p: len(read(p)), terms=terms)
    for path in paths:
        if path_problem(path) is None and path != TERMS_FILE:
            for lineno, text in enumerate(read(path).decode("utf-8", "replace").splitlines(), 1):
                if contains_name(text, terms):
                    problems.append(f"{path}:{lineno}: contains a real client name, use the codes instead")
    return problems


def update_terms():
    try:
        content = open(KEY_FILE, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"{KEY_FILE} not found: copy it from the team's Drive folder first.")
        return 1
    if BEGIN_TERMS not in content or END_TERMS not in content:
        print(f"{KEY_FILE} has no blocked-terms section ({BEGIN_TERMS} … {END_TERMS}).")
        return 1
    block = content.split(BEGIN_TERMS, 1)[1].split(END_TERMS, 1)[0]
    terms = [re.sub(r"^[-*]\s*", "", line.strip()) for line in block.splitlines()]
    words = [normalize(term) for term in terms if term.strip()]
    too_long = [" ".join(w) for w in words if len(w) > MAX_WORDS]
    if too_long:
        print(f"Terms longer than {MAX_WORDS} words are not supported: shorten them.")
        return 1
    hashes = sorted({digest(w) for w in words if w})
    with open(TERMS_FILE, "w", encoding="utf-8") as f:
        f.write("# SHA-256 of blocked names, normalized (lowercase, no accents, punctuation as spaces).\n")
        f.write("# Generated by `python3 tools/guard.py update-terms` from private/KEY.md. Do not edit.\n")
        f.writelines(h + "\n" for h in hashes)
    print(f"{len(hashes)} blocked terms written to {TERMS_FILE}.")
    return 0


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv else 2
    mode, args = argv[0], argv[1:]
    if mode == "update-terms":
        return update_terms()

    terms = load_terms()
    problems = [] if terms else [f"{TERMS_FILE} is missing or empty, so names cannot be checked"]
    if mode == "staged":
        problems += check_staged(terms)
    elif mode == "message":
        text = "\n".join(l for l in open(args[0], encoding="utf-8").read().splitlines()
                         if not l.startswith("#"))
        if contains_name(text, terms):
            problems.append("commit message contains a real client name")
    elif mode == "branch":
        if contains_name(args[0], terms):
            problems.append(f"branch name '{args[0]}' contains a real client name")
    elif mode == "range":
        problems += check_range(args[0], args[1], terms)
    elif mode == "all":
        problems += check_all(terms)
    else:
        print(__doc__)
        return 2

    if not problems:
        print("Confidentiality guard: OK")
        return 0
    print("\n✗ Blocked by the confidentiality guard (see DATA_POLICY.md):", file=sys.stderr)
    for problem in problems:
        print(f"  - {problem}", file=sys.stderr)
    print(
        "\nHow to fix: unstage data files (git restore --staged <file>), replace real names by\n"
        "the codes (Distributor A–D, the client), clear notebook outputs, shorten the message.\n"
        "Never bypass this check with --no-verify.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except subprocess.CalledProcessError as error:
        print(f"✗ Confidentiality guard could not run git: {error.stderr.decode(errors='replace').strip()}",
              file=sys.stderr)
        sys.exit(1)
