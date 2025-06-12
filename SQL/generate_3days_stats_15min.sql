-- Generate 3 days of 15-minute interval statistics data
-- Data will be generated for 2025-05-19 00:00:00 to 2025-05-21 23:45:00

INSERT INTO db_stat.stat_15min (measure_type, collect_time, value, label, description)
SELECT 
    measure_type,
    collect_time,
    CASE 
        WHEN RAND() < 0.2 THEN GREATEST(base_value - 30, 0)
        WHEN RAND() < 0.4 THEN GREATEST(base_value - 15, 0)
        WHEN RAND() < 0.6 THEN base_value
        WHEN RAND() < 0.8 THEN base_value + 15
        ELSE base_value + 30
    END as value,
    label,
    description
FROM (
    SELECT 
        DATE_FORMAT('2025-05-19 08:00:00' + INTERVAL seq * 15 MINUTE, '%Y%m%d%H%i') as collect_time
    FROM (
        SELECT a.N + b.N * 10 + c.N * 100 as seq
        FROM (SELECT 0 as N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a
        CROSS JOIN (SELECT 0 as N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) b
        CROSS JOIN (SELECT 0 as N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) c
        WHERE a.N + b.N * 10 + c.N * 100 < 320  -- 3 days * 24 hours * 4 intervals per hour
    ) numbers
) time_series
CROSS JOIN (
    SELECT 'AAA_AUTH_COUNT' as measure_type, 900 as base_value, 'Total number of AAA authentication' as label, 'Total number of AAA authentication' as description
    UNION ALL SELECT 'AAA_AUTH_SUCC', 900, 'Number of successful AAA authentication', 'Number of successful AAA authentication'
    UNION ALL SELECT 'APNS_PUSH_SUCC_COUNT', 900, 'IOS APNS push successful count', NULL
    UNION ALL SELECT 'APPLE_WATCH_ESIM_SUB_MM_ACTIVATE_SUCC', 600, 'Successful Count Of Apple Watch Multi-SIM activation', NULL
    UNION ALL SELECT 'APPLE_WATCH_ESIM_SUB_SA_ACTIVATE_SUCC', 450, 'Successful Count Of Apple Watch Standalone activation', NULL
    UNION ALL SELECT 'CARRIER_WEBSHEET_REQ_SUCC_COUNT', 750, 'The number of successful requests made by ES to the Carrier''s WebSheet', NULL
    UNION ALL SELECT 'ES_ESB_QUERYNEWSIMCARD_REQ_SUCCESS_COUNT', 600, 'The number of successful queryNewSimCard requests initiated by the SOAP', NULL
    UNION ALL SELECT 'ES_ESB_UPDSUBSCRIBERSIMCARD_REQ_SUCCESS_COUNT', 600, 'The number of successful updSubscriberSimCard requests initiated by the SOAP', NULL
    UNION ALL SELECT 'ES_OM_READSUBRDATAWS_REQ_SUCCESS_COUNT', 1050, 'The number of successful readSubrDataWS requests initiated by the SOAP', NULL
    UNION ALL SELECT 'ES_OM_SAVESCNDSIMWS_REQ_SUCCESS_COUNT', 750, 'The number of successful saveScndSIMWS requests initiated by the SOAP', NULL
    UNION ALL SELECT 'ES_RD_READCARDWS_REQ_SUCCESS_COUNT', 900, 'The number of successful readcardWS requests initiated by the SOAP', NULL
    UNION ALL SELECT 'ESIM_CLIENT_CONFIRM_ORDER_REQ_SUCC_COUNT', 1050, 'Number of successful ESIMCLIENT ConfirmOrder requests', NULL
    UNION ALL SELECT 'ESIM_CLIENT_DOWNLOAD_ORDER_REQ_SUCC_COUNT', 1050, 'Number of successful ESIMCLIENT DownloadOrder requests', NULL
    UNION ALL SELECT 'ESIM_CLIENT_HANDLE_DOWN_LOAD_SUCC_COUNT', 750, 'Number of successful ESIMCLIENT HandleDownloadProgressInfo requests', NULL
    UNION ALL SELECT 'UDM_REQ_SUCC_COUNT', 900, 'The number of successful UDM calls made by ES instances', NULL
    UNION ALL SELECT 'UE_ES_GET_PHONE_NUMBER_REQ_SUCC_COUNT', 900, 'The number of successful GetPhoneNumber requests initiated by the UE', NULL
    UNION ALL SELECT 'UE_ES_INTERACT_COUNT', 2700, 'UE to ES request times', NULL
    UNION ALL SELECT 'UE_ES_SIGN_UP_FOR_SIM_STATUS_REQ_SUCC_COUNT', 900, 'Number of successful MultiSIM sign up requests initiated by UE', NULL
    UNION ALL SELECT 'WEBSHEET_ES_INTERACT_COUNT', 900, 'WebSheet to ES request times', NULL
) measures
ORDER BY collect_time, measure_type; 