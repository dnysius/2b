import csv
import sqlglot
from sqlglot.expressions import Column

def load_schema_from_csv(csv_path):
    schema = {}
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            table = row['table_name'].lower()
            column = row['column_name'].lower()
            schema.setdefault(table, []).append(column)
    return schema

def resolve_columns_with_tables(query: str, schema_csv: str):
    schema = load_schema_from_csv(schema_csv)
    parsed = sqlglot.parse_one(query)
    parsed = parsed.analyze(schema)

    columns = []
    for col in parsed.find_all(Column):
        table = col.meta.get("table") or col.table
        columns.append(f"{table}.{col.name}")
    return columns

query = "SELECT a.col1, col2, b.col3 FROM a1 a JOIN b1 b ON a.col = b.col"
print(resolve_columns_with_tables(query, "your_schema.csv"))
