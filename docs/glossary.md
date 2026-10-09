# Glossary

Plain-language definitions. **General definitions are standard; how the client calculates each
metric must be confirmed** (see `open_questions.md`).

| Term | Meaning |
|---|---|
| **OOS (Out-of-Stock)** | A product is not available when someone wants it. It can be measured at different levels: distributor warehouse (zero on-hand), order line (ordered but not shipped) or retail shelf. *Client definition to confirm.* |
| **SKU** | Stock Keeping Unit: one specific sellable item (product + size + pack). |
| **Vintage** | Harvest year of a wine or champagne. The same product can exist in several vintages, which may or may not share a SKU code. *To confirm.* |
| **Distributor** | Wholesaler that buys from the supplier and sells to retailers and restaurants (US three-tier system). |
| **Shipments / Depletions** | Shipments: supplier → distributor (sell-in). Depletions: distributor → retail/on-premise (sell-out). |
| **On-hand** | Physical stock in the warehouse. |
| **On-order** | Stock ordered but not yet received. |
| **Lead time** | Time between placing a replenishment order and receiving it. |
| **MOQ (Minimum Order Quantity)** | Smallest quantity that can be ordered. It can force larger orders than needed. |
| **Forecast** | Expected future demand. |
| **ADU (Average Daily Usage)** | Average quantity consumed per day over a chosen window (past, future or blended). The base input for sizing DDMRP buffers. *Window and formula to confirm.* |
| **DDMRP** | Demand Driven Material Requirements Planning. Inventory is managed with buffers at chosen points, and orders are triggered by actual demand rather than forecasts alone. |
| **Inventory buffer** | Target stock range for an item, split into three zones: red (safety), yellow (covers demand during lead time), green (order size). |
| **TOR / TOY / TOG** | Top of Red / Top of Yellow / Top of Green. Cumulative buffer thresholds: TOY = red + yellow, TOG = TOY + green. |
| **Net flow position** | On-hand + on-order − qualified demand (past-due, due today, unusual spikes). Compared with the buffer each day. |
| **SOQ (Suggested Order Quantity)** | In standard DDMRP, when net flow ≤ TOY, SOQ = TOG − net flow, often rounded to MOQ or pack multiples. *Client formula to confirm.* |
| **Fill rate** | Share of demand shipped on time and in full. It can be counted by cases, order lines or orders, and the results differ. *Definition to confirm.* |
| **Pick omits** | Order lines or cases that could not be picked in the warehouse at fulfillment time, usually because stock was missing. A practical OOS signal at distributor level. *Definition to confirm.* |
| **Actual cases** | Physical cases, whatever their size (e.g. 6 × 750 mL or 12 × 375 mL). |
| **9L equivalent cases** | Standard industry volume unit: one 9L case = 9 liters = 12 × 750 mL bottles. Makes products of different sizes comparable. 9L cases = (bottles × bottle size in mL) / 9,000. |
| **S&OP** | Sales & Operations Planning: the regular process that balances demand and supply plans. |
| **Anaplan** | A commercial cloud planning software. It is part of the client's planning processes; its exact role is to confirm. |
