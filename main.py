import cleanOrders
import planOrders
import reconcile


def main():
    input_orders = cleanOrders.read_orders("orders.json")
    cleaned_orders, warnings = cleanOrders.clean_orders(input_orders)
    cleanOrders.write_cleaned_orders(cleaned_orders, warnings)

    couriers = reconcile.read_couriers("couriers.json")
    plan = planOrders.plan_order_couriers(cleaned_orders, couriers)
    planOrders.write_plan(plan)

    logs = reconcile.read_logs("logs.csv")
    reconciliation = reconcile.reconcile_plan_log(cleaned_orders, couriers, plan, logs)
    reconcile.write_reconciliation(reconciliation)

if __name__ == "__main__":
    main()