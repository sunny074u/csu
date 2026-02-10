"""
phtrs_summary.py

A small console summary of the main actors and use cases for a
Pothole Tracking & Repair System (PHTRS).

Run:
  python phtrs_summary.py
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class UseCase:
    name: str
    purpose: str


@dataclass(frozen=True)
class Actor:
    name: str
    description: str


def build_model() -> tuple[Dict[str, Actor], Dict[str, List[UseCase]]]:
    # Actors
    actors: Dict[str, Actor] = {
        "Citizen": Actor(
            name="Citizen",
            description="Resident or business user who reports potholes, checks status, and may submit a damage claim."
        ),
        "Public Works Admin": Actor(
            name="Public Works Admin",
            description="City staff who validate reports, prioritize work, assign crews, and monitor performance."
        ),
        "Repair Crew": Actor(
            name="Repair Crew",
            description="Field team that performs repairs and records labor, materials, and repair status from a mobile page."
        ),
        "Claims Processor": Actor(
            name="Claims Processor",
            description="Staff who review citizen damage claims and decide outcomes (approve/reject)."
        ),
    }

    # Use cases (grouped by actor)
    use_cases_by_actor: Dict[str, List[UseCase]] = {
        "Citizen": [
            UseCase("Report Pothole", "Submit a pothole report with address, size, and location details; optionally add photos."),
            UseCase("Track Pothole Status", "View the current status of a reported pothole using the assigned tracking number."),
            UseCase("Submit Damage Claim", "File a damage claim tied to a pothole report and provide supporting evidence."),
            UseCase("Track Claim Status", "Check where a submitted claim is in the review process.")
        ],
        "Public Works Admin": [
            UseCase("Review / Validate Reports", "Check incoming reports for completeness/duplicates and confirm details."),
            UseCase("Set / Confirm Priority", "Confirm repair priority (often based on reported size and local rules)."),
            UseCase("Assign Repair Crew", "Assign a crew and timing to a priority pothole."),
            UseCase("Create / Update Work Order", "Maintain work order details used for dispatch and cost tracking."),
            UseCase("Generate Reports", "Produce operational and performance reports by district, time period, or priority."),
            UseCase("Review Damage Claims", "View claims, request clarifications, and route to a decision step.")
        ],
        "Repair Crew": [
            UseCase("View Assigned Work Orders", "See assigned repairs for the day with location and priority details."),
            UseCase("Update Repair Status", "Set status such as in progress, temporary repair, repaired, or not repaired."),
            UseCase("Log Hours Applied", "Record labor time spent on the repair."),
            UseCase("Record Filler Used", "Enter filler material quantity used for the repair."),
            UseCase("Capture Before/After Photo", "Attach photos that document work completion (optional).")
        ],
        "Claims Processor": [
            UseCase("Review Damage Claims", "Examine claim details, evidence, and related pothole/work order context."),
            UseCase("Approve / Reject Claim", "Record a decision and (if applicable) trigger payment/notification steps.")
        ],
    }

    return actors, use_cases_by_actor


def print_summary(actors: Dict[str, Actor], use_cases_by_actor: Dict[str, List[UseCase]]) -> None:
    print("PHTRS Use Case Summary")
    print("-" * 72)

    for actor_key in ["Citizen", "Public Works Admin", "Repair Crew", "Claims Processor"]:
        actor = actors[actor_key]
        print(f"\nActor: {actor.name}")
        print(f"  {actor.description}")

        cases = use_cases_by_actor.get(actor_key, [])
        if not cases:
            print("  Use cases: (none listed)")
            continue

        print("  Use cases:")
        for uc in cases:
            print(f"   - {uc.name}: {uc.purpose}")

    print("\nDiagram structure (high level)")
    print("-" * 72)
    print("• System boundary: PHTRS (web portal + admin dashboard + mobile crew page)")
    print("• Actors: Citizen, Public Works Admin, Repair Crew, Claims Processor")
    print("• Core flow:")
    print("  1) Citizen reports pothole → system assigns tracking number and derives district/priority")
    print("  2) Admin reviews reports → confirms priority → assigns crew and work order")
    print("  3) Crew completes repair → logs hours/materials → status updates and cost can be calculated")
    print("  4) Citizen may submit a damage claim → claims staff review and decide")


def main() -> None:
    actors, use_cases_by_actor = build_model()
    print_summary(actors, use_cases_by_actor)


if __name__ == "__main__":
    main()