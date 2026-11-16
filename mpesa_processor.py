"""
mpesa_processor.py
M-Pesa transaction processor: validates amounts, categorises them
(Small / Medium / Large), flags suspicious ones, prints a summary
report, then lets the user check more amounts interactively.
"""

# ---------------------------------------------------------------
# STEP 1: Rules (constants)
# ---------------------------------------------------------------
SMALL_LIMIT = 1000        # below 1,000            -> Small
LARGE_LIMIT = 10000       # 10,000 and above       -> Large
FLAG_LIMIT = 150000       # above 150,000          -> Flagged


# ---------------------------------------------------------------
# STEP 2: Categorise one amount
# Returns "Small", "Medium" or "Large"
# ---------------------------------------------------------------
def categorise(amount):
    if amount < SMALL_LIMIT:
        return "Small"
    elif amount < LARGE_LIMIT:      # 1,000 to 9,999
        return "Medium"
    else:                           # 10,000 and above
        return "Large"


# ---------------------------------------------------------------
# STEP 3: Check one amount and print the result
# Returns the category if the amount is valid, otherwise None
# ---------------------------------------------------------------
def check_amount(amount):
    # Check the type first so a string never reaches a comparison
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        print(f"Invalid transaction: KES {amount}")
        return None

    # Below 0 (and zero, which is not a real payment) is invalid
    if amount <= 0:
        print(f"Invalid transaction: KES {amount}")
        return None

    # Above 150,000 is flagged for review
    if amount > FLAG_LIMIT:
        print(f"Flagged transaction: KES {amount:,}")
        return None

    # Otherwise it is valid: categorise and print
    category = categorise(amount)
    print(f"Transaction: KES {amount:,} → Category: {category}")
    return category


# ---------------------------------------------------------------
# STEP 4: Process the whole list and collect statistics
# ---------------------------------------------------------------
def process_transactions(transactions):
    valid_amounts = []
    counts = {"Small": 0, "Medium": 0, "Large": 0}
    invalid_count = 0
    flagged_count = 0

    for amount in transactions:
        category = check_amount(amount)

        if category is not None:                 # valid
            valid_amounts.append(amount)
            counts[category] += 1
        elif isinstance(amount, (int, float)) and not isinstance(amount, bool) \
                and amount > FLAG_LIMIT:         # flagged
            flagged_count += 1
        else:                                    # invalid
            invalid_count += 1

    return valid_amounts, counts, invalid_count, flagged_count


# ---------------------------------------------------------------
# STEP 5: Print the summary report
# ---------------------------------------------------------------
def print_summary(valid_amounts, counts, invalid_count, flagged_count):
    print("\n===== TRANSACTION SUMMARY =====")
    print(f"Total transactions: {len(valid_amounts)}")

    # Only calculate statistics if there is at least one valid amount
    if valid_amounts:
        total = sum(valid_amounts)
        print(f"Total amount: KES {total:,.2f}")
        print(f"Average transaction: KES {total / len(valid_amounts):,.2f}")
        print(f"Highest transaction: KES {max(valid_amounts):,.2f}")
        print(f"Lowest transaction: KES {min(valid_amounts):,.2f}")

    print(f"Small transactions: {counts['Small']}")
    print(f"Medium transactions: {counts['Medium']}")
    print(f"Large transactions: {counts['Large']}")
    print(f"Invalid transactions: {invalid_count}")
    print(f"Flagged transactions: {flagged_count}")
    print("===============================")


# ---------------------------------------------------------------
# STEP 6: Interactive loop
# ---------------------------------------------------------------
def interactive_loop():
    while True:
        answer = input("\nCheck another amount? (yes/no): ").strip().lower()

        if answer == "yes":
            raw = input("Enter amount in KES: ").strip()
            try:
                amount = float(raw)
                if amount.is_integer():          # show 4500 not 4500.0
                    amount = int(amount)
            except ValueError:
                print(f"Invalid transaction: KES {raw}")
                continue
            check_amount(amount)

        elif answer == "no":
            print("Thank you for using the M-Pesa Transaction Processor. Goodbye!")
            break

        else:
            print("Please type 'yes' or 'no'.")


# ---------------------------------------------------------------
# STEP 7: Test data and program entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # List from the brief
    brief_list = [150, 4500, 12000, 800, 25000, 3200, 600, 18000, 950, 7500]

    # My own amounts: 2 valid, 1 flagged, 1 invalid (negative)
    my_tests = [
        2750,       # valid (Medium)
        999,        # valid (Small, just below the boundary)
        200000,     # flagged (above 150,000)
        -500,       # INVALID (below 0)
    ]

    transactions = brief_list + my_tests

    results = process_transactions(transactions)
    print_summary(*results)
    interactive_loop()