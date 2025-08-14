# AI_NOTES.md

This file documents how GPT was used while building the **Delivery Orders Cleaner & Planner**, the prompts that guided the process, key adjustments I made, and one notable correction.

---

# AI_NOTES.md

## 1) Prompt: Normalizing Messy Order Data
**What I asked:**  
"I want you to walk me through, step-by-step, how you would normalize messy order data into a clean, standardized format before actually implementing it — I’ll supervise and give corrections if needed."

**What GPT did:**  
Outlined a general plan including trimming, case formatting, whitespace cleanup, and using `re.fullmatch` for pattern detection.

**What I changed:**  
I provided my own **regex logic** for detecting and formatting certain fields (payment type, IDs) and replaced GPT’s `re.fullmatch` usage with `re.search` so patterns could be matched even if they appeared within a longer string.

---

## 2) Prompt: Planning Courier Assignments Under Constraints
**What I asked:**  
"Before writing any code, explain how you would plan courier assignments so that each courier has a reasonable workload, respects delivery deadlines, and stays within maximum order limits"

**What GPT did:**  
Suggested an initial approach where orders were distributed evenly among couriers

**What I changed:**  
I reworked the logic to account for **both deadlines and courier capacity**, sorting orders by urgency and assigning them based on who could realistically fulfill them on time. This made the plan more realistic and avoided unassignable orders.


