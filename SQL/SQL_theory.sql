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

DATE and TIME functions in SQL are used to manipulate and 
extract information from date and time values.

2. time duration in sql:
    SELECT 
        emp_id,
        activity,
        start_time,
        end_time,
        TIMESTAMPDIFF(HOUR, start_time, end_time) AS duration_hours
    FROM employee_log;
  Postgres
EXTRACT(EPOCH FROM (  first_login - last_login    )) / 3600.0  AS duration_hours
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

---------------------------------------------------------

20251024 - YYYYMMDD - 
🐘 PostgreSQL
SELECT TO_CHAR(TO_DATE('20251024', 'YYYYMMDD'), 'DD-MM-YYYY') AS formatted_date;
🐬 MySQL
SELECT DATE_FORMAT(STR_TO_DATE('20251024', '%Y%m%d'), '%d-%m-%Y') AS formatted_date;
🐝 HiveQL (on AWS EMR)
SELECT date_format(CAST('2025-10-24' AS DATE), 'dd-MM-yyyy') AS formatted_date;
Hive expects a proper date format like '2025-10-24', so you may need to convert 20251024 to 
that format first using string functions.

----------------------------------------------------------------------------
--✅ Generic SQL (MySQL, SQL Server, PostgreSQL with slight tweaks)
SELECT *FROM your_table
WHERE DAY(date_column) = 30  AND MONTH(date_column) = 10;
--This will return all rows where the date is October 30th (regardless of year).

--✅ Generic SQL (MySQL, SQL Server)
SQLSELECT *FROM your_table
WHERE DAY(date_column) = 30  AND MONTH(date_column) = 10  AND YEAR(date_column) = 2025;

--✅ PostgreSQL
SQLSELECT *FROM your_table
WHERE EXTRACT(DAY FROM date_column) = 30  AND EXTRACT(MONTH FROM date_column) = 10  AND EXTRACT(YEAR FROM date_column) = 2025;

--✅ Oracle SQL
SQLSELECT *FROM your_table
WHERE TO_CHAR(date_column, 'DD') = '30'  AND TO_CHAR(date_column, 'MM') = '10'  AND TO_CHAR(date_column, 'YYYY') = '2025';

-- ✅ SQL Query (Works in PostgreSQL, SQL Server, etc.)

SELECT 
        cust_id,
DATE_TRUNC('month', order_date) AS order_month;


--join:

Tab1
1
1
2
NULL
2
NULL
3

Tab2
1
2
2
NULL
NULL
3

what will the inner join and left join output

inner join - 
1	1
1	1
2	2
2	2
2	2
2	2
3	3

left join-
1		1
1		1
2		2
2		2
2		2
2		2
NULL	NULL
NULL	NULL
3		3

FULL OUTER JOIN - 👉 Total = 11 rows
| Tab1 | Tab2 |
| --- | --- |
| 1 | 1 |
| 1 | 1 |
| 2 | 2 |
| 2 | 2 |
| 2 | 2 |
| 2 | 2 |
| 3 | 3 |
| NULL | NULL |
| NULL | NULL |
| NULL | NULL |
| NULL | NULL |
FULL OUTER JOIN (Tab1 FULL OUTER JOIN Tab2 ON Tab1.Value = Tab2.Value)
A FULL OUTER JOIN returns:

All matching rows
All non-matching rows from both tables
Matches are by value (NULL does not match NULL)

👉 Rules:
Each 1 in Tab1 matches each 1 in Tab2 (2×1 = 2 rows)
Each 2 in Tab1 matches each 2 in Tab2 (2×2 = 4 rows)
Each 3 in Tab1 matches the single 3 in Tab2 (1 row)
NULL does not match NULL → all NULLs show separately

✔️ Final FULL OUTER JOIN Output (explicit):
Matching rows

1 × 1 → 2 rows
2 × 2 → 4 rows
3 × 3 → 1 row

Non-matching rows (NULLs):

Tab1 NULLs → 2 rows
Tab2 NULLs → 2 rows

Final table will have:

2 (for 1s)
+4 (for 2s)
+1 (for 3s)
+2 (Tab1 NULLs unmatched)
+2 (Tab2 NULLs unmatched)

👉 Total = 11 rows
-----------------------------------------------------------------------------------------

In SQL, unpivoting refers to the process of converting columns into rows — 
the opposite of pivoting, which turns rows into columns.

Col_A 	| 	Col_B
ABC		|	aa
CDE		|	cd 	
EFG		|	ef
EFG		|	aa
ABC		|	bb
ABC		|	cc
 
Output :
 
Col_A	| Column_1 	|  Column_2	  | Column_3
ABC		|  aa		|	bb		  |	cc		
CDE		|  cd		|			  | 	
EFG		|  ef		|	aa		  |	, solve using SQL


WITH ranked AS (
  SELECT
    Col_A,
    Col_B,
    ROW_NUMBER() OVER (PARTITION BY Col_A ORDER BY Col_B) AS rn
  FROM src_table_with_ordercol
)
SELECT
  Col_A,
  MAX(CASE WHEN rn = 1 THEN Col_B END) AS Column_1,
  MAX(CASE WHEN rn = 2 THEN Col_B END) AS Column_2,
  MAX(CASE WHEN rn = 3 THEN Col_B END) AS Column_3
FROM ranked
GROUP BY Col_A
ORDER BY Col_A;
----------------------------
To merge (collapse) into one row → use an aggregate function
We need to combine the 3 rows into 1:

For rn=1 → pick "aa"
For rn=2 → pick "bb"
For rn=3 → pick "cc"

MAX() works because:

Each column contains one non‑NULL value per group
MAX() returns that non‑NULL value

Example for Column_1:
MAX(aa, NULL, NULL) = aa

🎯 Why MAX instead of MIN or SUM?
You can use any aggregate that:
✔ Ignores NULL values
✔ Returns the single non‑NULL value
MAX() is the standard choice because its safe and clear.
MIN() would also work.
SUM() does not work (string mismatch).

-- connect to PostgreSQL and load data into a pandas DataFrame
import psycopg2
import pandas as pd

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="your_host",
    database="your_db",
    user="your_user",
    password="your_password"
)

# Query and load into DataFrame
query = "SELECT * FROM your_table_name"
df = pd.read_sql_query(query, conn)

conn.close()
print(df.head())