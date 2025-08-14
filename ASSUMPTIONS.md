# Assumptions & Processing Rules

This document outlines the **normalization rules**, **deduplication heuristics**, and **tie-breaking logic** used in this project to ensure consistent, deterministic outputs.

---

## 1. Normalization Rules

1. **Order IDs**  
   - All order IDs are converted to **uppercase**.  
   - IDs are parsed to extract **letters + digits** (`ABC-123` format).  
   - Acceptable forms:  
     - Only letters (`ABC`)  
     - Only digits (`123`)  
     - Letters and digits (`ABC123`, `ABC-123`, `ABC 123`)  
   - Any extra characters at the start/end are ignored.

2. **Dates**  
   - Two formats are supported for parsing:  
     - `YYYY-MM-DD HH:MM`  
     - `YYYY/MM/DD HH:MM`  

3. **Zones / Cities**  
   - Normalized using the mapping provided in **`zones.csv`**.  
   - Matching is case-insensitive.  
   - If no mapping exists, the original value is preserved.

---

## 2. Deduplication Heuristic

When multiple orders share the same **normalized order ID**:

- If **all addresses match** → keep the earliest deadline order.  

---

## 3. Tie-Breakers (Courier Assignment)

When a courier is eligible to take multiple orders at the same time, orders are assigned based on:

1. **Earliest deadline** takes priority.
2. If same deadline → lowest **priority**
2. If priorities are identical → lowest assigned total weight (alphabetical/numeric sort).  
3. If still tied → lowest **courier ID** (alphabetical/numeric sort)


---

## 4. Determinism Guarantees

To ensure repeatable results:
- All **IDs**, **addresses**, and **zones** are normalized before processing.  
- Lists are **sorted alphabetically** before output.  
