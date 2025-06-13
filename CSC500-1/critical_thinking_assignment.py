# Part 1: Addition and Subtraction
print("=== Part 1: Addition and Subtraction ===")
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

addition = num1 + num2
subtraction = num1 - num2

print(f"Addition: {num1} + {num2} = {addition}")
print(f"Subtraction: {num1} - {num2} = {subtraction}")

# Part 2: Multiplication and Division
print("\n=== Part 2: Multiplication and Division ===")
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

multiplication = num1 * num2

if num2 != 0:
    division = num1 / num2
    print(f"Multiplication: {num1} * {num2} = {multiplication}")
    print(f"Division: {num1} / {num2} = {division}")
else:
    print(f"Multiplication: {num1} * {num2} = {multiplication}")
    print("Division: Cannot divide by zero")
