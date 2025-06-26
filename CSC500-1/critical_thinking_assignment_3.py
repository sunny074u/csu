# Part 1: Meal Total Calculator

while True:
    try:
        food_charge = float(input("Enter the charge for the food: $"))
        if food_charge < 0:
            print("Please enter a positive number.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a number.")

tip = food_charge * 0.18
tax = food_charge * 0.07
total = food_charge + tip + tax

print(f"Food Charge: ${food_charge:.2f}")
print(f"Tip (18%): ${tip:.2f}")
print(f"Sales Tax (7%): ${tax:.2f}")
print(f"Total Amount: ${total:.2f}")



# Part 2: Alarm Clock Calculation

while True:
    try:
        current_time = int(input("What is the current time (0–23)? "))
        if current_time < 0 or current_time > 23:
            print("Time must be between 0 and 23.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a whole number between 0 and 23.")

while True:
    try:
        hours_to_wait = int(input("How many hours to wait for the alarm? "))
        if hours_to_wait < 0:
            print("Please enter a non-negative number.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a whole number.")

alarm_time = (current_time + hours_to_wait) % 24
print(f"The alarm will go off at {alarm_time}:00 hours.")