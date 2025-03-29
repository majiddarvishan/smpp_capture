-- 1️⃣ Latency over time (time-series)
SELECT time_bucket('1 minute', submit_time) AS time, AVG(latency_ms) AS avg_latency
FROM smpp_latency
GROUP BY time
ORDER BY time;

-- 2️⃣ High latency alerts (latest 10 alerts)
SELECT timestamp, alert_message
FROM smpp_alerts
ORDER BY timestamp DESC
LIMIT 10;

-- 3️⃣ Count of SMPP requests in the last 1 hour
SELECT COUNT(*)
FROM smpp_latency
WHERE submit_time > NOW() - INTERVAL '1 hour';

-- 4️⃣ Maximum latency in the last hour
SELECT MAX(latency_ms)
FROM smpp_latency
WHERE submit_time > NOW() - INTERVAL '1 hour';

-- 5️⃣ Count of packets with latency higher than average
SELECT COUNT(*)
FROM smpp_latency
WHERE latency_ms > (SELECT AVG(latency_ms) FROM smpp_latency);

-- 6️⃣ Count of packets with latency lower than average
SELECT COUNT(*)
FROM smpp_latency
WHERE latency_ms < (SELECT AVG(latency_ms) FROM smpp_latency);
