🧩 Types of Window Functions in SQL
1. Aggregate Window Functions
These apply aggregate calculations across a defined window of rows but keep each row visible.
SUM() → Running totals
AVG() → Moving averages
COUNT() → Row counts per partition
MAX() / MIN() → Highest or lowest values in a window

Example:
sql
SELECT emp_id, department, salary,
       AVG(salary) OVER (PARTITION BY department) AS dept_avg_salary
FROM employee;
➡ Shows each employee’s salary alongside their department’s average.

2. Ranking Window Functions
Used to assign ranks or numbers to rows within partitions.
ROW_NUMBER() → Sequential numbering (no ties)
RANK() → Ranking with gaps for ties
DENSE_RANK() → Ranking without gaps for ties
PERCENT_RANK() → Relative rank as a percentage

Example:
sql
SELECT emp_id, salary,
       RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM employee;
➡ Ranks employees by salary, allowing gaps if salaries are equal.

3. Value Functions (Row-to-Row Comparisons)
These let you look at previous or next rows.
LAG() → Value from the previous row
LEAD() → Value from the next row
FIRST_VALUE() / LAST_VALUE() → First or last value in the window
------------------------------------------------------------------------------
Example:
sql
SELECT emp_id, year, salary,
       LAG(salary) OVER (PARTITION BY emp_id ORDER BY year) AS prev_salary
FROM employee_salary;
➡ Compares each year’s salary with the previous year.

4. Statistical/Distribution Functions
Used for percentiles and cumulative distributions.
NTILE(n) → Divides rows into n buckets
CUME_DIST() → Cumulative distribution (fraction of rows ≤ current row)
------------------------------------------------------------------------------
Example:
sql
SELECT emp_id, salary,
       NTILE(4) OVER (ORDER BY salary DESC) AS quartile
FROM employee;
➡ Splits employees into 4 salary quartiles.

📊 Quick Comparison Table
Category	Functions	Use Case Example
Aggregate	SUM, AVG, COUNT, MAX, MIN	Running totals, averages
Ranking	ROW_NUMBER, RANK, DENSE_RANK, PERCENT_RANK	Leaderboards, top-N queries
Value (Row-to-Row)	LAG, LEAD, FIRST_VALUE, LAST_VALUE	Compare current vs previous row
Distribution	NTILE, CUME_DIST	Percentiles, quartiles

------------------------------------------------------------------------------




