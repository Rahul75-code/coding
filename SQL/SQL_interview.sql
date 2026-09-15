
find the max sale from the order table from each category in new column
----------------------------------------------------------------------------------------
--masking dob and mobile number in sql
SELECT 
    CONCAT(SUBSTRING(dob, 1, 4), '-XX-XX') AS dob_masked,
    CONCAT('XXXXXX', RIGHT(mobile, 4)) AS mobile_masked
FROM my_table;

----------------------------------------------------------------------------------------
--find Cumulative or running total of sales using window function, in sql
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
---------------------------------------------------
✅ Moving Sum
Sum of last N rows only.
SUM(value) OVER (
    ORDER BY id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
-------------------------------------------------------------------------------------------------------


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

----------------------------------------------------------------------------------------------

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

----------------------------------------------------------
table a	  table b
------- ----- ----------------
name		 name
------- ----- ----------------
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
----------------------------------------------------------------------------

 -- employees who joined in the last 30 days from the employee table
SELECT emp_id, emp_name, join_date
FROM employee
WHERE join_date >= CURRENT_DATE - INTERVAL '30 DAYS';


------------------------------------------------------------------------
--Q>> find duplicate ID ?
select emp_id, count(emp_id) as cnt 
from employees
group by emp_id
having cnt >= 2

-----------------------------------------------------------------------
-- 3.Find employees with salary greater than their departmental average.
EMP_ID DEPT_NBR 	SAL
101     50    	  2000
102     50       	2200
103     50 			  2400
104     60 			  3000
105     60 			  2000
106     70 			  1000
107     70 			  2000

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
--Write a SQL query to print only the names of students who passed all subjects.
 
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
from student_marks
group BY name
having min(mark) >= 40

or

SELECT Name
FROM student_marks
GROUP BY Name
HAVING COUNT(CASE WHEN Mark >= 40 THEN 1 END) = COUNT(Subject);

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
		        10		    60				    70				       80		    	90
		        20						          60				       70		    	80
		
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

SELECT emp_id, emp_name,  EXTRACT(YEAR FROM expense_date) AS year_expense,
           SUM(expense_amt) AS total_expense
    FROM expense
    GROUP BY emp_id, emp_name,  EXTRACT(YEAR FROM expense_date) AS year_expense

-- last expense each year for each emp
SELECT emp_id,
       EXTRACT(YEAR FROM expense_date) AS years,
       MAX(expense_date) AS last_expense
FROM expense
WHERE EXTRACT(YEAR FROM expense_date) IN (2023, 2024, 2025)
GROUP BY emp_id, EXTRACT(YEAR FROM expense_date);
--or-----
-- my sql db
SELECT 
    emp_id,
    YEAR(expense_date) AS years,
    SUM(expense_amt) AS total_expense
FROM expense
WHERE YEAR(expense_date) IN (2023, 2024, 2025)
GROUP BY emp_id, YEAR(expense_date);

------------------------------------------------------------------------

cust_id, entry_date 
1			    13/5
1			    20/5
1			    30/5
--find the  maximum entry_date for each a customer 
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
--write a sql query for the above output. sql query to fix match with each other team
-------------------------
SELECT t1.team AS TeamA,
       t2.team AS TeamB
FROM team t1
JOIN team t2
  ON t1.team < t2.team
ORDER BY TeamA, TeamB;

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

----------------------------------------------------------------------------

-- from order table (customer_id, order_id, order_date, amount), 
--Retrieve each customer’s most recent order.
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

-- explained in SQL_theory.sql
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

---------------------------------------------------------------------------
--given a sales table with columns cust_id, order_date, and amount,
--write a query to find customer who have placed orders in three consecutive months.

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
--🔍 Explanation:
--We join the sales table to itself three times for the same customer.
--We check if the second and third orders occurred in the next two consecutive months after the first.
--DATE_TRUNC('month', order_date) ensures we’re comparing by month only (ignoring day).
--INTERVAL '1 month' and '2 month' help identify consecutive months.

---------------------------------------------------------------------------

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


---------------------------------------------------------------------------------------

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

------------------------------------------------------------------------

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
    EXTRACT(EPOCH FROM (  first_login - last_login    )) / 3600.0  AS duration_hours
FROM user_sessions
GROUP BY user_id, CAST(action_time AS DATE);

----------------------------------------------------------------------------------------


