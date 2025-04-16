import csv
import sqlglot
from sqlglot.expressions import Column, Table

def load_schema_from_csv(path):
    schema = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            full_table = f"{row['table_schema'].lower()}.{row['table_name'].lower()}"
            column = row['column_name'].lower()
            schema.setdefault(full_table, set()).add(column)
    return schema

def resolve_columns_with_tables(query: str, schema_csv: str):
    schema = load_schema_from_csv(schema_csv)
    parsed = sqlglot.parse_one(query, read='tsql')

    aliases = {}
    for table in parsed.find_all(Table):
        name = table.name.lower()
        full_table_matches = [t for t in schema if t.endswith(f".{name}")]
        full_name = full_table_matches[0] if full_table_matches else name

        if table.alias:
            aliases[table.alias.lower()] = full_name
        else:
            aliases[name] = full_name

    resolved = []
    for col in parsed.find_all(Column):
        col_name = col.name.lower()
        alias = col.table.lower() if col.table else None

        if alias:
            resolved_table = aliases.get(alias, alias)
        else:
            # Search all tables for the column
            matches = [t for t, cols in schema.items() if col_name in cols]
            resolved_table = matches[0] if len(matches) == 1 else "UNKNOWN"

        resolved.append(f"{resolved_table}.{col.name}")
    return resolved
