import pandas as pd

# file_name = "/home/dinesh/shopsight/hm_with_images/articles/part-00000-63ea08b0-f43e-48ff-83ad-d1b7212d7840-c000.snappy.parquet"
file_name = "/home/dinesh/shopsight/hm_with_images/customers/part-00000-9b749c0f-095a-448e-b555-cbfb0bb7a01c-c000.snappy.parquet"

df = pd.read_parquet(file_name)

print(df.head())          # preview rows
print(df.info())          # schema + types
print(df.describe())      # stats (numeric)
print(df.columns)         # column names