import sqlite3

conn = sqlite3.connect('financial_app.db')
cursor = conn.cursor()

# Find user with income around 635000
cursor.execute("SELECT user_id, SUM(amount) as total FROM income GROUP BY user_id HAVING total >= 630000 AND total <= 640000")
rows = cursor.fetchall()

if rows:
    print("Users with income ~6.35 lakh:")
    user_id = rows[0][0]
    print(f"User {user_id}: ₹{rows[0][1]}")
    
    # Show their income records
    print(f"\nIncome records for User {user_id}:")
    cursor.execute("SELECT id, source, amount, date FROM income WHERE user_id = ? ORDER BY date DESC", (user_id,))
    for row in cursor.fetchall():
        print(f"  ID {row[0]}: {row[1]} - ₹{row[2]} ({row[3]})")
else:
    # Find users with highest income
    print("No user found with exactly 6.35 lakh. Top 5 users by income:")
    cursor.execute("SELECT user_id, SUM(amount) as total FROM income GROUP BY user_id ORDER BY total DESC LIMIT 5")
    for row in cursor.fetchall():
        print(f"User {row[0]}: ₹{row[1]}")

conn.close()
