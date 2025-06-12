-- Generate 3 days of 5-minute interval statistics data
-- Data will be generated for 2025-05-19 00:00:00 to 2025-05-21 23:55:00

INSERT INTO db_stat.stat_5min (measure_type, collect_time, value, label, description)
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
        DATE_FORMAT('2025-05-19 08:00:00' + INTERVAL seq * 5 MINUTE, '%Y%m%d%H%i') as collect_time
    FROM (
        SELECT a.N + b.N * 10 + c.N * 100 as seq
        FROM (SELECT 0 as N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a
        CROSS JOIN (SELECT 0 as N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) b
        CROSS JOIN (SELECT 0 as N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) c
        WHERE a.N + b.N * 10 + c.N * 100 < 960  -- 3 days * 24 hours * 12 intervals per hour
    ) numbers
) time_series
CROSS JOIN (
    SELECT 'AAA_AUTH_COUNT' as measure_type, 300 as base_value, 'Total number of AAA authentication' as label, 'Total number of AAA authentication' as description
    UNION ALL SELECT 'AAA_AUTH_SUCC', 300, 'Number of successful AAA authentication', 'Number of successful AAA authentication'
    UNION ALL SELECT 'APNS_PUSH_SUCC_COUNT', 300, 'IOS APNS push successful count', NULL
    UNION ALL SELECT 'APPLE_WATCH_ESIM_SUB_MM_ACTIVATE_SUCC', 200, 'Successful Count Of Apple Watch Multi-SIM activation', NULL
    UNION ALL SELECT 'APPLE_WATCH_ESIM_SUB_SA_ACTIVATE_SUCC', 150, 'Successful Count Of Apple Watch Standalone activation', NULL
    UNION ALL SELECT 'CARRIER_WEBSHEET_REQ_SUCC_COUNT', 250, 'The number of successful requests made by ES to the Carrier''s WebSheet', NULL
    UNION ALL SELECT 'ES_ESB_QUERYNEWSIMCARD_REQ_SUCCESS_COUNT', 200, 'The number of successful queryNewSimCard requests initiated by the SOAP', NULL
    UNION ALL SELECT 'ES_ESB_UPDSUBSCRIBERSIMCARD_REQ_SUCCESS_COUNT', 200, 'The number of successful updSubscriberSimCard requests initiated by the SOAP', NULL
    UNION ALL SELECT 'ES_OM_READSUBRDATAWS_REQ_SUCCESS_COUNT', 350, 'The number of successful readSubrDataWS requests initiated by the SOAP', NULL
    UNION ALL SELECT 'ES_OM_SAVESCNDSIMWS_REQ_SUCCESS_COUNT', 250, 'The number of successful saveScndSIMWS requests initiated by the SOAP', NULL
    UNION ALL SELECT 'ES_RD_READCARDWS_REQ_SUCCESS_COUNT', 300, 'The number of successful readcardWS requests initiated by the SOAP', NULL
    UNION ALL SELECT 'ESIM_CLIENT_CONFIRM_ORDER_REQ_SUCC_COUNT', 350, 'Number of successful ESIMCLIENT ConfirmOrder requests', NULL
    UNION ALL SELECT 'ESIM_CLIENT_DOWNLOAD_ORDER_REQ_SUCC_COUNT', 350, 'Number of successful ESIMCLIENT DownloadOrder requests', NULL
    UNION ALL SELECT 'ESIM_CLIENT_HANDLE_DOWN_LOAD_SUCC_COUNT', 250, 'Number of successful ESIMCLIENT HandleDownloadProgressInfo requests', NULL
    UNION ALL SELECT 'UDM_REQ_SUCC_COUNT', 300, 'The number of successful UDM calls made by ES instances', NULL
    UNION ALL SELECT 'UE_ES_GET_PHONE_NUMBER_REQ_SUCC_COUNT', 300, 'The number of successful GetPhoneNumber requests initiated by the UE', NULL
    UNION ALL SELECT 'UE_ES_INTERACT_COUNT', 900, 'UE to ES request times', NULL
    UNION ALL SELECT 'UE_ES_SIGN_UP_FOR_SIM_STATUS_REQ_SUCC_COUNT', 300, 'Number of successful MultiSIM sign up requests initiated by UE', NULL
    UNION ALL SELECT 'WEBSHEET_ES_INTERACT_COUNT', 300, 'WebSheet to ES request times', NULL
) measures
ORDER BY collect_time, measure_type; 