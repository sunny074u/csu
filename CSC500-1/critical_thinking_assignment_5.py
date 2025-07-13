# PART 1: Average Rainfall Calculator

def calculate_average_rainfall():
    total_rainfall = 0.0
    total_months = 0

    years = int(input("Enter the number of years: "))

    for year in range(1, years + 1):
        print(f"\nYear {year}:")
        for month in range(1, 13):
            while True:
                try:
                    rainfall = float(input(f"Enter rainfall in inches for month {month}: "))
                    if rainfall < 0:
                        print("Rainfall cannot be negative. Try again.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")

            total_rainfall += rainfall
            total_months += 1

    average_rainfall = total_rainfall / total_months
    print("\n--- Rainfall Statistics ---")
    print(f"Total Months: {total_months}")
    print(f"Total Rainfall: {total_rainfall:.2f} inches")
    print(f"Average Rainfall per Month: {average_rainfall:.2f} inches")

# PART 2: Bookstore Points Calculator

def calculate_bookstore_points():
    try:
        books_purchased = int(input("\nEnter the number of books purchased this month: "))
        if books_purchased == 0:
            points = 0
        elif books_purchased == 2:
            points = 5
        elif books_purchased == 4:
            points = 15
        elif books_purchased == 6:
            points = 30
        elif books_purchased >= 8:
            points = 60
        else:
            points = 0  # Optional rule for odd numbers like 1, 3, 5, 7

        print(f"Points awarded: {points}")
    except ValueError:
        print("Invalid input. Please enter a whole number.")

# MAIN EXECUTION
if __name__ == "__main__":
    calculate_average_rainfall()
    calculate_bookstore_points()
