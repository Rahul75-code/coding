df2=df.withColumn("max",greatest(col1, col2) , least(col1, col2))

# to get all different values in group by use group_concat
Q>> sells table(sell_date, product), find for each date the number of different products sold and their names 

select sell_date, count(*) as num_sold, 
group_concat(product) as products,
from activities
group by 1
order by 1

##########################################################################
	# Persist the DataFrame in memory
	df.persist()
	
	# Perform some operations on the persisted DataFrame
	df_filter= df.filter(df.id =1)
	
	# Unpersist the DataFrame from memory
	df.unpersist()
	
##########################################################################

#Different level you can give:
#df.persist("MEMORY_ONLY_SER")
#df.persist("DISK_ONLY")
#df.persist("MEMORY_AND_DISK")
#df.persist("MEMORY_AND_DISK_SER")
##########################################################################

# Filter the dataframe based on multiple conditions
filtered_df = joined_df.filter((joined_df.column_name1 > 10) & (joined_df.column_name2 == 'condition'))
# Filter the dataframe based on null checks
filtered_df = joined_df.filter(joined_df.column_name.isNull())

GroupBys enable you to aggregate and summarize data based on specific columns. PySpark provides a wide range of aggregation functions like sum, count, avg, min, max, etc.

Here’s an example of how to use groupBys in PySpark:)

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

emp = [(1,"Smith",-1,"2018","10","M",3000), \
    (2,"Rose",1,"2010","20","M",4000), \
    (3,"Williams",1,"2010","10","M",1000), \
    (4,"Jones",2,"2005","10","F",2000), \
    (5,"Brown",2,"2010","40","",-1), \
      (6,"Brown",2,"2010","50","",-1) \
  ]
empColumns = ["emp_id","name","superior_emp_id","year_joined", \
       "emp_dept_id","gender","salary"]

empDF = spark.createDataFrame(data=emp, schema = empColumns)
empDF.printSchema()
empDF.show(truncate=False)


dept = [("Finance",10), \
    ("Marketing",20), \
    ("Sales",30), \
    ("IT",40) \
  ]
deptColumns = ["dept_name","dept_id"]
deptDF = spark.createDataFrame(data=dept, schema = deptColumns)
deptDF.printSchema()
deptDF.show(truncate=False)

empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"inner") \
     .show(truncate=False)

empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"outer") \
    .show(truncate=False)
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"full") \
    .show(truncate=False)
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"fullouter") \
    .show(truncate=False)

empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"left") \
    .show(truncate=False)
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"leftouter") \
   .show(truncate=False)

empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"right") \
   .show(truncate=False)
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"rightouter") \
   .show(truncate=False)

empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"leftsemi") \
   .show(truncate=False)

empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"leftanti") \
   .show(truncate=False)

empDF.alias("emp1").join(empDF.alias("emp2"), \
    col("emp1.superior_emp_id") == col("emp2.emp_id"),"inner") \
    .select(col("emp1.emp_id"),col("emp1.name"), \
      col("emp2.emp_id").alias("superior_emp_id"), \
      col("emp2.name").alias("superior_emp_name")) \
   .show(truncate=False)

empDF.createOrReplaceTempView("EMP")
deptDF.createOrReplaceTempView("DEPT")

joinDF = spark.sql("select * from EMP e, DEPT d where e.emp_dept_id == d.dept_id") \
  .show(truncate=False)

joinDF2 = spark.sql("select * from EMP e INNER JOIN DEPT d ON e.emp_dept_id == d.dept_id") \
  .show(truncate=False)
  
------------------------------------------------------------------------------------------------

from pyspark import sparkSession
from pyspark.sql import functions
from pyspark.sql import window

spark = sparkSession.builder.master('local').appName('sprk_app').getOrCreate()

data1 = {(), (), (), (), ()}

cols1 = ['sdf','tgv','bhj']

df = spark.createDataFrame(data  = data1, schema = cols1)

win = window.orderBy(col('bhj').desc())

df_with_rank = df.withColumn('rank', rank().over(win)).withColumn('dense_rank', dense_rank().over(win))

df_with_rank.show()


for item in range(10):
    if i < 5:
        'expression'
        
 com_lst = ['expression' for item in range(10) if i < 5]
 
 
 -------------------------------------------------------------------------------------##
 
 select *,
		rank() over(order by marks descs) as rnk,
		dense_rank() over (order by marks desc) as dns_rnk
 from tbl
 
 
 
 from pyspark import sparkSesson
 from pyspark.sql import functions
 from pyspark.sql.window import window
 
 spark = sparkSession.builder.master('local').appName('sparkApp').getOrCreate()
 
 data1 = {
	(1, "dsf", 95),(2, "gerg", 97),(3, "rbt", 96),(4, "tyjf", 97),((5, "eafr", 98)
 }
 
 columns = ['id', 'name', 'marks']
 
 df = spark.createDataFrame(data = data1, schema = columns)
 
 win = window.orderBy(col('marks').desc())
 
 df_with_rnk = df.withColumn('rank', rank().over(win)).withColumn('dns_rnk', dense_rank().over(win))
 
 df_with_rnk.show()  
  
  
 ------------------------------------------------------------------------------------



fdf = df1.filter((df1.col1 >5) & (df1.col2 == 'True'))


filtered_df = joined_df.filter((joined_df.column_name1 > 10) & (joined_df.column_name2 == 'condition'))



function Component() {
useEffect(() => {
//componentdidMount or componentDid update
return () => {
// componentwill Unmount
};
}, []);
}


function controllledInput () {
const [value, setValue
 = React.useSate('');
 return <input value = {value} onchange ={(e) => setValue(e.target.value)} />;
 }
 
 onChange = {(e) => setValue
 
 
 
 
 s = '3A2B1C0D5A'
 
 o/p = AAABBCAAAAA
 
 
 arr = []
 for ch in s:
     
 i=0
 while (i < len(s)) :
     arr.append(s[i+1]*int(s[i]))
     i = i+2
 print(''.join(arr))
 
 
 input -
 
 tbl1-
 col1   col2   col3
 30     null   null
 40     35     null
 50     45     38
 60     55     44
 
 output - 
 col1   col2   col3
 30     35     38
 
 SELECT
  (SELECT col1 FROM tbl1 WHERE col1 IS NOT NULL LIMIT 1) AS col1,
  (SELECT col2 FROM tbl1 WHERE col2 IS NOT NULL LIMIT 1) AS col2,
  (SELECT col3 FROM tbl1 WHERE col3 IS NOT NULL LIMIT 1) AS col3; 
  
  
  ------------------------------------------------------------------------------------
  
  create or replace snowpipe pipeName
url = s3://
table = tblName
source provide = s3
format = csv


fruit_data = 
{
  "fruit": [
    {"name": "Apple", "quantity": 1},
    {"name": "Peach", "quantity": 2},
    {"name": "Banana", "quantity": 3},
    {"name": "Orange", "quantity": 4}
  ]
}
1.Flatten the JSON array and extract the name and quantity of each fruit
2.Count the total quantity of fruits across all rows after flattening the JSON
3.Find the fruit with the highest quantity
4..List all fruits and their quantities with their index positions in the original JSON array after flattening the JSON data


df = data.json()

con = snowflake.connector.connnect(

user_name
password
database
datawarehouse
)

cur = con.cursur

cur.execute(insert)


select name, quantity from fruit_data;

select sum(quantity) from fruit_data group by name;

select max(quantity) from fruit_data;

select 
row_number() over( order by name)
,*
from fruit_data;



----------------------------------------------------
Emp
3rd highest salary


with salary as (
*,
row_number() over(order by salary desc) as row_num
from emp
)

select * from salary where row_num = 3;


-------------------------------------------------------------------------------------------



Q. Given an array of sorted numbers, find the first pair of numbers adding upto 0.
for e.g. 
input-> [-4,-3,-2,0,1,2,3,10]
output -> [-3,3]

inp = [-4,-3,-2,0,1,2,3,10]



for i in inp








mp = []
for i in inp:
	for j in mp:
		if i-j == 0:
			return [i,j]
		mp.append(i)
		
		
		
i = 0
j = -1
for i in :






str = 'dhchjedn'


ls = list()
for i in str:
	if len(ls) < 2:
		return(ls[1])
	if count(i) < 1:
		ls.append(i)
	
	
	
emp = name, id, salary, deprt, manager_id

find employees having salary higher then avg salary of department

with sal as(
select name, salary , avg(salary) as avg_sal
from emp group by deprt
)


select name salary from sal 
where salary > avg_sal
	
-------------------------------------------------------------------------------------------


empid, empname, salary, deptname
 
1,A,7000,IT
 
2,B,6000,IT
 
3,C,5000,IT
 
4,D,5000,HR
 
5,E,1200,HR
 
6,F,1999,HR
 
7,G,2000,Fin
 
8,H,5000,Fin
 
9,I,4000,Fin
 
10,J,1000,Security
 
Get the highest salary record from each department


with emp1 as ( select *,
row_number() over(partition by('deptname') order by('salary', desc)) as rownum
 from emp
 
 )
 
 select * from emp1 where rownum = 1;
 
 -----------------------------------------------------
 
 win = window.partitionby('deptname').orderby('salary', desc)
 
 df1 = emp.withColumn('rownum', rowNumber.over(win))
 
 df2 = df1.filter(df1.rownum = 1)

--------------------------------------------------------------------------

Write a Glue job to read data from S3 bronze layer - csv format 
 
Add 1 column to the df
 
Write back to staging layer - parquet format


--------------------------------------------------------

import boto3


spark = sparkseesion.builder.appname('app1').getOrCreate


s3 = boto3(s3)

path = s3://bronze
key = file1

data = s3.read(path+key)


df1 = spark.createDataFrame(data)

df_new_col = df1.withcolumn('col1')


s3.upload(df_new_col, format = 'parquet')

----------------------------------------------------------------------------------------------------------------

s = 'aaabbccabc'
# output=> "a3b2c2a1b1c1"
ls = ''
l = 0
i  =0
bet = True
while i < len(s):
    print(' ')
    print('i-',i)
    t_mx = 0
    while i < len(s) and s[i] == s[l]:
        print('s[i], s[l]- ', s[i], s[l])
        print('l,i- ', l,i)
        t = i-l+1
        print('i-l+1 - ',t)
        t_mx = max(t, t_mx)
        i +=1
        if i >= len(s):
            print('end')
            bet = False
            break
            
 
    print(' ')
    print('t_mx-',t_mx)
    ls +=s[l]
    ls +=f"{t_mx}"
    print('ls',ls)
    if bet:
        if s[i] != s[l]:
            l = i
    print('new l, new i -',l, i)
print(ls)

 
 
ls = ''
l = 0
i  =0
bet = True
while i < len(s):
    t_mx = 0
    while i < len(s) and s[i] == s[l]:
        t = i-l+1
        t_mx = max(t, t_mx)
        i +=1
        if i >= len(s):
            bet = False
            break
    ls +=s[l]
    ls +=f"{t_mx}"
    if bet:
        if s[i] != s[l]:
            l = i
print(ls)



----------------------------------------------------------------------------------------------------------------

flatten the nested list using python program 

ls = [1,[2,3,[4],5],6]
 

new_list = [x for x in ls for i in x ]

[item for sublist in lst for item in (flatten(sublist) if isinstance(sublist, list) else [sublist])]


Random string - "jjkkkaauanjkeeeeeenj" -  
write a python program to get the character and its occurrence,
that is repeated most number of times.

op = e,6
s - "jjkkkaauanjkeeeeeenj"



for i in s:

input - 
employee
emp_id, emp_name, dept, salary

3rd highest salary for each dept


with sal as(
select *,
dense_rank() over(partition by dept order by salary desc) as dns_rnk
from employee )

select * from sal 
where dns_rnk = 3





win = windows().partition('dept').orderby(salary, desc)
df1 = emp_df.with_column('dense_rank',dense_rank().over(win))
df2 = df1.filter(df1['dense_rank'] = 3)



from pyspark.sql import Window
from pyspark.sql.functions import dense_rank, desc

# Define window spec
win = Window.partitionBy('dept').orderBy(desc('salary'))

# Add dense_rank column
df1 = emp_df.withColumn('dense_rank', dense_rank().over(win))

# Filter for employees with rank 3
df2 = df1.filter(df1['dense_rank'] == 3)




emp_id, emp_name, dept, salary
 
A	B

1	1

1	1

1	2

1	3

1	1

Number of rows in output for inner, left , right and full join



inner - 15

left - 15

right - 17

full join - 5X5

----------------------------------------------------------------------------------------------------------------


s = [2,3,4,5,6,1]
 
for i in range(len(s)):

    for j in range(len(s)):

        if s[i] < s[j]:

            s[i], s[j] = s[j], s[i]

print(s)
 
n = 4
 
for i in s:

    if i == n:

        print(n)

        break
 
mx_n = 0
 
for i in range(len(s)):

    if mx_n < s[i]:

        mx_n = s[i]

print(mx_n)
 
with s as(

selct *,

dense_rank() over(partition by dept order by sal desc) as rnk

from emp

)

select id, name, sal, dept

from s where rnk = 2
 

----------------------------------------------------------------------------------------------------------------

 

Customers
Customer 		ID	Name	Age	City
1	John Smith	25	New York
2	Jane Doe	30	Chicago
3	Bob Brown	35	Los Angeles
4Alice Johnson	20	New York
5	Mike Davis	40	Chicago
6	Emily Taylor	 Los Angeles
7	David Lee	28	New York
8	Sarah Kim	32	Chicago
9	Kevin White	38	Los Angeles
10	 			45	New York
 
 
 df['Age'].fillna(18)
 df.dropna(how = 'y')
 df.filter(df.Name = 'John Smith')
 df['Name'].isin('John Smith')
 
 
 Orders
 
Order ID	Customer ID	Order Date	Total
101				1	2022-01-01	100.0
102				1	2022-01-15	200.0
103				2	2022-02-01	50.0
104				3	2022-03-01	150.0
105				4	2022-04-01	250.0
106				5	2022-05-01	300.0
107				6	2022-06-01	 
108				7	2022-07-01	400.0
109				8	2022-08-01	500.0
110				9	2022-09-01	600.0



Customers.join(Orders, on ='Customer ID' how ='inner join' )

df.groupbykey()


df.groupby()

df = df1.join(df2, df1.col = df2.col, 'left')

spark = sparkSession.builder.appname('app1').getOrCreate()


tbl - emp

col - id , name, dept, sal

2nd higest sal


with s as (
select *,
dense_rank() over(partition by dept order by sal desc) as rnk
from emp
)

select id , name, dept, sal
from s where rnk = 2



win = window.partitionBy('dept').orderBy(desc('sal'))

df = emp.withColumn('dense_rank', dense_rank().over(win))

df2 = df1.filter(df1['dense_rank'] == 2)




-----------------------------------------------------------------------------



with f.open('file1','r') as data1
data.isin('rahul')


search the element in file using pyspark

emp

ID	NAME	SALARY
1	DEV		20000
1	DEV		20000
2	SCOTT	10000
4	DAVID	5000
4	DAVID	5000
1	DEV		20000
1	DEV		20000
4	DAVID	5000
 
 
select ID, NAME, SALARY
from emp 
 
 
read()

group_by()

re-partition()

count()

 
 
apply, map and applymap
 
piping in pyspark
 
dataware house, datalake, delta lake
 

 ------------------------------------------------------------------
 
 CITY	,YEAR,	TEMP
Banglore,2020,35
Chennai, 2020,31
Mumbai,  2020,32
Chennai, 2021,26
Hyderabad,2021,32
Mumbai,  2021,31
 
Records which are having highest temp in each year
----------------------------------------------
Expected Output:
---------------------
CITY,YEAR,TEMP
Banglore,2020,35
Hyderabad,2021,32


with t as (
select *,
row_number() over(partition by YEAR order by TEMP desc ) as row_nm
from temp
)

select * 
from t where row_nm = 1;



win = window.partitionby('YEAR').orderby(desc(TEMP))

df1 = temp.withColumn('row_nm', rownumber().over(win))

df2 = df1.filter(df1['row_nm'] == 1)



s = 'vduhdbdd'

op = d

map_s = {}
for i in s:
    if i in map_s:
        map_s[i] +=1
    else:
        map_s[i] = 1

vals = list(map_s.values())
mx_val = max(vals)
idx_val = vals.index(mx_val)
mx_key = list(map_s.keys())[idx_val]
print(mx_key)

---------------------------------------------------------------------------------



Questions: Write a pyspark code to get names of only passed students. Passing mark is 40.
CSV : student_marks
Columns:
Name, subject, marks
 
EX:
Ram, Math, 80
Ram, Science, 70
Ram , Biology, 30
Prasad, Math, 67
Prasad, Science, 48
Prasad, Biologgy, 78
 
Expected Output:
Prasad


std_df= spark.read.csv('student_marks')

pass_df = std_df.filter(std_df['marks'] >= 40)

pass_df.filter(pass_df[''])


---------------------------------------




select Name
from student_marks
groupby Name 
having count(Name) = 3 and marks >= 40;


-----------------------------------------------------------------



Write Python code to find the longest consecutive sequence of numbers.
i/p: list1 = [1,4,2,6,3,4,5, 8,6,7,8,9]
o/p: [6,7,8,9], length = 4


ls = []
n = 0
while i < len(list1):
    while n2 == list1[i+1]:
        n = list1[i]
        n2 +=1
        ls.append(list1[i+1])
        i +=1
         
    ls = 
    
    
    
    
map_n = {}
for i in list1:
    if i in map_n:
        map_n[i] += 1
    else:
        map_n[i] = 1
    
mx_val = max(list(map_n.values()))

idx_val = list(map_n.values()).index(mx_val)
mx_key = list(map_n.keys())[idx_val]
 


----------------------------------------------------------



fls = [1, 2, [3, 4], 5, 6]

ls1 = [i for sublist in fls for i in sublist]

print(ls1)


dict1 =
{
	    "abc" : "oihcioec",
	    "gfd" : {
	        "abc": "1257gs6",
	        "jnh":"oiwhow"
	    },
	    "hnb" : {
	        "gbv":"jhz",
	        "abc":"jxiwox"
	    }
	}

def getCnt():
	cnt = 0
	for i, j in dict1.items:
		if i == 'abc':
			cnt +=1
		if isinstance(j, dictionary):
			getCnt()
	return cnt
	
	


i/p:
id
1
2
3
 
o/p:
id
1
2
2
3
3
3


select *
from tbl as t1 self join tbl as t2 
on t1.id >= t2.id



with s as (
select *,
dense_rank() over(partition by dept order by salary desc) as rnk
from emp
)

select id , salary, dept from s 
where rnk = 3


emp_df

win = window.partitionby('dept').orderby(col('salary').desc())

rnk_df = emp_df.withColumn('rank', dense_rank().over(win))

df = rnk_df.filter(rnk_df['rank'] == 3)

df.show()

---------------------------------------------------------------------------------

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
------------------------------------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.getOrCreate()

# Sample data
data = [
    (10, "maths", 60),
    (10, "english", 70),
    (10, "science", 80),
    (10, "hindi", 90),
    (20, "english", 60),
    (20, "science", 70),
    (20, "hindi", 80)
]

columns = ["roll_no", "subject", "marks"]

student_df = spark.createDataFrame(data, columns)

# Pivot the table
pivot_df = (
    student_df
    .groupBy("roll_no")
    .pivot("subject", ["maths", "english", "science", "hindi"])
    .max("marks")
)

pivot_df.show()

---------------------------------------------------------------------------------