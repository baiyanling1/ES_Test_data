-- Generate 1 day of 1-minute interval statistics data
-- Data will be generated for 2025-05-19 00:00:00 to 2025-05-19 23:59:00

INSERT INTO db_stat.stat_min (measure_type, collect_time, value, label, description)
SELECT 
    measure_type,
    collect_time,
    CASE 
        WHEN RAND() < 0.2 THEN GREATEST(base_value - 2, 0)
        WHEN RAND() < 0.4 THEN GREATEST(base_value - 1, 0)
        WHEN RAND() < 0.6 THEN base_value
        WHEN RAND() < 0.8 THEN base_value + 1
        ELSE base_value + 2
    END as value,
    label,
    description
FROM (
    SELECT 
        DATE_FORMAT('2025-05-22 00:00:00' + INTERVAL seq * 1 MINUTE, '%Y%m%d%H%i') as collect_time
    FROM (
        SELECT a.N + b.N * 10 + c.N * 100 as seq
        FROM (SELECT 0 as N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a
        CROSS JOIN (SELECT 0 as N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) b
        CROSS JOIN (SELECT 0 as N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) c
        WHERE a.N + b.N * 10 + c.N * 100 < 10  -- 1 day * 24 hours * 60 minutes
    ) numbers
) time_series
CROSS JOIN (
    SELECT 'AAA_AUTH_COUNT' as measure_type, 60 as base_value, 'Total number of AAA authentication' as label, 'Total number of AAA authentication' as description
    UNION ALL SELECT 'AAA_AUTH_SUCC', 60, 'Number of successful AAA authentication', 'Number of successful AAA authentication'
    UNION ALL SELECT 'APNS_PUSH_FAIL_COUNT', 10, 'IOS APNS push failed count', NULL
    UNION ALL SELECT 'ESIM_CLIENT_CONFIRM_ORDER_REQ_SUCC_COUNT', 70, 'Number of successful ESIMCLIENT ConfirmOrder requests', NULL
    UNION ALL SELECT 'ESIM_CLIENT_DOWNLOAD_ORDER_REQ_FAIL_COUNT', 15, 'Number of failed ESIMCLIENT DownloadOrder requests', NULL
    UNION ALL SELECT 'FCM_PUSH_FAIL_COUNT', 10, 'Android FCM push failed count', NULL
    UNION ALL SELECT 'QUERY_COMPANIONESIM_SUBSCRIPTION_FAIL_COUNT', 15, 'Number of failed companion eSIM subscription queries', NULL
    UNION ALL SELECT 'QUERY_COMPANIONESIM_SUBSCRIPTION_SUCC_COUNT', 60, 'Number of successful companion eSIM subscription queries', NULL
    UNION ALL SELECT 'QUERY_SOAP_FAIL_COUNT', 20, 'Number of failed SOAP queries', NULL
    UNION ALL SELECT 'QUERY_SOAP_SUCC_COUNT', 80, 'Number of successful SOAP queries', NULL
    UNION ALL SELECT 'SOAP_NOTIFY_ESIM_TRANSFER_FAIL_COUNT', 15, 'Number of failed eSIM transfer notifications via SOAP', NULL
    UNION ALL SELECT 'SOAP_NOTIFY_ESIM_TRANSFER_SUCC_COUNT', 60, 'Number of successful eSIM transfer notifications via SOAP', NULL
    UNION ALL SELECT 'UE_ES_INTERACT_COUNT', 180, 'UE to ES request times', NULL
) measures
ORDER BY collect_time, measure_type; 