Finding key of a table using distinct count

```sql
SELECT COUNT(DISTINCT LDKEY) / COUNT( LDKEY )
FROM MAXIMO.LONGDESCRIPTION

```
If the result is 1, each row has a unique value of the column; the column is likely a key.

Relationships



Table structure/schema


String Manipulation

REGEXP
SUBSTR
INSTR

Temporary table
```sql
DROP TABLE IF EXISTS temp.temp2;
CREATE TEMP TABLE IF NOT EXISTS temp.temp2
(id int);

INSERT INTO temp.temp2
VALUES (NULL), (2), (3), (3)
```

> [!NOTE] - Code Snippet
> ```
> CREATE TEMP TABLE IF NOT EXISTS temp.temp1
```