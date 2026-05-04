CREATE TABLE IF NOT EXISTS incidents (
    id SERIAL PRIMARY KEY,
    component_id VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    severity VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    rca TEXT
);
