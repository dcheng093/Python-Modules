#!/usr/bin/python3.10
import sys

if __name__ == "__main__":
    print("=== Inventory System Analysis ===")
    inventory: dict[str, int] = {}
    for arg in sys.argv[1:]:
        if ":" not in arg:
            print(f"Error - invalid parameter '{arg}'")
            continue
        name, qty_str = arg.split(":", 1)
        if name in inventory:
            print(f"Redundant item '{name}' - discarding")
            continue
        try:
            qty = int(qty_str)
        except ValueError as e:
            print(f"Quantity error for '{name}': {e}")
            continue
        inventory.update({name: qty})
    print(f"Got inventory: {inventory}")
    items = list(inventory.keys())
    print(f"Item list: {items}")
    total = sum(inventory.values())
    print(f"Total quantity of the {len(inventory)} items: {total}")
    if total != 0:
        for name in items:
            percent = inventory[name] / total * 100
            print(f"Item {name} represents {round(percent, 1)}%")
    if len(items) > 0:
        most_item = items[0]
        least_item = items[0]
        for name in items:
            if inventory[name] > inventory[most_item]:
                most_item = name
            if inventory[name] < inventory[least_item]:
                least_item = name
        print(f"Item most abundant: {most_item} "
              f"with quantity {inventory[most_item]}")
        print(f"Item least abundant: {least_item} "
              f"with quantity {inventory[least_item]}")
    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")

# def parse_inventory(args):
#     """Parse command-line args like sword:1 potion:5 into a dict"""
#     inventory = {}
#     for arg in args:
#         if ":" in arg:
#             name, qty = arg.split(":")
#             inventory[name] = int(qty)
#     return inventory


# def display_inventory_stats(inventory):
#     total_items = sum(inventory.values())
#     unique_items = len(inventory)
#     print("=== Inventory System Analysis ===")
#     print(f"Total items in inventory: {total_items}")
#     print(f"Unique item types: {unique_items}")
#     print("\n=== Current Inventory ===")
#     for item, qty in sorted(inventory.items(), key=lambda x: -x[1]):
#         percent = (qty / total_items) * 100
#         print(f"{item}: {qty} unit{'s' if qty > 1 else ''} ({percent:.1f}%)")
#     most_item = max(inventory.items(), key=lambda x: x[1])
#     least_item = min(inventory.items(), key=lambda x: x[1])
#     print("\n=== Inventory Statistics ===")
#     print(f"Most abundant: {most_item[0]} ({most_item[1]} units)")
#     print(f"Least abundant: {least_item[0]} ({least_item[1]} units)")
#     moderate = {k: v for k, v in inventory.items() if v > 3}
#     scarce = {k: v for k, v in inventory.items() if v <= 3}
#     print("\n=== Item Categories ===")
#     print(f"Moderate: {moderate}")
#     print(f"Scarce: {scarce}")
#     restock = [item for item, qty in inventory.items() if qty == 1]
#     print("\n=== Management Suggestions ===")
#     if restock:
#         print("Restock needed:", ", ".join(restock))
#     else:
#         print("All items sufficiently stocked")
#     print("\n=== Dictionary Properties Demo ===")
#     print("Dictionary keys:", ", ".join(inventory.keys()))
#     print("Dictionary values:",",".join(str(v) for v in inventory.values()))
#     sample_item = 'sword'
#     print(f"Sample lookup - '{sample_item}' in inventory:",
#           sample_item in inventory)


# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python3 ft_inventory_system.py sword:1 potion:5 ...")
#         sys.exit(1)
#     inventory = parse_inventory(sys.argv[1:])
#     display_inventory_stats(inventory)


# def display_inventory(player_name, player_dict):
#     print(f"=== {player_name}'s Inventory ===\n")
#     inventory = player_dict.get(player_name, {})
#     total_val = 0
#     total_items = 0
#     cat = {}
#     for item, details in inventory.items():
#         item_type = details.get("type")
#         rarity = details.get("rarity")
#         qty = details.get("quantity")
#         val = details.get("value")
#         print(f"{item} ({item_type}, {rarity}): {qty}x @ {val} gold each = "
#               f"{qty * val} gold")
#         total_val += qty * val
#         total_items += qty
#         cat[item_type] = cat.get(item_type, 0) + qty
#     print("")
#     print(f"Inventory value: {total_val} gold")
#     print(f"Item count: {total_items} items")
#     print("Categories: ", end="")
#     cat_items = cat.items()
#     count = 0
#     total_cats = len(cat)
#     for name, qty in cat_items:
#         count += 1
#         print(f"{name}({qty})", end="")
#         if count < total_cats:
#             print(", ", end="")
#     print("")


# def transaction_update(player1, player2, item_name, qty, player_dict):
#     inv1 = player_dict.get(player1)
#     inv2 = player_dict.get(player2)
#     item_data = inv1.get(item_name)
#     if item_data and item_data.get("quantity") >= qty:
#         item_data["quantity"] -= qty
#         if item_name not in inv2:
#             inv2[item_name] = {
#                 "type": item_data.get("type"),
#                 "rarity": item_data.get("rarity"),
#                 "quantity": qty,
#                 "value": item_data.get("value")
#             }
#         else:
#             inv2[item_name]["quantity"] += qty
#         print("")
#         print(f"=== Transaction:{player1} gives {player2} {qty} {item_name}s"
#               " ===")
#         print("Transaction successful!")
#         print("")
#         p1_qty = inv1.get(item_name).get("quantity")
#         p2_qty = inv2.get(item_name).get("quantity")
#         print("=== Updated Inventories ===")
#         print(f"{player1} {item_name}: {p1_qty}")
#         print(f"{player2} {item_name}: {p2_qty}")
#         print("")
#     else:
#         print("Transaction failed: Not enough items!")
#         print("")


# def display_analytics(player_dict):
#     print("=== Inventory Analytics ===")
#     mvp_name = ""
#     max_gold = 0
#     most_items_name = ""
#     max_items = 0
#     for name, inv in player_dict.items():
#         current_total = 0
#         item_count = 0
#         for details in inv.values():
#             current_total += details.get("quantity") * details.get("value")
#             item_count += details.get("quantity")
#         if current_total > max_gold:
#             max_gold = current_total
#             mvp_name = name
#         if item_count > max_items:
#             max_items = item_count
#             most_items_name = name
#     print(f"Most valuable player: {mvp_name} ({max_gold} gold)")
#     print(f"Most items: {most_items_name} ({max_items} items)")
#     rare_items = {}
#     for inv in player_dict.values():
#         for item, details in inv.items():
#             if details.get("rarity") == "rare":
#                 rare_items[item] = True
#     if rare_items:
#         print("Rarest items: ", end="")
#         count = 0
#         total = len(rare_items)
#         for item in rare_items.keys():
#             count += 1
#             print(item, end="")
#             if count < total:
#                 print(", ", end="")
#         print("")
#     print("")


# if __name__ == "__main__":
#     print("=== Player Inventory System ===\n")
#     players = {
#         "Alice": {
#             "sword": {"type": "weapon", "rarity": "rare", "quantity": 1,
#                       "value": 500},
#             "potion": {"type": "consumable", "rarity":"common", "quantity":5,
#                        "value": 50},
#             "shield": {"type": "armor", "rarity": "uncommon", "quantity": 1,
#                        "value": 200}
#         },
#         "Bob": {
#             "magic_ring": {"type": "ring", "rarity": "rare", "quantity": 1,
#                            "value": 1}
#         }
#     }
#     display_inventory("Alice", players)
#     transaction_update("Alice", "Bob", "potion", 2, players)
#     display_analytics(players)
