Instructions
1. The dataset explanation is given below
2. Follow software engineering best practices
3. Plan product search → past sales chart using the dataset user jouney
    Come up with a steup by step plane (export to plan.md)

Dataset

The articles(hm_with_images/articles/part-00000-63ea08b0-f43e-48ff-83ad-d1b7212d7840-c000.snappy.parquet) contains product catalog information with 105,542 articles including:
- Product details (name, type, group)
- Visual attributes (color, appearance)
- Organizational data (department, section, garment group)
- Image URLs

The customers parquet file(hm_with_images/customers/part-00000-9b749c0f-095a-448e-b555-cbfb0bb7a01c-c000.snappy.parquet) contains customer demographic and profile information with 1,371,980 customers including:
  - Customer identifiers (hashed customer_id)
  - Demographics (age, postal_code)
  - Membership info (club_member_status)
  - Marketing preferences (fashion_news_frequency, Active, FN flags)

The transactions parquet files (hm_with_images/transactions/*.parquet) contains historical sales data with:

  Time Period: September 20, 2018 to September 22, 2020 (approximately 2
  years, 733 days)

  Sales Data Includes:
  - t_dat: Transaction date
  - article_id: Product identifier (links to articles file)
  - customer_id: Customer identifier (links to customers file)
  - price: Sale price (appears normalized)
  - sales_channel_id: Channel where sale occurred
  - transaction_id: Unique transaction identifier
  - analysis_column_30 and analysis_column_90: Additional analysis fields

  Volume:
  - 476,039 total transactions
  - 20,317 unique customers
  - 58,360 unique articles sold
  - 734 unique transaction dates (nearly daily data)

  This is the historical sales dataset you were looking for. It can be
  joined with the articles file (product catalog) and customers file
  (customer profiles) using the respective IDs to create a complete view of
  sales history with product details and customer demographics.

 Data Range: September 20, 2018 to September 22, 2020

  Key Statistics:
  - Total period: 734 days (approximately 2 years)
  - Total transactions: 31,788,324 (31.8 million transactions)
  - Total files: 68 partitioned parquet files
  - Average transactions per file: ~467,000

  All 68 partition files contain transactions spanning the same complete
  date range (2018-09-20 to 2020-09-22), meaning the data is partitioned by
  customer or some other dimension rather than by date.

  This is a substantial historical sales dataset covering 2 full years of
  transaction history.

The data is partitioned by CUSTOMER_ID. Here's what I found:

  Partitioning Strategy:
  - Each partition file contains transactions for a unique set of customers
  - There is zero customer overlap between files (File 0 & 1: 0 shared
  customers, File 0 & 67: 0 shared customers)
  - However, the same articles appear across multiple files (47,368 shared
  articles between files 0 & 1)

  What this means:
  - All transactions for a given customer are in the same partition file
  - Customers are distributed across the 68 files (likely using hash-based
  distribution on customer_id)
  - Each file has ~15,000-20,000 unique customers
  - The file names themselves don't reveal this - it's a standard Spark hash
   partitioning pattern

  Why partition this way:
  - Customer-level analytics are more efficient (all customer data is
  co-located)
  - Enables parallel processing by customer
  - Common pattern for customer segmentation, recommendation systems, and
  personalization tasks

  This is why all files have the same date range (2018-09-20 to 2020-09-22)
  - each file contains the complete transaction history for its subset of
  customers.
