"""
atm_steps.py
Prints step-by-step sequences for key ATM operation paths reflected in the UML state machine diagram.

This script is intentionally "print-first" to satisfy the assignment requirement:
"print all the steps in sequence for all the operations at the teller machine as shown in your diagram(s)."
"""

from dataclasses import dataclass

@dataclass
class ATMConfig:
    max_fails: int = 3

def banner(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)

def scenario_successful_withdrawal(amount: float = 60.0) -> None:
    banner("Scenario A — Successful withdrawal")
    print("Idle: Waiting for customer.")
    print("Event: InsertCard [cardValid] / readCard()")
    print("State: CardInserted (entry/ promptForPIN())")
    print("Event: EnterPIN / capturePIN()")
    print("Event: CheckPIN [pinCorrect] / resetFailCounter()")
    print("State: Authenticated")
    print("Event: ShowMenu / displayOptions()")
    print("Event: SelectWithdraw / captureAmount()")
    print(f"Event: CheckBalance [balance >= amount] / debitAccount()  (amount={amount})")
    print("Event: Dispense / printReceipt()")
    print("Event: Complete / ejectCard()")
    print("Event: RemoveCard / endSession()")
    print("Back to Idle.")

def scenario_incorrect_pin_then_success(config: ATMConfig) -> None:
    banner("Scenario B — Incorrect PIN once, then success")
    fails = 0
    print("Idle: Waiting for customer.")
    print("Event: InsertCard [cardValid] / readCard()")
    print("State: CardInserted (entry/ promptForPIN())")

    # Attempt 1
    print("Event: EnterPIN / capturePIN()")
    fails += 1
    print(f"Event: CheckPIN [pinIncorrect && failCount < maxFails] / incrementFailCounter()  (failCount={fails}, maxFails={config.max_fails})")
    print("State: CardInserted (entry/ promptForPIN())")

    # Attempt 2
    print("Event: EnterPIN / capturePIN()")
    print("Event: CheckPIN [pinCorrect] / resetFailCounter()")
    print("State: Authenticated")
    print("Event: ShowMenu / displayOptions()")
    print("Event: SelectWithdraw / captureAmount()")
    print("Event: CheckBalance [balance >= amount] / debitAccount()")
    print("Event: Dispense / printReceipt()")
    print("Event: Complete / ejectCard()")
    print("Event: RemoveCard / endSession()")
    print("Back to Idle.")

def scenario_rejected_after_max_fails(config: ATMConfig) -> None:
    banner("Scenario C — Rejected after too many incorrect PIN attempts")
    fails = 0
    print("Idle: Waiting for customer.")
    print("Event: InsertCard [cardValid] / readCard()")
    print("State: CardInserted (entry/ promptForPIN())")

    while True:
        print("Event: EnterPIN / capturePIN()")
        fails += 1

        if fails >= config.max_fails:
            print(f"Event: CheckPIN [pinIncorrect && failCount >= maxFails] / retainCardAndReject()  (failCount={fails}, maxFails={config.max_fails})")
            print("State: Rejected")
            print("Event: End / logEvent()")
            print("Back to Idle.")
            break
        else:
            print(f"Event: CheckPIN [pinIncorrect && failCount < maxFails] / incrementFailCounter()  (failCount={fails}, maxFails={config.max_fails})")
            print("State: CardInserted (entry/ promptForPIN())")

def scenario_balance_zero_account_closed() -> None:
    banner("Scenario D — Balance is zero, account closed")
    print("Idle: Waiting for customer.")
    print("Event: InsertCard [cardValid] / readCard()")
    print("State: CardInserted (entry/ promptForPIN())")
    print("Event: EnterPIN / capturePIN()")
    print("Event: CheckPIN [pinCorrect] / resetFailCounter()")
    print("State: Authenticated")
    print("Event: ShowMenu / displayOptions()")
    print("Event: SelectWithdraw / captureAmount()")
    print("Event: CheckBalance [balance == 0] / closeAccount()")
    print("State: AccountClosed")
    print("Event: End / logEvent()")
    print("Back to Idle.")

def main() -> None:
    config = ATMConfig(max_fails=3)

    scenario_successful_withdrawal(amount=60.0)
    scenario_incorrect_pin_then_success(config)
    scenario_rejected_after_max_fails(config)
    scenario_balance_zero_account_closed()

if __name__ == "__main__":
    main()
