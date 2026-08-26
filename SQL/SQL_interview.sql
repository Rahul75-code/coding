
topics - --
Suggest and Implement best practices / innovative ways/ re-usable solutions Suggest/ implement value adds which will benefit in cost/ time saving


find the max sale from the order table from each category in new column
----------------------------------------------------------------------------------------



Q>> find top salary from each department ?
employee
ID, name, dept_id, Sal	rn
1	abc		1		10	
2	bcd		1		11	
3	xyz		1		9	
4	buf		2		20
5	yui		2		5	
6	ghi		3		12
7	dhr		2		5

with row_sal(
select ID, name, dept_id, Sal,
rank() over(partition by dept_id, order by Sal desc) as rn
from employee
);

select* 
from row_sal
where rn = 1;

----------------------------------------------------------------------------------------
find running total of sales using window functiion, in sql
df = 
category     Date         Sales
A            2024-01-01   100
B            2024-01-01   50
A            2024-01-02   150
B            2024-01-02   75
A            2024-01-03   200
B            2024-01-03   120


SELECT 
    category,
    Date,
    Sales,
    SUM(Sales) OVER (
        PARTITION BY category 
        ORDER BY Date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM sales;

---------------------------------------------------------------------------------------------------------------------
✅ Moving Window Sum — Simple Definition
A moving window sum calculates the sum of values within a fixed window of rows, which “moves” as you go down your dataset.
✅ SQL Example — Moving Window Sum (last 2 rows)
SELECT
    value,
    SUM(value) OVER (
        ORDER BY id
        ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
    ) AS moving_sum
FROM table;
--------------------------
✅ Cumulative Sum (Running Total)
Sum of all previous rows up to current.
SUM(value) OVER (
    ORDER BY id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
-------------------------------------------------------------------------------------------------------
✅ Moving Sum
Sum of last N rows only.
SUM(value) OVER (
    ORDER BY id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
-------------------------------------------------------------------------------------------------------

Employee table
Emp_No	Emp_Name	Salary	Location	Dept_No
101		Graham		10345	New York	40
102		Mike		20436	Toranto		30
103		Dean		15730	Mexico		60
104		John		10000	New York	40
105		Sara		25000	New York	40


Department Table:
Dept_No	Dept_Name
30		Sales
40		Marketing
50		Audit
 
-- second highest salary in Sales department with emp name

with sales_t as (
select e.Emp_No, e.Emp_Name, e.Salary, d.Dept_No
from Employee e
join Department d
on d.Dept_No = e.Dept_No
where d.Dept_Name = 'Sales'
order by e.Salary desc
)

select Emp_No, Emp_Name, Dept_No, Salary
from sales_t
offset = 1
limit - 1
-------------------------------------------------------------------------------------------------

-- Scenario 3: Hierarchical Data and Recursive Queries
-- You have an Employees table with EmployeeID, EmployeeName, and ManagerID (which references EmployeeID for the employee's manager).

-- Task: Write a SQL query to find all direct and indirect subordinates of a given ManagerID.

WITH RECURSIVE Subordinates AS (
    SELECT EmployeeID, EmployeeName, ManagerID
    FROM Employees
    WHERE ManagerID = 101  -- Replace with the given ManagerID
    UNION ALL
    SELECT E.EmployeeID, E.EmployeeName, E.ManagerID
    FROM Employees E
    INNER JOIN Subordinates S ON E.ManagerID = S.EmployeeID
)
SELECT * FROM Subordinates;

----------------------------------------------------------------------------------------------

-- to include manger name
WITH RECURSIVE Subordinates AS (
    -- Anchor: direct subordinates of the given manager
    SELECT 
        e.EmployeeID,
        e.EmployeeName,
        e.ManagerID
    FROM Employees e
    WHERE e.ManagerID = @ManagerID  -- Replace with actual ManagerID

    UNION ALL

    -- Recursive: find subordinates of already found employees
    SELECT 
        e.EmployeeID,
        e.EmployeeName,
        e.ManagerID
    FROM Employees e
    INNER JOIN Subordinates s ON e.ManagerID = s.EmployeeID
)
SELECT 
    s.EmployeeID,
    s.EmployeeName,
    s.ManagerID,
    m.EmployeeName AS ManagerName
FROM Subordinates s
LEFT JOIN Employees m ON s.ManagerID = m.EmployeeID;

----------------------------------------------------------------------------------------------------------

-- Task: Write a SQL query to find the entire management hierarchy (upwards) for a specific EmployeeID.
WITH RECURSIVE ManagementHierarchy AS (
    SELECT EmployeeID, EmployeeName, ManagerID
    FROM Employees
    WHERE EmployeeID = 105  -- Replace with the specific EmployeeID
    UNION ALL
    SELECT E.EmployeeID, E.EmployeeName, E.ManagerID
    FROM Employees E
    INNER JOIN ManagementHierarchy MH ON E.EmployeeID = MH.ManagerID
)
SELECT * FROM ManagementHierarchy;


----------------------------------------------------------------------------------------------------------

-- SQL implementation of SCD Type 1
-- 🔹 Step-by-Step SQL Example
-- 		A target dimension table: dim_customer
-- 		A staging table with new data: stg_customer
UPDATE dim_customer dim
SET 
    Name = stg.Name,
    Address = stg.Address
FROM stg_customer stg
WHERE dim.Customer_ID = stg.Customer_ID;

INSERT INTO dim (Customer_ID, Name, Address)
SELECT stg.Customer_ID, stg.Name, stg.Address
FROM stg_customer stg
LEFT JOIN dim_customer dim
    ON stg.Customer_ID = dim.Customer_ID
WHERE dim.Customer_ID IS NULL;

----------------------------------------------------------------------------------------------
-- SCD 2
-- src_tbl, trg_tbl
-- Step 1: Expire old records
UPDATE target_table tgt
SET end_date = CURRENT_DATE,
    Current_Flag = 'N'
FROM source_table src
WHERE tgt.customer_id = src.customer_id
  AND tgt.Current_Flag = 'Y'
  AND (
    tgt.name <> src.name OR
    tgt.address <> src.address
  ); 
---------------------------
-- Step 2: Insert new and updated records
INSERT INTO target_table (customer_id, name, address, effective_date, end_date, Current_Flag)
SELECT src.customer_id, src.name, src.address, CURRENT_DATE, DATE '9999-12-31', 'Y'
FROM source_table src
LEFT JOIN target_table tgt
  ON src.customer_id = tgt.customer_id AND tgt.Current_Flag = 'Y'
WHERE tgt.customer_id IS NULL
   OR (
     tgt.name <> src.name OR
     tgt.address <> src.address
   );

-----------------------------------------------------------------------------------------------

update tgt as t
set t.flag = 'n', t.end_date = current_date()
from src as s 
where s.id = t.id and t.flag = 'y' and
(s.name <> t.name or s.city <> t.city);

insert into tgt(,,,,,)
select s.name,,,,,current_date(), null, 'y'
from stg as s 
left join tgt as t 
on t.id = s.id and t.flag ='y'
where t.id is null
or (s.name <> t.name or s.city <> t.city);
-----------------------------------------------------------------------------------------------

MERGE INTO dim_customer AS tgt
USING (
  SELECT s.*
  FROM stg_customer_ready s
) AS src
ON tgt.customer_id = src.customer_id
AND tgt.is_current = TRUE
WHEN MATCHED AND tgt.change_hash <> src.change_hash 
THEN
  /* expire the current row */
  UPDATE SET
    tgt.is_current        = FALSE,
    tgt.effective_end_at  = src.batch_ts
WHEN NOT MATCHED THEN
  /* insert new current version (new key or after expiration) */
  INSERT (
    customer_id, name, email, city, phone, state,
    effective_start_at, effective_end_at, is_current, version, change_hash
  )
  VALUES (
    src.customer_id, src.name, src.email, src.city, src.phone, src.state,
    src.batch_ts, NULL, TRUE,
    /* version: 1 for brand new; for changed rows we need previous version+1.
       Snowflake can compute version with a subquery: */
    COALESCE(
      (SELECT MAX(version)+1 FROM dim_customer d
       WHERE d.customer_id = src.customer_id),
      1
    ),
    src.change_hash

------------------------------------------------------

MERGE INTO dim_customer AS tgt
USING stg_customer AS src
ON tgt.customer_id = src.customer_id
AND tgt.is_current = TRUE
WHEN MATCHED AND (
    tgt.name  <> src.name
 OR tgt.email <> src.email
 OR tgt.city  <> src.city
)
THEN
  -- Expire old version
  UPDATE SET
    tgt.is_current        = FALSE,
    tgt.effective_end_at  = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN
  -- Insert new version
  INSERT (
    customer_id, name, email, city, effective_start_at, effective_end_at, is_current, version
  )
  VALUES (
    src.customer_id, src.name, src.email, src.city, CURRENT_TIMESTAMP, NULL, TRUE,
    COALESCE(
      (SELECT MAX(version)+1 FROM dim_customer d WHERE d.customer_id = src.customer_id),1)
  );

-----------------------------------------------------------------------


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

---------------------------------------------------------
----------------------------------------------------------------------------

✅ Using BETWEEN
SELECT *FROM your_table
WHERE date_column BETWEEN '2025-10-01' AND '2025-10-30';

-- This includes both start and end dates.
-- Format 'YYYY-MM-DD' is standard for most SQL engines.


✅ Using >= and <=
SELECT *FROM your_table
WHERE date_column >= '2025-10-01'  AND date_column <= '2025-10-30';

-- Same result as BETWEEN, but gives you more flexibility if you want to use exclusive bounds (e.g., < instead of <=).

----------------------------------------------------------------------------

SELECT CURRENT_DATE - INTERVAL 40 DAY AS past_date;
 -- employees who joined in the last 30 days from the employee table
SELECT emp_id, emp_name, join_date
FROM employee
WHERE join_date >= CURRENT_DATE - INTERVAL 30 DAY;


table a	  table b
------------- ----------------
name		 name
------------- ----------------
Kiran	 	 NULL
NULL	 	 Madhu
Sam	 	 	 John	 	
			 Kiran
	 	     Sam
	 	     NULL
		     Kiran
			 
 what is the count of rows for each join for above table 
 
--------------------
 left - 2+1+1 = 4
 right - 1+1+1+1+1+1+1 = 7
 inner - 2+1 = 3
 outer - 3+1+4 = 8
-----------------------------------------------------------------------------
------------------------------------------------------------------------
Q>> find duplicate ID ?
select emp_id, count(emp_id) as cnt 
from employees
group by emp_id
having cnt >= 2

-----------------------------------------------------------------------
-- 3.Find employees with salary greater than their departmental average.
EMP_ID DEPT_NBR 	SAL
101     50    	    2000
102     50       	2200
103     50 			2400
104     60 			3000
105     60 			2000
106     70 			1000
107     70 			2000

-- Step 1: Define the CTE to calculate average salary per department
WITH DeptAvg AS (
    SELECT DEPT_NBR, AVG(SAL) AS Avg_Sal
    FROM Employee
    GROUP BY DEPT_NBR
)

-- Step 2: Use the CTE to find employees with salary greater than the departmental average
SELECT e.EMP_ID, e.DEPT_NBR, e.SAL
FROM Employee e
JOIN DeptAvg d ON e.DEPT_NBR = d.DEPT_NBR
WHERE e.SAL > d.Avg_Sal;

or 

SELECT EMP_ID, DEPT_NBR, SAL
FROM employee e
WHERE SAL > (
    SELECT AVG(SAL)
    FROM employee
    WHERE DEPT_NBR = e.DEPT_NBR
);

------------------------------------------------------------------------
Write a SQL query to print only the names of students who passed all subjects.
 
Table: student_marks
Columns: Name, Mark, Subject
 
Example Data:
Anand, Eng, 50
Anand, Math, 70
Anand, Science, 30
Mahesh, Eng, 90
Mahesh, Math, 92
Mahesh, Science, 78
 
Output:
Mahesh
---------

select name 
from table
group by name
having min(mark) >= 40

or

SELECT Name
FROM student_marks
GROUP BY Name
HAVING COUNT(CASE WHEN Mark >= 40 THEN 1 END) = COUNT(Subject);

------------------------------------------------------------------------

emp table -  emp_id , name
leave table - leave_id, start_date, end_date
assingment table - ass_id, leave_id, emp_id, hire_date
write a query to find emp_id who hired after 1/1/2025 and no leaves in feb  2025
---------------------
WITH hired_emp AS (
    SELECT e.emp_id, e.name, a.hire_date
    FROM emp e
    JOIN assignment a 
      ON e.emp_id = a.emp_id
    WHERE a.hire_date > '2025-01-01'
),
leave_in_feb AS (
    SELECT DISTINCT a.emp_id
    FROM assignment a
    JOIN leave l 
      ON a.leave_id = l.leave_id
    WHERE l.start_date <= '2025-02-28'
      AND l.end_date >= '2025-02-01'
)
SELECT h.emp_id, h.name
FROM hired_emp h
LEFT JOIN leave_in_feb l
  ON h.emp_id = l.emp_id
WHERE l.emp_id IS NULL;

----or-----

WITH d AS (
    SELECT e.emp_id, e.name, a.leave_id
    FROM emp AS e
    JOIN assignment AS a
      ON e.emp_id = a.emp_id
    WHERE a.hire_date > DATE '2025-01-01'
)
SELECT d.emp_id, d.name
FROM d
LEFT JOIN leave l
  ON d.leave_id = l.leave_id
WHERE NOT (
    l.start_date <= DATE '2025-02-28'
    AND l.end_date >= DATE '2025-02-01'
);

------------------------------------------------------------------------

student_df=
roll_no, subject, marks
	10		maths	60
	10		english	70
	10		science	80
	10		hindi	90
	20				
	20		english	60
	20		science	70
	20		hindi	80
		
output - roll_no, maths_marks, english_marks, science_marks, hindi_marks
		10		60				70				80			90
		20						60				70			80
		
write a sql query for above output
-----------
SELECT 
    roll_no,
    MAX(CASE WHEN subject = 'maths'   THEN marks END) AS maths_marks,
    MAX(CASE WHEN subject = 'english' THEN marks END) AS english_marks,
    MAX(CASE WHEN subject = 'science' THEN marks END) AS science_marks,
    MAX(CASE WHEN subject = 'hindi'   THEN marks END) AS hindi_marks
FROM student_df
GROUP BY roll_no;

------------------------------------------------------------------------

--expense table: emp_id emp_name expense_date expense_amt
--find total expense for each emp in that year ?

SELECT emp_id, emp_name, YEAR(expense_date) AS year,
           SUM(expense_amt) AS total_expense
    FROM expense
    GROUP BY emp_id, emp_name, YEAR(expense_date)
--or-----
SELECT emp_id,
       DATE_FORMAT(expense_date, '%Y') AS years,
       MAX(expense_date) AS last_expense
FROM expense
WHERE YEAR(expense_date) IN (2023, 2024, 2025)
GROUP BY emp_id, DATE_FORMAT(expense_date, '%Y');
--or-----
SELECT 
    emp_id,
    YEAR(expense_date) AS years,
    SUM(expense_amt) AS total_expense
FROM expense
WHERE YEAR(expense_date) IN (2023, 2024, 2025)
GROUP BY emp_id, YEAR(expense_date);

------------------------------------------------------------------------

cust_id, entry_date 
1			13/5
1			20/5
1			30/5
find the  maximum date for which a customer 
-------------------
SELECT cust_id,
       MAX(entry_date) AS max_entry_date
FROM customer_entries
GROUP BY cust_id;

------------------------------------------------------------------------
input - 
Team
India
pakistan
bangladesh
Srilanka

Output - 
Team A | Team B
India | Pakistan
India | Srilanka
India | Bangladesh
Pakistan | Srilanka
Pakistan | Bangladesh
Bangladesh| Srilanka
write a sql query for the above output.
-------------------------
SELECT t1.team AS TeamA,
       t2.team AS TeamB
FROM team t1
JOIN team t2
  ON t1.team < t2.team
ORDER BY TeamA, TeamB;

------------------------------------------------------------------------
-- top 5th salary from employee tbl

with emp_tbl as (
select emp_id, salary, depart,
    rank() over ( partition by depart, order by salary)  as row_num
from tbl1
)

select
 emp_id, salary, depart
from emp_tbl
where row_num = 5

------------------------------------------------------------------------

sales(region, amount, date). 
Write a query to find the second highest sale per region for the last 30 days.

WITH ranked_sales AS (
    SELECT region,
           amount,
           date,
           DENSE_RANK() OVER (PARTITION BY region ORDER BY amount DESC) AS rnk
    FROM sales
    WHERE date >= CURRENT_DATE - INTERVAL '30' DAY
)
SELECT region, amount, date
FROM ranked_sales
WHERE rnk = 2;
-------------------------------------------------------------------------
-- employee count for each department
SELECT dept_id, COUNT(*) AS employee_count
FROM employee
GROUP BY dept_id;


-- If you want to include department names
SELECT d.dept_id, d.dept_name, COUNT(e.emp_id) AS employee_count
FROM department d
LEFT JOIN employee e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name;

-------------------------------------------------------------------------

-- 1.consider the Employee table below.
Emp_Id Emp_name Salary Manager_Id
10 		Anil     50000 	18
11      Vikas    75000  16
12      Nisha    40000  18
13      Nidhi    60000  17
14      Priya    80000  18
15      Mohit    45000  18
16      Rajesh   90000  -
17      Raman    55000  16
18      Santosh  65000  17


-- Write a query to generate below output:
Manager_Id     Manager   Average_Salary_Under_Manager
    16         Rajesh           65000
    17         Raman            62500
    18         Santosh           5375

-- answer
SELECT
    m.Emp_Id      AS Manager_Id,
    m.Emp_name    AS Manager,
    AVG(e.Salary) AS Average_Salary_Under_Manager
FROM Employee AS e          -- e = employee (direct report)
JOIN Employee AS m          -- m = manager
  ON e.Manager_Id = m.Emp_Id
GROUP BY 
    m.Emp_Id, m.Emp_name
ORDER BY 
    m.Emp_Id;

or

WITH tbl2 AS (
    SELECT m.Emp_Id AS Manager_Id, m.Emp_name AS Manager, e.Salary AS Salary
    FROM Employee m
    JOIN Employee e ON m.Emp_Id = e.Manager_Id
)
SELECT Manager_Id, Manager, AVG(Salary) AS Average_Salary_Under_Manager 
FROM tbl2
GROUP BY Manager_Id, Manager;
``
----------------------------------------------------------------------------

-- from order table (customer_id, order_id, order_date, amount), Retrieve each customer’s most recent order.
WITH ranked_orders AS (
    SELECT customer_id, order_id, order_date, amount,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
    FROM order
)
SELECT customer_id, order_id, order_date, amount
FROM ranked_orders
WHERE rn = 1;


----------------------------------------------------------------------------------------
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
---------------------------------------------------------------------------
--given a sales table with columns cust_id, order_date, and amount,
--write a query to find customer who have placed orders in three consecutive months.

SELECT DISTINCT o1.cust_id
FROM sales o1
JOIN sales o2 ON o1.cust_id = o2.cust_id
JOIN sales o3 ON o1.cust_id = o3.cust_id
WHERE 
    DATE_TRUNC('month', o2.order_date) = DATE_TRUNC('month', o1.order_date) + INTERVAL '1 month' AND
    DATE_TRUNC('month', o3.order_date) = DATE_TRUNC('month', o1.order_date) + INTERVAL '2 month'

--🔍 Explanation:
--We join the sales table to itself three times for the same customer.
--We check if the second and third orders occurred in the next two consecutive months after the first.
--DATE_TRUNC('month', order_date) ensures we’re comparing by month only (ignoring day).
--INTERVAL '1 month' and '2 month' help identify consecutive months.

---------------------------------------------------------------------------

-- 3.1 Prepare staging with hash for redshift
CREATE TEMP TABLE stg_ready AS
SELECT
  customer_id, name, email, city, phone, state,
  md5(COALESCE(name,'') || '||' || COALESCE(email,'') || '||' || COALESCE(city,'')) AS change_hash,
  GETDATE() AS batch_ts
FROM stg_customer;

-- 3.2 Expire changed current rows
UPDATE dim_customer d
SET    is_current       = FALSE,
       effective_end_at = r.batch_ts
FROM   stg_ready r
WHERE  d.customer_id = r.customer_id
AND    d.is_current = TRUE
AND    d.change_hash <> r.change_hash;

-- 3.3 Insert new versions (new keys + changed keys)
INSERT INTO dim_customer (
  customer_id, name, email, city, phone, state,
  effective_start_at, effective_end_at, is_current, version, change_hash
)
SELECT
  r.customer_id, r.name, r.email, r.city, r.phone, r.state,
  r.batch_ts, NULL, TRUE,
  COALESCE(MAX(d.version) + 1, 1) AS version,
  r.change_hash
FROM stg_ready r
LEFT JOIN dim_customer d
  ON d.customer_id = r.customer_id
GROUP BY
  r.customer_id, r.name, r.email, r.city, r.phone, r.state, r.batch_ts, r.change_hash;

---------------------------------------------------------------------------------------

--> question screenshot in onenote -sql- sql query

SELECT 
    TO_CHAR(trans_date, 'YYYY-MM') AS month,
    country,
    COUNT(*) AS trans_count,
    SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_count,
    SUM(amount) AS trans_total_amount,
    SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total_amount
FROM transactions
GROUP BY TO_CHAR(trans_date, 'YYYY-MM'), country
ORDER BY month, country;


-- if date is string and need to format:
TO_CHAR(TO_DATE(trans_date, 'YYYY-MM-DD HH24:MI:SS'), 'YYYY-MM') AS month,

---------------------------------------------------------------------------------------

 emp table - 
emp_id, name, doj
-----------------
project table -
project_id, emp_id, project_name
-----------------
salary details - 
salary_id, emp_id, salary

get all emp who is working in more then 3 project and salary is less then 70000 
------------

with t as (
select e.emp_id, e.name, p.project_id, p.project_name
from emp as e join project as p
on e.emp_id = p.emp_id
group by p.emp_id
having count(project_id) > 3
)

select t.emp_id, t.name
from t join salary as s
on t.emp_id = s.emp_id
where s.salary < 70000

----------------------------------------------------------------------------

employee, department
emp_id		dpt_id
emp_name	dpt_name
salary		
dpt_id

-- departments that have no employees.

select d.dept_id, dept_name
from departments as d
left join employees as e
on e.dept_id = d.dept_id
where e.emp_id IS NULL


-- employees who are not assigned to any department.

select e.emp_id, e.emp_name
from employee e
left join department d
on e.dpt_id = d.dpt_id
where d.dpt_id IS NULL

--------------------------------------------------------------------------

-- number of employees in each department

SELECT dept_id, COUNT(*) AS employee_count
FROM employee
GROUP BY dept_id;

-- include department names & Sort by number of employees

SELECT d.dept_id, d.dept_name, COUNT(e.emp_id) AS employee_count
FROM department d
LEFT JOIN employee e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY employee_count DESC;

-- average salary per department along with the number of employees

SELECT d.dept_id,
       d.dept_name, 
       COUNT(e.emp_id) AS employee_count, 
       AVG(e.salary) AS average_salary
FROM department d
LEFT JOIN employee e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY employee_count DESC;

---------------------------------------------------------------------------------------


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


-----------------------

SELECT Emp_Name, Salary
FROM (
    SELECT E.Emp_Name, E.Salary, D.Dept_Name,
           RANK() OVER (PARTITION BY D.Dept_Name ORDER BY E.Salary DESC) AS salary_rank
    FROM Employee E
    JOIN Department D ON E.Dept_No = D.Dept_No
    WHERE D.Dept_Name = 'Sales'
) AS RankedSalaries
WHERE salary_rank = 2;

----------------------------------------------------------------------------------------

SELECT E.Emp_Name, E.Salary
FROM Employee E
JOIN Department D ON E.Dept_No = D.Dept_No
WHERE D.Dept_Name = 'Sales'
ORDER BY E.Salary DESC
LIMIT 1 OFFSET 1;

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

------------------------------------------------------------------------

Order 
order id, order date, product, qty, amount
Shipment
Shipment id, order id, shipment date
Delivery
Delivery id, order id, shipment id, delivery date
Find all orders shipped after 15th May 2025 and not yet delivered to the customer
---------------
WITH os AS (
    SELECT o.order_id, 
           o.order_date, 
           s.shipment_id, 
           s.shipment_date
    FROM orders o
    JOIN shipment s
      ON o.order_id = s.order_id
    WHERE s.shipment_date > DATE '2025-05-15'
)
SELECT os.order_id, os.shipment_id, os.shipment_date
FROM os
LEFT JOIN delivery d
  ON os.order_id = d.order_id
WHERE d.order_id IS NULL;
----or-----
WITH shipped_orders AS (
    SELECT o.order_id, o.order_date, s.shipment_id, s.shipment_date
    FROM orders o
    JOIN shipment s 
      ON o.order_id = s.order_id
    WHERE s.shipment_date > DATE '2025-05-15'
),
delivered_orders AS (
    SELECT DISTINCT d.order_id
    FROM delivery d
)
SELECT so.order_id, so.order_date, so.shipment_id, so.shipment_date
FROM shipped_orders so
LEFT JOIN delivered_orders do
  ON so.order_id = do.order_id
WHERE do.order_id IS NULL;

-- is the above query will give the same output or what need to change in above query ?
----------------------------------------------------------------------------------------
--given a sales table with columns cust_id, order_date, and amount,
--write a query to find customer who have placed orders in
----------------------------------------------------------------------------------------

WITH monthly_orders AS (
    SELECT DISTINCT 
           cust_id,
           DATE_TRUNC('month', order_date) AS order_month
    FROM sales
),
ranked AS (
    SELECT cust_id,
           order_month,
           ROW_NUMBER() OVER (PARTITION BY cust_id ORDER BY order_month) AS rn
    FROM monthly_orders
)
SELECT DISTINCT r1.cust_id
FROM ranked r1
JOIN ranked r2 
  ON r1.cust_id = r2.cust_id AND r2.rn = r1.rn + 1
JOIN ranked r3 
  ON r1.cust_id = r3.cust_id AND r3.rn = r1.rn + 2
WHERE r2.order_month = r1.order_month + INTERVAL '1 month'
  AND r3.order_month = r1.order_month + INTERVAL '2 month';

----------------------------------------------------------------------------------------

--from employee_salary_table where salary of each employee for each year, 
--find the employee who got increment for each year consecutive
--------
WITH yearly_salary AS (
    SELECT 
        emp_id,
        year,
        salary,
        LAG(salary) OVER (PARTITION BY emp_id ORDER BY year) AS prev_salary
    FROM employee_salary_table
)
SELECT emp_id
FROM yearly_salary
GROUP BY emp_id
HAVING COUNT(*) = SUM(CASE WHEN salary > prev_salary OR prev_salary IS NULL THEN 1 ELSE 0 END);

----------------------------------------------------------------------------------------
--logins table: user_id, action_time, action (login/logout)

SELECT 
    user_id,
    CAST(action_time AS DATE) AS session_date,
    MIN(CASE WHEN action = 'login' THEN action_time END) AS first_login,
    MAX(CASE WHEN action = 'logout' THEN action_time END) AS last_logout,
    TIMESTAMPDIFF(
        MINUTE,
        MIN(CASE WHEN action = 'login' THEN action_time END),
        MAX(CASE WHEN action = 'logout' THEN action_time END)
    ) AS duration_minutes
FROM user_sessions
GROUP BY user_id, CAST(action_time AS DATE);

----------------------------------------------------------------------------------------

SELECT 
    user_id,
    CAST(action_time AS DATE) AS session_date,
    FIRST_VALUE(action_time) FILTER (WHERE action = 'login') OVER (
        PARTITION BY user_id, CAST(action_time AS DATE)
        ORDER BY action_time
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS first_login,
    LAST_VALUE(action_time) FILTER (WHERE action = 'logout') OVER (
        PARTITION BY user_id, CAST(action_time AS DATE)
        ORDER BY action_time
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_logout
FROM user_sessions;

