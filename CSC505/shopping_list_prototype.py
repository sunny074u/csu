# shopping_list_prototype.py

# Define screens
screens = [
    "Home",
    "Add Item",
    "View List",
    "Edit Item",
    "Settings"
]

# Define navigation flow
navigation_flow = {
    "Home": ["Add Item", "View List", "Settings"],
    "Add Item": ["View List"],
    "View List": ["Edit Item", "Home"],
    "Edit Item": ["View List"],
    "Settings": ["Home"]
}

# Screen descriptions
screen_descriptions = {
    "Home": "Displays saved shopping lists and main navigation options.",
    "Add Item": "Allows the user to add a new item to the shopping list.",
    "View List": "Shows all items in the selected shopping list.",
    "Edit Item": "Edit or delete an existing item.",
    "Settings": "Application preferences and about information."
}

# Output summary
print("Screens:")
for screen in screens:
    print(f"- {screen}: {screen_descriptions[screen]}")

print("\nTotal Screens:", len(screens))

print("\nNavigation Flow:")
for source, destinations in navigation_flow.items():
    for destination in destinations:
        print(f"{source} → {destination}")
