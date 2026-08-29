import sqlite3
import pandas as pd
from datetime import datetime
import os
import random
from datetime import timedelta

class DataProcessor:
    def __init__(self):
        """Initialize SQLite database connection"""
        self.connection = sqlite3.connect('transactions.db')
        self.cursor = self.connection.cursor()
        print("[OK] Connected to SQLite database")
    
    def create_tables(self):
        """Create required tables"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                transaction_type TEXT,
                amount REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'completed',
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        self.connection.commit()
        print("[OK] Tables created successfully")
    
    def load_sample_data(self):
        """Load sample data"""
        # Check if data exists
        self.cursor.execute("SELECT COUNT(*) FROM transactions")
        count = self.cursor.fetchone()[0]
        
        if count > 0:
            print(f"[INFO] Sample data already exists ({count} records)")
            return
        
        print("[DATA] Loading sample data...")
        
        # Insert customers
        customers = [
            (1, 'Alice Johnson', 'alice@example.com'),
            (2, 'Bob Smith', 'bob@example.com'),
            (3, 'Carol White', 'carol@example.com'),
            (4, 'Dave Brown', 'dave@example.com'),
            (5, 'Eve Davis', 'eve@example.com')
        ]
        self.cursor.executemany(
            "INSERT OR IGNORE INTO customers (id, name, email) VALUES (?, ?, ?)",
            customers
        )
        
        # Insert transactions
        base_date = datetime.now().date()
        transactions = []
        
        for i in range(100):
            customer_id = (i % 5) + 1
            amount = round((i + 1) * 10.50, 2)
            txn_date = base_date - timedelta(days=i % 30)
            txn_type = ['purchase', 'refund', 'transfer', 'deposit', 'withdrawal'][i % 5]
            
            transactions.append((
                customer_id,
                txn_type,
                amount,
                f"{txn_date} {random.randint(8, 20)}:{random.randint(0, 59)}:00"
            ))
        
        self.cursor.executemany(
            "INSERT INTO transactions (customer_id, transaction_type, amount, created_at) VALUES (?, ?, ?, ?)",
            transactions
        )
        
        self.connection.commit()
        print(f"[OK] Loaded {len(transactions)} transactions")
    
    def process_daily_transactions(self, date=None):
        """Process transactions for a specific date"""
        if date is None:
            date = datetime.now().date()
        
        print(f"[DATA] Processing transactions for {date}")
        
        query = """
        SELECT 
            t.customer_id,
            t.transaction_type,
            t.amount,
            t.created_at,
            c.name as customer_name
        FROM transactions t
        LEFT JOIN customers c ON t.customer_id = c.id
        WHERE DATE(t.created_at) = ?
        ORDER BY t.created_at
        """
        
        df = pd.read_sql_query(query, self.connection, params=[str(date)])
        
        if df.empty:
            print(f"[WARNING] No transactions found for {date}")
            return pd.DataFrame()
        
        summary = df.groupby(['customer_id', 'customer_name']).agg({
            'amount': ['sum', 'mean', 'count'],
            'transaction_type': lambda x: x.value_counts().to_dict()
        })
        
        summary.columns = ['total_amount', 'avg_amount', 'transaction_count', 'transaction_types']
        summary = summary.reset_index()
        summary['processed_at'] = datetime.now()
        
        print(f"[OK] Processed {len(summary)} customers")
        return summary
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("[LOCK] Database connection closed")

def main():
    print("[START] Starting Data Processing Application (SQLite)")
    
    processor = DataProcessor()
    
    try:
        # Create tables
        processor.create_tables()
        
        # Load sample data
        processor.load_sample_data()
        
        # Process transactions
        today = datetime.now().date()
        results = processor.process_daily_transactions(today)
        
        if not results.empty:
            print("\n" + "="*60)
            print("Daily Transaction Summary")
            print("="*60)
            print(results.to_string(index=False))
            print("="*60)
            print(f"Total Customers: {len(results)}")
            print(f"Total Transactions: {results['transaction_count'].sum()}")
            print(f"Total Amount: ${results['total_amount'].sum():,.2f}")
            print("="*60)
        else:
            print("[INFO] No transactions to process")
        
        print("[OK] Application completed successfully")
        
    except Exception as e:
        print(f"[ERROR] Application error: {e}")
    finally:
        processor.close()

if __name__ == "__main__":
    main()
