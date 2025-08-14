import json

def matching_couriers(order, couriers, couriers_capacity):
    matching_couriers = []

    for courier in couriers:
        ok_courier = True

        if order["city"] not in courier["zonesCovered"] and (order["city"] not in zone for zone in courier["zonesCovered"]):
            ok_courier = False
        elif order["paymentType"] == "COD" and not courier["acceptsCOD"]:
            ok_courier = False
        elif order["weight"] > couriers_capacity[courier["courierId"]]:
            ok_courier = False
        elif order["productType"] in courier["exclusions"]:
            ok_courier = False
        
        if ok_courier:
            matching_couriers.append(courier)
    
    return matching_couriers


def best_matching_courier(order, couriers, couriers_capacity):
    
    available_couriers = matching_couriers(order, couriers, couriers_capacity)
    
    if not available_couriers:
        return None
    else:
        available_couriers.sort(key= lambda c: (c["priority"], c["dailyCapacity"], c["courierId"]))
        return available_couriers[0]
    

def initialize_daily_capacity(couriers):
    daily_capacity = {}

    for courier in couriers:
        daily_capacity[courier["courierId"]] = courier["dailyCapacity"]

    return daily_capacity

def initialize_capacity_usage(couriers):
    capacity_usage = []

    for courier in couriers:
        capacity_usage.append({"courierId": courier["courierId"], "totalWeight": 0})

    return capacity_usage

def write_plan(plan):
    with open("plan.json", "w") as plan_file:
        json.dump(plan, plan_file, indent=4, default=str)

def plan_order_couriers(orders, couriers):
    assignments = []
    unassigned = []
    couriers_current_capacity = initialize_daily_capacity(couriers)
    capacity_usage = {}

    orders.sort(key= lambda o: o["deadline"])
    for order in orders:
        courier = best_matching_courier(order, couriers, couriers_current_capacity)

        if courier:
            assignments.append({"orderId": order["orderId"], "courierId": courier["courierId"]})
            couriers_current_capacity[courier["courierId"]] -= order["weight"]
            
            if not capacity_usage.get(courier["courierId"]):
                capacity_usage[courier["courierId"]] = 0

            capacity_usage[courier["courierId"]] += order["weight"]
            
        else:
            unassigned.append({"orderId": order["orderId"], "reason": "no_supported_courier_or_capacity"})

              
    assignments.sort(key= lambda a: a["orderId"])
    capacity_usage = [{"courierId": k, "totalWeight": v} for k, v in sorted(capacity_usage.items(), key=lambda item: item[0])]
    
    plan = {"assignments": assignments, "unassigned": unassigned, "capacityUsage": capacity_usage}
    return plan

    
