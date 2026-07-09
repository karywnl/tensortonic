## The SELECT Statement

The `SELECT` statement is the most fundamental SQL command - it retrieves data from one or more tables.

### Selecting Specific Columns

Instead of grabbing everything with `SELECT *`, you list only the columns you need:

```sql
SELECT column1, column2 FROM table_name;
```

This is preferred in production code because it makes queries faster (less data transferred) and your intent explicit.

### Column Aliases with AS

The `AS` keyword renames a column in the output. The underlying table is unchanged - aliases only affect what the result set calls each column:

```sql
SELECT first_name AS name FROM employees;
```

The alias can be any valid identifier. If it contains spaces or special characters, wrap it in double quotes: `AS "Full Name"`.

### Computed Columns

SQL lets you write expressions directly in the SELECT list. Arithmetic operators (`+`, `-`, `*`, `/`) work on numeric columns:

```sql
SELECT price, quantity, price * quantity AS total FROM orders;
```

The database evaluates the expression for every row and returns the result as a new column. The computed column only exists in the output - it is not stored in the table.

### FROM Clause

`FROM` tells the database which table to read. Every SELECT that queries a table needs a FROM:

```sql
SELECT col1, col2 FROM my_table;
```

### Execution Order

SQL processes clauses in this order: `FROM` (find the table) then `SELECT` (pick and compute columns). This matters later when you add WHERE, GROUP BY, and ORDER BY.
