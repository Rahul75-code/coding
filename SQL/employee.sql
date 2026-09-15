
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

------------------------------------------------------------------------
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
emp table - 
emp_id, name, doj
-----------------
project table -
project_id, emp_id, project_name
-----------------
salary details - 
salary_id, emp_id, salary

--get all emp who is working in more then 3 project and salary is less then 70000 
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

-----------------------
-- find employee with second highest salary in Sales department with emp name
SELECT Emp_Name, Salary
FROM (
    SELECT E.Emp_Name, E.Salary, D.Dept_Name,
           RANK() OVER (PARTITION BY D.Dept_Name ORDER BY E.Salary DESC) AS salary_rank
    FROM Employee E
    JOIN Department D ON E.Dept_No = D.Dept_No
    WHERE D.Dept_Name = 'Sales'
) AS RankedSalaries
WHERE salary_rank = 2;

--------------------------------
-- find employee with second highest salary in Sales department with emp name
SELECT E.Emp_Name, E.Salary
FROM Employee E
JOIN Department D ON E.Dept_No = D.Dept_No
WHERE D.Dept_Name = 'Sales'
ORDER BY E.Salary DESC
LIMIT 1 OFFSET 1;