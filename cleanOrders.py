import datetime
import json
import re
import csv
from collections import defaultdict


def read_orders(file_name):
    orders = []
    with open(file_name, "r") as orders_file:
        orders = json.load(orders_file)

    return orders

def write_cleaned_orders(cleaned_orders, warnings):
    
    cleaned_orders.sort(key= lambda o: o["orderId"])
    if warnings :
        output_data = {
            "cleaned_orders": cleaned_orders,
            "warnings": warnings
        }
    else:
        output_data = {
            "cleaned_orders": cleaned_orders
        }

    with open("clean_orders.json", "w") as clean_order_file:
        json.dump(output_data, clean_order_file, indent=4, default=str)
            


def clean_orders(orders):
    """ Clean each order and then remove duplicates """
    cleaned_orders = []
    for order in orders:
        cleaned_orders.append(clean_order(order))

    return handle_duplicate_orders(cleaned_orders)


def clean_order(order):
        
        # Order_ID
        order_id = order["orderId"]
        order_id = normalize_order_id(order_id)

        # City
        city = order["city"]
        city = normalize_city(city)

        # Zone hint
        zone_hint = order["zoneHint"]
        zone_hint = normalize_zone_hint(zone_hint)
        
        # Address
        address = order["address"]
        address = normalize_address(address)

        # Payment type
        payment_type = order["paymentType"]
        payment_type = normalize_payment_type(payment_type)

        # Product type
        product_type = order["productType"]
        product_type = normalize_product_type(product_type)

        # weight
        weight = order["weight"]
        weight = normalize_weight(weight)

        # deadline
        date = order["deadline"]
        date = normalize_date(date)

        order = {
            "orderId": order_id,
            "city": city,
            "zoneHint": zone_hint,
            "address": address,
            "paymentType": payment_type,
            "productType": product_type,
            "weight": weight,
            "deadline": date
        }

        return order


""" Normalization part / Helper functions """
def normalize_order_id(order_id):
    """ Allow optional letters, optional digits """
    
    match = re.search(r"([A-Za-z]*)(?:[- ]?)(\d*)", order_id.strip())
    if match:
        letters = match.group(1).upper()
        numbers = match.group(2)
        
        if letters and numbers:
            return f"{letters}-{numbers}"
        elif letters:
            return letters
        elif numbers:
            return numbers
    
    return None

def normalize_city(city):
    # Read the zones.csv

    zones = load_zones("zones.csv")
    canonical = zones.get(city)

    if canonical is None:
        if city in zones.values():
            return city

    return canonical
    
def normalize_zone_hint(zone_hint):

    zones = load_zones("zones.csv")

    parts = re.split(r'([\-\,])', zone_hint)
    normalized_parts = []
    
    for part in parts:
        p_clean = part.strip()
        if p_clean in zones:
            normalized_parts.append(zones[p_clean])
        else:
            normalized_parts.append(part.strip())
    return " ".join(normalized_parts).replace(" - ", " - ")
    
    
def normalize_address(addr):
    return ''.join(ch.lower() for ch in addr if ch.isalnum() or ch.isspace()).strip()

def normalize_payment_type(payment_type):
    payment_type = payment_type.strip().upper()

    if re.search(r"COD", payment_type):
        return "COD"
    elif re.search(r"PREPAID", payment_type) or re.search(r"PAID", payment_type):
        return "Prepaid"
    else:
        return None

def normalize_product_type(product_type):
    product_type = product_type.strip().upper()

    if re.search(r"STANDARD", product_type):
        return "standard"
    elif re.search(r"FRAGILE", product_type):
        return "fragile"
    else:
        return None

def normalize_weight(weight):
    weight = str(weight).strip()

    match = re.search(r"\d+(\.\d+)?", weight)
    if match:
        return float(match.group())
    
    return None

def normalize_date(date):
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
    ]

    for fmt in formats:
        try:
            return datetime.datetime.strptime(date.strip(), fmt)
        except ValueError:
            continue
    return None

def load_zones(file_name):
    zones = {}
    with open(file_name, newline='') as zones_file:
        reader = csv.DictReader(zones_file)

        for row in reader:
            zones[row["raw"]] = row["canonical"]
    return zones

""" End of Normalization """

def handle_duplicate_orders(cleaned_orders):

    """ Gather duplicate orders with the same orderId and merege them with optional warnings """
    grouped_orders = defaultdict(list)
    warnings = []

    # Gather duplicate orderId
    for order in cleaned_orders:
        grouped_orders[order["orderId"]].append(order)

    # Merge duplicates
    for order_id, items in grouped_orders.items():
        if len(items) > 1:
            grouped_orders[order_id] = merge_orders(items, warnings)
        else:
            grouped_orders[order_id] = items[0]

    unique = list(grouped_orders.values())
    return unique, warnings

def merge_orders(duplicate_orders, warnings):
    
    addresses = set()
    for order in duplicate_orders:
        addresses.add(order["address"])

    if len(addresses) != 1:
        warnings.append(f"Conflict in {order["orderId"]}")
    
    duplicate_orders.sort(key= lambda o: o["deadline"])

    return duplicate_orders[0]

