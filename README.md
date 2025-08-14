# Delivery Orders Cleaner & Planner

This project processes messy delivery order data, normalizes it, assigns couriers under specific constraints, and reconciles actual deliveries against the planned schedule.  
It ensures **deterministic output** — the same inputs will always produce the same outputs — by applying consistent sorting, formatting, and mapping rules.

---

## 📖 Features

- **Data Cleaning:**  
  - Normalizes date formats.  
  - Converts order IDs to uppercase.  
  - Trims extra spaces from addresses.  
  - Maps zones and cities using `zones.csv`.

- **Courier Assignment:**  
  - Assigns couriers based on availability and constraints.  
  - Ensures optimal load distribution.

- **Reconciliation:**  
  - Compares planned deliveries with actual logs.  
  - Outputs warnings for mismatches or inconsistencies.

- **Determinism:**  
  - Sorted IDs/lists in output files.  
  - Fixed normalization rules for consistent results.

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/haidy73/Logistics-Cleanup-Reconciliation.git
cd REPO_Folder

# 3. Run the script
python main.py