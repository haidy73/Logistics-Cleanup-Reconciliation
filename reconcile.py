import csv
import datetime
import json
from cleanOrders import normalize_date, normalize_order_id


def read_couriers(file_name):
    couriers = []
    with open(file_name, "r") as couriers_file:
        couriers = json.load(couriers_file)

    return couriers

def read_logs(file_name):
    logs = []
    with open(file_name,  "r") as logs_file:
        reader = csv.DictReader(logs_file)

        for row in reader:
            logs.append({"orderId": normalize_order_id(row["orderId"]), "courierId": row["courierId"].title(), "deliveredAt": normalize_date(row["deliveredAt"])})
    
    return logs

def missing_orders(plan, logs):
    missing = []

    for order in plan["assignments"]:
        
        # Missing
        order_missing = True
        for log in logs:
            if order["orderId"] == log["orderId"]:
                order_missing = False
                break
            
        if order_missing:
            missing.append(order["orderId"])
    
    return missing

def unexpected_orders(cleaned_orders, logs):
    orders = []
    unexpected = []

    for order in cleaned_orders:
        orders.append(order["orderId"])
    
    for log in logs:
        if log["orderId"] not in orders:
            unexpected.append(log["orderId"])
            logs.remove(log)

    return unexpected

def duplicate_logs(logs):
    unique = []
    duplicate = []

    for log in logs:
        if log["orderId"] in unique: 
            duplicate.append(log["orderId"])
        else: 
            unique.append(log["orderId"])

    return duplicate

def misassigned_orders(plan, logs):
    misassigned = []
    for order in plan["assignments"]:
        for log in logs:
            if order["orderId"] == log["orderId"]:
                if order["courierId"] != log["courierId"]:
                    misassigned.append(order["orderId"])

    return misassigned

def overloaded_couriers(cleaned_orders, couriers, logs):
    log_courier_capacity = {}
    order_weight = {}
    courier_capacity = {}
    overloaded_couriers = []

    for order in cleaned_orders:
        order_weight[order["orderId"]] = order["weight"]

    for courier in couriers:
        courier_capacity[courier["courierId"]] = courier["dailyCapacity"]


    for log in logs:
        if not log_courier_capacity.get(log["courierId"]):
            log_courier_capacity[log["courierId"]] = 0

        log_courier_capacity[log["courierId"]] += order_weight[log["orderId"]]
        if log_courier_capacity[log["courierId"]] > courier_capacity[log["courierId"]]:
            overloaded_couriers.append(log["courierId"])
            
    return overloaded_couriers

def late_orders(cleaned_orders, logs, unexpected):
    
    orders_deadline = {}
    late = []

    for order in cleaned_orders:
        orders_deadline[order["orderId"]] = order["deadline"]

    for log in logs:
        
        if log["orderId"] not in unexpected and log["deliveredAt"] > orders_deadline[log["orderId"]]:
            late.append(log["orderId"])
    
    return late

def reconcile_plan_log(cleaned_orders, couriers, plan, logs):

    missing = missing_orders(plan, logs)
    unexpected = unexpected_orders(cleaned_orders, logs)
    duplicate = duplicate_logs(logs)
    late = late_orders(cleaned_orders, logs, unexpected)
    misassigned = misassigned_orders(plan, logs)
    overloaded_couriers_list = overloaded_couriers(cleaned_orders, couriers, logs)

    reconciliation = {"missing": missing, "unexpected": unexpected, "duplicate": duplicate, "late": late, "misassigned": misassigned, "overloadedCouriers": overloaded_couriers_list}
    
    return reconciliation

def write_reconciliation(reconcile):
    with open("reconciliation.json", "w") as reconcile_file:
        json.dump(reconcile, reconcile_file, indent=4)