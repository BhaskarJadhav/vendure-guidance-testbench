import subprocess
import sys

sql_commands = """
UPDATE product_translation SET description = description || ' Electronics' WHERE name IN ('Gaming Laptop', 'UltraWide Monitor') AND description NOT LIKE '%Electronics%';
UPDATE product_translation SET description = description || ' Appliances' WHERE name IN ('Smart Refrigerator', 'Microwave Oven') AND description NOT LIKE '%Appliances%';
UPDATE product_translation SET description = description || ' Furniture' WHERE name IN ('Ergonomic Chair', 'Standing Desk') AND description NOT LIKE '%Furniture%';
"""

print("Executing SQL description updates in PostgreSQL container...")
try:
    # We pass the SQL commands directly to psql inside the vendure-db container
    result = subprocess.run(
        ["sudo", "docker", "exec", "-i", "vendure-db", "psql", "-U", "postgres", "-d", "vendure"],
        input=sql_commands,
        capture_output=True,
        text=True,
        check=True
    )
    print("Database update output:")
    print(result.stdout)
    if result.stderr:
        print("Warnings/Errors:", result.stderr)
    print("Database successfully updated!")
except subprocess.CalledProcessError as e:
    print("Database update failed!", file=sys.stderr)
    print("Stdout:", e.stdout, file=sys.stderr)
    print("Stderr:", e.stderr, file=sys.stderr)
    sys.exit(1)
