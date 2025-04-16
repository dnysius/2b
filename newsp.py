import csv
import sqlglot
from sqlglot.expressions import Column, Table

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
    parsed = sqlglot.parse_one(query).analyze(schema)

    columns = []
    for col in parsed.find_all(Column):
        table = col.table or col.meta.get("table")
        columns.append(f"{table}.{col.name}")

    return columns
