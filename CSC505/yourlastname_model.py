# This script captures user-defined phases for the YourLastName Adaptive Model
# and outputs a structured summary.

def collect_model_phases():
    phases = []
    phase_count = int(input("How many phases are in your model? "))

    for i in range(phase_count):
        print(f"\nEnter details for Phase {i + 1}")
        name = input("Phase name: ")
        description = input("Short description: ")
        phases.append((name, description))

    return phases


def display_model(phases):
    print("\nYourLastName Adaptive Model Summary")
    print("-" * 40)
    for index, phase in enumerate(phases, start=1):
        print(f"Phase {index}: {phase[0]} - {phase[1]}")


def main():
    phases = collect_model_phases()
    display_model(phases)


if __name__ == "__main__":
    main()
