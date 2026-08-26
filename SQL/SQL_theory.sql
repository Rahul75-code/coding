Idempotency in data engineering is the property of an operation that produces the same result, no matter how many times it's executed. 
This is crucial for creating reliable and repeatable data pipelines, as it ensures that re-running a job due to a failure won't lead 
to duplicate data or corruption. Key benefits include robust failure recovery, predictable batch processing, and simplified debugging. 
Select, joining, filter, aggregating groupby

a standard View is a virtual table that re-runs its underlying query every time it is accessed, 
whereas a Materialized View is a physical cache that precomputes and saves the query results directly to disk

-----------------------
🎯 Quick Memory Trick

1. window function
  ROW_NUMBER() → Unique sequence, no ties
  RANK() → Ties allowed, gaps present
  DENSE_RANK() → Ties allowed, no gaps
  LAG() → Value from the previous row
  LEAD() → Value from the next row
-----------------------
2. time duration in sql:
    SELECT 
        emp_id,
        activity,
        start_time,
        end_time,
        TIMESTAMPDIFF(HOUR, start_time, end_time) AS duration_hours
    FROM employee_log;
  in spark:
    from pyspark.sql import functions as F
    df = df.withColumn(
        "duration_hours",
        (F.unix_timestamp("end_time") - F.unix_timestamp("start_time")) / 3600
    )
    df.show()
-----------------------
📌 Best Practice
Always check the data type of action_time.
If it’s already DATETIME → CAST(... AS DATE) is perfect.
If it’s VARCHAR → use the appropriate parsing function for your SQL dialect.

convert into date : CAST(action_time AS DATE) AS session_date