import sqlite3

conn = sqlite3.connect('financial_app.db')
cursor = conn.cursor()

# Check income records
cursor.execute('SELECT COUNT(*) as total_records FROM income')
total = cursor.fetchone()[0]
print(f"Total Income Records in Database: {total}")

# Check by user
cursor.execute('SELECT user_id, COUNT(*) as count, SUM(amount) as total FROM income GROUP BY user_id')
print("\nIncome by User:")
for row in cursor.fetchall():
    print(f"  User {row[0]}: {row[1]} records, Total: ₹{row[2]}")

# Show recent income records
print("\nRecent Income Records (last 10):")
cursor.execute('SELECT id, user_id, source, amount, date FROM income ORDER BY date DESC LIMIT 10')
for row in cursor.fetchall():
    print(f"  ID {row[0]} | User {row[1]} | {row[2]} | ₹{row[3]} | {row[4]}")

# Check expenses
print("\n" + "="*50)
cursor.execute('SELECT COUNT(*) as total_records FROM expenses')
total = cursor.fetchone()[0]
print(f"Total Expense Records in Database: {total}")

# Check expenses by user
cursor.execute('SELECT user_id, COUNT(*) as count, SUM(amount) as total FROM expenses GROUP BY user_id')
print("\nExpenses by User:")
for row in cursor.fetchall():
    print(f"  User {row[0]}: {row[1]} records, Total: ₹{row[2]}")

conn.close()
