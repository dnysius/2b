import sqlglot
from sqlglot import exp

# Wrap SELECT in a dummy full expression so .analyze() works
query = "SELECT a.col1, col2, b.col3 FROM a1 a JOIN b1 b ON a.col = b.col"
schema = {'a1': ['col1', 'col2', 'col'], 'b1': ['col3', 'col']}

# Create a dummy expression like SELECT ... inside a statement
parsed = sqlglot.parse_one(f"WITH x AS ({query}) SELECT * FROM x")
parsed = parsed.analyze(schema)

# Pull the inner select expression (the original query)
inner_select = parsed.args['expressions'][0].this  # WITH -> x -> SELECT

columns = []
for col in inner_select.find_all(exp.Column):
    table = col.meta.get("table") or col.table
    columns.append(f"{table}.{col.name}")

print(columns)
