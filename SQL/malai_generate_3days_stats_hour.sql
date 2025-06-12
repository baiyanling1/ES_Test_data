-- Generate 3 days of hourly interval statistics data
-- Data will be generated for 2025-05-19 00:00:00 to 2025-05-21 23:00:00

INSERT INTO db_stat.stat_hour (measure_type, collect_time, value, label, description)
SELECT 
    measure_type,
    collect_time,
    CASE 
        WHEN RAND() < 0.2 THEN GREATEST(base_value - 10, 0)
        WHEN RAND() < 0.4 THEN GREATEST(base_value - 5, 0)
        WHEN RAND() < 0.6 THEN base_value
        WHEN RAND() < 0.8 THEN base_value + 5
        ELSE base_value + 10
    END as value,
    label,
    description
FROM (
    SELECT 
        DATE_FORMAT('2025-05-19 08:00:00' + INTERVAL seq * 1 HOUR, '%Y%m%d%H%i') as collect_time
    FROM (
        SELECT a.N + b.N * 10 + c.N * 100 as seq
        FROM (SELECT 0 as N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a
        CROSS JOIN (SELECT 0 as N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) b
        CROSS JOIN (SELECT 0 as N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) c
        WHERE a.N + b.N * 10 + c.N * 100 < 80  -- 3 days * 24 hours
    ) numbers
) time_series
CROSS JOIN (
    SELECT 'AAA_AUTH_COUNT' as measure_type, 3600 as base_value, 'Total number of AAA authentication' as label, 'Total number of AAA authentication' as description
    UNION ALL SELECT 'AAA_AUTH_SUCC', 3600, 'Number of successful AAA authentication', 'Number of successful AAA authentication'
    UNION ALL SELECT 'APNS_PUSH_FAIL_COUNT', 600, 'IOS APNS push failed count', NULL
    UNION ALL SELECT 'ESIM_CLIENT_CONFIRM_ORDER_REQ_SUCC_COUNT', 4200, 'Number of successful ESIMCLIENT ConfirmOrder requests', NULL
    UNION ALL SELECT 'ESIM_CLIENT_DOWNLOAD_ORDER_REQ_FAIL_COUNT', 900, 'Number of failed ESIMCLIENT DownloadOrder requests', NULL
    UNION ALL SELECT 'FCM_PUSH_FAIL_COUNT', 600, 'Android FCM push failed count', NULL
    UNION ALL SELECT 'QUERY_COMPANIONESIM_SUBSCRIPTION_FAIL_COUNT', 900, 'Number of failed companion eSIM subscription queries', NULL
    UNION ALL SELECT 'QUERY_COMPANIONESIM_SUBSCRIPTION_SUCC_COUNT', 3600, 'Number of successful companion eSIM subscription queries', NULL
    UNION ALL SELECT 'QUERY_SOAP_FAIL_COUNT', 1200, 'Number of failed SOAP queries', NULL
    UNION ALL SELECT 'QUERY_SOAP_SUCC_COUNT', 4800, 'Number of successful SOAP queries', NULL
    UNION ALL SELECT 'SOAP_NOTIFY_ESIM_TRANSFER_FAIL_COUNT', 900, 'Number of failed eSIM transfer notifications via SOAP', NULL
    UNION ALL SELECT 'SOAP_NOTIFY_ESIM_TRANSFER_SUCC_COUNT', 3600, 'Number of successful eSIM transfer notifications via SOAP', NULL
    UNION ALL SELECT 'UE_ES_INTERACT_COUNT', 10800, 'UE to ES request times', NULL
) measures
ORDER BY collect_time, measure_type; 