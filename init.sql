-- Initialize database with extensions
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Enable performance monitoring
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET work_mem = '64MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET pg_stat_statements.track = 'all';
SELECT pg_reload_conf();

-- Create table structure (if not exists)
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'completed'
);

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_transactions_customer ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_created ON transactions(created_at);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(transaction_type);

-- Display setup completion
\echo '✅ Database initialization complete'
\echo '✅ Tables created: transactions, customers'
\echo '✅ Indexes created for performance'
\echo '✅ Extensions installed: pg_stat_statements'