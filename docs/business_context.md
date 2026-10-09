# Business context

> Sections marked **General** describe standard supply-chain knowledge. Sections marked
> **Client-specific** state only what the project brief says; anything else is an open question.

## How products reach the consumer (General)

In the US alcohol market, the **three-tier system** generally applies: a supplier sells to
**distributors** (wholesalers), who sell to **retailers and restaurants**, who sell to consumers.
Two flows matter:

- **Shipments / sell-in:** supplier → distributor
- **Depletions / sell-out:** distributor → retailers and on-premise accounts

An out-of-stock can happen at each step: the distributor's warehouse has no stock when an order
arrives, or the retail shelf is empty. Which level the client measures is an open question.

## Why stockouts happen (General)

Inventory is a balance between **demand** (orders from customers) and **supply** (replenishment
orders that arrive after a lead time). A stockout occurs when demand during the lead time exceeds
available stock. Typical causes:

- Demand spike or forecast error
- Replenishment parameters out of date (buffer too small, ADU stale)
- Late or partial supplier delivery; lead time longer than assumed
- Order not placed, or constrained by MOQ / allocation
- Product-level issues (new item, vintage change, allocation-limited product)
- Data issues (wrong units, mismatched SKUs, missing records)

## DDMRP in one paragraph (General)

Instead of pushing stock based on a forecast alone, **Demand Driven MRP** keeps **inventory
buffers** at selected points. Each buffer has three zones (red, yellow, green) sized from
**average daily usage (ADU)** and **lead time**. Every day, the **net flow position**
(on-hand + on-order − qualified demand) is compared with the buffer: when it drops to the
**top of yellow (TOY)** or below, an order is suggested to bring it back to the **top of green (TOG)**.
OOS can therefore point to buffers that are sized wrong, ADU that does not reflect real demand,
lead times that are underestimated, or orders that are not executed. See `glossary.md`.

## Relationships we need to understand

```
forecast / ADU ──► buffer sizing (TOY, TOG) ──► suggested orders (SOQ, MOQ) ──► supply after lead time
                                                                                │
customer orders ──► fulfillment from on-hand stock ◄────────────────────────────┘
                     │
                     ├─ fully shipped  → fill rate OK
                     └─ not shipped    → pick omits / unfulfilled orders → OOS
```

## Client-specific facts (from the project brief)

- The client works with **several distributors**, each with its own inventory and
  order-management processes; datasets may be **heterogeneous**.
- The client operates in a **demand-driven / DDMRP** environment.
- Concepts used by the client include ADU, SOQ, TOY/TOG, MOQ, lead time, fill rate,
  pick omits, actual vs 9L-equivalent cases, SKU and vintage.
- **Anaplan** is part of the client's planning processes. How it is used is not yet known.
- Initial datasets have been received for Distributors A–D and Master Data.

Everything else (formulas, refresh frequency, OOS definition, who decides what) must be confirmed.
