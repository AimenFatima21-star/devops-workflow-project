#!/usr/bin/env python3
"""Web server version of the data processing app"""

import sqlite3
import json
import pandas as pd
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

class DataProcessor:
    def __init__(self):
        self.connection = sqlite3.connect('transactions.db')
        self.cursor = self.connection.cursor()
        print("[OK] Connected to SQLite database")
        self.create_tables()
        self.load_sample_data()

    def create_tables(self):
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
        self.cursor.execute("SELECT COUNT(*) FROM transactions")
        count = self.cursor.fetchone()[0]
        if count > 0:
            print(f"[INFO] Sample data exists ({count} records)")
            return

        print("[DATA] Loading sample data...")
        import random
        from datetime import timedelta

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

        base_date = datetime.now().date()
        transactions = []
        for i in range(100):
            customer_id = (i % 5) + 1
            amount = round((i + 1) * 10.50, 2)
            txn_date = base_date - timedelta(days=i % 30)
            txn_type = ['purchase', 'refund', 'transfer', 'deposit', 'withdrawal'][i % 5]
            transactions.append((customer_id, txn_type, amount, f"{txn_date} {random.randint(8, 20)}:{random.randint(0, 59)}:00"))

        self.cursor.executemany(
            "INSERT INTO transactions (customer_id, transaction_type, amount, created_at) VALUES (?, ?, ?, ?)",
            transactions
        )
        self.connection.commit()
        print(f"[OK] Loaded {len(transactions)} transactions")

    def process_daily_transactions(self, date=None):
        if date is None:
            date = datetime.now().date()
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
            return {}
        summary = df.groupby(['customer_id', 'customer_name']).agg({
            'amount': ['sum', 'mean', 'count'],
            'transaction_type': lambda x: x.value_counts().to_dict()
        })
        summary.columns = ['total_amount', 'avg_amount', 'transaction_count', 'transaction_types']
        summary = summary.reset_index()
        summary['processed_at'] = datetime.now().isoformat()
        return summary.to_dict(orient='records')

    def close(self):
        if self.connection:
            self.connection.close()

# Initialize processor
processor = DataProcessor()

class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'database': 'connected'
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/summary':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            results = processor.process_daily_transactions()
            self.wfile.write(json.dumps(results).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')

    def log_message(self, format, *args):
        pass

def run_server(port=8080):
    print(f"[START] Starting web server on port {port}")
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, AppHandler)
    print(f"[OK] Server running at http://localhost:{port}")
    print(f"📊 Summary: http://localhost:{port}/summary")
    print(f"💚 Health: http://localhost:{port}/health")
    print("[PRESS Ctrl+C to stop]")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[STOP] Shutting down server...")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()
