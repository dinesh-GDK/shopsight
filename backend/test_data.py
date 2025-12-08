"""Test script to debug data access and product search."""

import duckdb
import sys

# Connect to DuckDB
conn = duckdb.connect(':memory:')

print("=" * 60)
print("Testing DuckDB Data Access")
print("=" * 60)

# Test 1: Check articles file
print("\n1. Testing articles file...")
articles_path = "../hm_with_images/articles/*.parquet"

try:
    # First, let's see the schema
    print(f"\nSchema for {articles_path}:")
    schema_query = f"DESCRIBE SELECT * FROM read_parquet('{articles_path}') LIMIT 1"
    schema = conn.execute(schema_query).fetchall()
    for col in schema:
        print(f"  - {col[0]}: {col[1]}")

    # Count total records
    count_query = f"SELECT COUNT(*) FROM read_parquet('{articles_path}')"
    total = conn.execute(count_query).fetchone()[0]
    print(f"\nTotal articles: {total:,}")

    # Sample a few records
    print("\nSample records:")
    sample_query = f"""
    SELECT article_id, prod_name, product_type_name, department_name
    FROM read_parquet('{articles_path}')
    LIMIT 5
    """
    samples = conn.execute(sample_query).fetchall()
    for row in samples:
        print(f"  ID: {row[0]}, Name: {row[1]}, Type: {row[2]}, Dept: {row[3]}")

    # Test search with LIKE
    print("\n2. Testing search with LIKE...")
    search_terms = ["shirt", "dress", "shoe", "jacket"]
    for term in search_terms:
        search_query = f"""
        SELECT COUNT(*)
        FROM read_parquet('{articles_path}')
        WHERE LOWER(prod_name) LIKE '%{term}%'
        """
        count = conn.execute(search_query).fetchone()[0]
        print(f"  Products containing '{term}': {count}")

    # Test parameterized query (like in our code)
    print("\n3. Testing parameterized query...")
    test_query = """
    SELECT article_id, prod_name, product_type_name
    FROM read_parquet(?)
    WHERE LOWER(prod_name) LIKE ? OR LOWER(product_type_name) LIKE ?
    LIMIT 5
    """
    result = conn.execute(test_query, [articles_path, "%shirt%", "%shirt%"]).fetchall()
    print(f"  Found {len(result)} products with 'shirt':")
    for row in result:
        print(f"    ID: {row[0]}, Name: {row[1]}, Type: {row[2]}")

    print("\n✅ Data access test completed successfully!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
