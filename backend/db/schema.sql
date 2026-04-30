CREATE TABLE IF NOT EXISTS packets (
    id          SERIAL PRIMARY KEY,
    src_ip      VARCHAR(45),
    dst_ip      VARCHAR(45),
    src_port    INT,
    dst_port    INT,
    protocol    VARCHAR(10),
    length      INT,
    timestamp   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS alerts (
    id           SERIAL PRIMARY KEY,
    src_ip       VARCHAR(45),
    attack_type  VARCHAR(50),
    confidence   FLOAT DEFAULT 1.0,
    details      TEXT,
    timestamp    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS blocked_ips (
    id         SERIAL PRIMARY KEY,
    ip_address VARCHAR(45) UNIQUE,
    reason     VARCHAR(100),
    blocked_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS traffic_stats (
    id              SERIAL PRIMARY KEY,
    packets_per_sec INT,
    recorded_at     TIMESTAMP DEFAULT NOW()
);

-- Indexes for faster dashboard queries
CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_packets_src_ip ON packets(src_ip);
CREATE INDEX IF NOT EXISTS idx_traffic_recorded ON traffic_stats(recorded_at DESC);