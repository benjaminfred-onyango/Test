
# mpesa_processor.py
# M-Pesa Transaction Processor

# Step 1: Create a list of transaction amounts
# The first five amounts are sample transactions.
# The last three are additional test amounts, including an invalid amount.
transactions = [100, 250, 0, 500, 1000, 150, -50, "invalid"]

# Step 2: Initialize counters and totals
valid_count = 0
invalid_count = 0
total_amount = 0

# Step 3: Process each transaction
for amount in transactions:

    # Step 4: Skip transactions with invalid data types
    if not isinstance(amount, (int, float)):
        print(f"Invalid transaction: {amount}")
        invalid_count += 1
        continue

    # Step 5: Skip zero or negative transaction amounts
    if amount <= 0:
        print(f"Corrupted transaction skipped: {amount}")
        invalid_count += 1
        continue

    # Step 6: Process valid transactions
    print(f"Transaction processed: KSh {amount}")
    valid_count += 1
    total_amount += amount

# Step 7: Display the transaction summary
print("\n--- M-Pesa Transaction Summary ---")
print(f"Valid transactions: {valid_count}")
print(f"Invalid transactions: {invalid_count}")
print(f"Total valid amount: KSh {total_amount}")
