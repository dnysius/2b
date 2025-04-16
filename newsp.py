import csv
import sqlglot
from sqlglot.expressions import Column, Table

def load_schema_from_csv(path):
    schema = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            table = row['table_name'].lower()
            column = row['column_name'].lower()
            schema.setdefault(table, set()).add(column)
    return schema

def resolve_columns_with_tables(query: str, schema_csv: str):
    schema = load_schema_from_csv(schema_csv)
    parsed = sqlglot.parse_one(query, read='tsql')

    aliases = {}
    for table in parsed.find_all(Table):
        real_name = table.name.lower()
        if table.alias:
            aliases[table.alias.lower()] = real_name
        else:
            aliases[real_name] = real_name

    resolved = []
    for col in parsed.find_all(Column):
        col_name = col.name.lower()
        alias = col.table.lower() if col.table else None

        if alias:
            resolved_table = aliases.get(alias, alias)
        else:
            # Search for col_name in all known tables (only one match)
            candidates = [t for t, cols in schema.items() if col_name in cols]
            resolved_table = candidates[0] if len(candidates) == 1 else "UNKNOWN"

        resolved.append(f"{resolved_table}.{col.name}")
    return resolved
query = "SELECT a.col1, col2, b.col3 FROM a1 a JOIN b1 b ON a.col = b.col"
print(resolve_columns_with_tables(query, "your_schema.csv"))
