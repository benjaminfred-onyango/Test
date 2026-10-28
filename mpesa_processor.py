
# mpesa_processor.py
# M-Pesa Transaction Processor

# Step 1: Create the transaction list with the provided and additional test amounts.
transactions = [
    150, 4500, 12000, 800, 25000,
    3200, 600, 18000, 950, 7500,
    120, 50000, -200, "invalid"
]

# Step 2: Initialize transaction counters and totals.
total_transactions = len(transactions)
valid_count = 0
invalid_count = 0
flagged_count = 0
total_amount = 0
valid_transactions = []

# Initialize category counters.
small_count = 0
medium_count = 0
large_count = 0


# Step 3: Format transaction amounts in Kenyan shillings.
def format_kes(amount):
    if amount == int(amount):
        return f"{int(amount):,}"
    return f"{amount:,.2f}"


# Step 4: Validate and categorize each transaction.
def process_transaction(amount):
    # Check whether the transaction amount is numeric.
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        print(f"Invalid transaction: {amount}")
        return None

    # Reject negative transaction amounts.
    if amount < 0:
        print(f"Invalid transaction: KES {format_kes(amount)}")
        return None

    # Flag transactions exceeding KES 150,000.
    if amount > 150000:
        print(f"Flagged transaction: KES {format_kes(amount)}")
        return None

    # Assign a category based on the transaction amount.
    if amount < 1000:
        category = "Small"
    elif amount < 10000:
        category = "Medium"
    else:
        category = "Large"

    # Display the transaction and its category.
    print(
        f"Transaction: KES {format_kes(amount)} "
        f"→ Category: {category}"
    )

    return category


# Step 5: Process every transaction in the list.
for amount in transactions:
    category = process_transaction(amount)

    # Skip invalid and flagged transactions.
    if category is None:
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            invalid_count += 1
        elif amount < 0:
            invalid_count += 1
        elif amount > 150000:
            flagged_count += 1
        continue

    # Update totals and record accepted transactions.
    valid_count += 1
    total_amount += amount
    valid_transactions.append(amount)

    # Update the relevant category counter.
    if category == "Small":
        small_count += 1
    elif category == "Medium":
        medium_count += 1
    elif category == "Large":
        large_count += 1


# Step 6: Calculate transaction statistics.
if valid_transactions:
    average_amount = total_amount / valid_count
    highest_amount = max(valid_transactions)
    lowest_amount = min(valid_transactions)
else:
    average_amount = 0
    highest_amount = 0
    lowest_amount = 0


# Step 7: Display the complete transaction summary.
print("\n========== M-PESA TRANSACTION SUMMARY ==========")
print(f"Total transactions: {total_transactions}")
print(f"Accepted transactions: {valid_count}")
print(f"Invalid transactions: {invalid_count}")
print(f"Flagged transactions: {flagged_count}")
print(f"Total amount: KES {format_kes(total_amount)}")
print(f"Average amount: KES {format_kes(average_amount)}")
print(f"Highest transaction: KES {format_kes(highest_amount)}")
print(f"Lowest transaction: KES {format_kes(lowest_amount)}")

print("\nTransaction Categories:")
print(f"Small (below KES 1,000): {small_count}")
print(f"Medium (KES 1,000–9,999): {medium_count}")
print(f"Large (KES 10,000 and above): {large_count}")
print("================================================")


# Step 8: Allow the user to check additional transaction amounts.
while True:
    answer = input("\nCheck another amount? (yes/no): ").strip().lower()

    if answer == "yes":
        user_input = input("Enter transaction amount in KES: ").strip()

        try:
            amount = float(user_input)

            # Reject non-finite numeric values.
            if amount != amount or amount in (
                float("inf"), float("-inf")
            ):
                print(f"Invalid transaction: {user_input}")
                continue

            # Validate and categorize the entered amount.
            process_transaction(amount)

        except ValueError:
            print(f"Invalid transaction: {user_input}")

    elif answer == "no":
        # End the program when the user is finished.
        print(
            "Thank you for using the M-Pesa Transaction Processor. "
            "Goodbye!"
        )
        break

    else:
        # Request a valid response.
        print("Please enter 'yes' or 'no'.")
