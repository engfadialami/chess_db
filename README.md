
# Session 6 Learning Notes and Difficulties

## Main Difficulty

The biggest challenge was understanding the difference between:

- CSV files
- pandas DataFrames
- SQLite databases
- SQL language

Initially these concepts appeared to be the same thing.

### Final Understanding

CSV:
- Simple file on disk.

DataFrame:
- Temporary table loaded into RAM by pandas.

SQLite:
- Database engine storing multiple related tables in a .db file.

SQL:
- Language used to query the database.

Workflow:

CSV -> DataFrame -> SQLite Database -> SQL Query -> DataFrame

---

## Confusion About groupby()

Initially there was confusion between:

```python
groupby()
```

and

```python
sort_values()
```

Final understanding:

sort_values():
- Reorders rows.

groupby():
- Creates logical groups then performs calculations.

Example:

```python
df.groupby("winner")["turns"].mean()
```

creates one result per winner.

---

## Confusion About SQL GROUP BY

The concept became clearer after understanding:

1. SQLite creates groups.
2. COUNT, AVG, MAX, etc. run inside each group.
3. The result contains one row per group.

---

## Confusion About SQL Execution Order

SQL is written:

SELECT -> FROM -> GROUP BY

but executed approximately:

FROM -> GROUP BY -> SELECT

This explained why:

COUNT(*)

inside GROUP BY is different from:

SELECT COUNT(*) FROM games

inside a subquery.

---

## Confusion About CTE

CTE (WITH) was initially unclear.

Final understanding:

A CTE behaves like a temporary DataFrame or temporary variable.

```sql
WITH white_wins AS (...)
```

creates a temporary table that exists only during the query.

---

## Confusion About JOIN

The meaning of:

```sql
ON p.username = g.white_id
```

was initially unclear.

Final understanding:

The ON clause defines how rows from two tables match.

Equivalent idea:

```python
pd.merge(...)
```

---

## Confusion About map()

map() was difficult because it behaves like a dictionary lookup.

Final understanding:

```python
df["salary"] = df["name"].map(dictionary)
```

is very similar to Excel VLOOKUP.

---

## Database Design Lessons

The database was normalized into:

- players
- openings
- games

Reasons:

- Reduce repeated information.
- Create relationships using keys.
- Improve data integrity.

---

## New Concepts Learned

Pandas:
- concat()
- groupby()
- last()
- reset_index()
- value_counts()
- add()
- map()
- astype()

SQL:
- SELECT
- COUNT
- AVG
- MAX
- GROUP BY
- ORDER BY
- LIMIT
- HAVING
- JOIN
- LEFT JOIN
- UNION ALL
- CTE
- RANK
- PARTITION BY
- LAG
- EXPLAIN QUERY PLAN
