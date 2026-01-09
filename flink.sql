CREATE TABLE marks_streams (

  id STRING,
  score STRING,
  event_time TIMESTAMP(3) METADATA FROM 'timestamp',
  WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND

) WITH (
  'connector' = 'kafka',
  'topic' = 'marks_clean',
  'properties.bootstrap.servers' = 'localhost:9095,localhost:9097,localhost:9102',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'json',
  'json.ignore-parse-errors' = 'true',
  'json.fail-on-missing-field' = 'false'
);



CREATE TABLE marks_raw (

  id STRING,
  score STRING,
  event_time TIMESTAMP(3) METADATA FROM 'timestamp',
  WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND

) WITH (
  'connector' = 'kafka',
  'topic' = 'marks',
  'properties.bootstrap.servers' = 'localhost:9095,localhost:9097,localhost:9102',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'json',
  'json.ignore-parse-errors' = 'true',
  'json.fail-on-missing-field' = 'false'
);
