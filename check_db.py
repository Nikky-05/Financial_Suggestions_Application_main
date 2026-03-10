import sqlite3

conn = sqlite3.connect('financial_app.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("\n" + "="*50)
print("  SQLite Database Contents")
print("="*50 + "\n")

total_records = 0
for table in tables:
    table_name = table[0]
    cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
    count = cursor.fetchone()[0]
    total_records += count
    print(f"✓ {table_name:20} : {count:,} records")

print("\n" + "="*50)
print(f"Total Records in Database: {total_records:,}")
print("="*50 + "\n")

conn.close()
