
--SCD Type 1
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

----------------------------------------------------------------------------------------------------------
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

--------------------------------------------------------------------------
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