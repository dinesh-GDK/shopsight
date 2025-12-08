"""Direct test of the search API without running the server."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.duckdb_client import DuckDBClient
from app.services.product_search import ProductSearchService
from app.config import settings

print("=" * 60)
print("Testing Product Search Service")
print("=" * 60)

# Print configuration
print(f"\nConfiguration:")
print(f"  ARTICLES_PATH: {settings.ARTICLES_PATH}")
print(f"  LOG_LEVEL: {settings.LOG_LEVEL}")

# Initialize database
print("\n1. Initializing DuckDB client...")
db = DuckDBClient()
print(f"  ✓ DB connected: {db.is_connected()}")

# Initialize service
print("\n2. Initializing Product Search Service...")
service = ProductSearchService(db)
print("  ✓ Service initialized")

# Test searches
test_cases = [
    (["shirt"], {}),
    (["dress"], {}),
    (["Nike"], {}),
    (["shoe"], {}),
]

print("\n3. Running test searches...")
for keywords, filters in test_cases:
    print(f"\n  Testing: keywords={keywords}, filters={filters}")
    try:
        products = service.search(keywords=keywords, filters=filters, limit=5)
        print(f"  ✓ Found {len(products)} products")
        if products:
            for p in products[:3]:
                print(f"    - {p.article_id}: {p.name} ({p.type})")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 60)
