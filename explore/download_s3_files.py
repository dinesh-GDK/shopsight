#!/usr/bin/env python3
"""
Script to download all files from
s3://kumo-public-datasets/hm_with_images/transactions/
"""

import boto3
from botocore import UNSIGNED
from botocore.config import Config
import os
from pathlib import Path

def download_s3_files():
    bucket_name = "kumo-public-datasets"
    prefix = "hm_with_images/transactions/"
    local_dir = "hm_with_images/transactions"   # <-- updated
    
    # Create S3 client with unsigned requests for public buckets
    s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    
    # Create local directory structure
    Path(local_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # List objects with pagination
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        
        downloaded_files = 0
        
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    
                    # Skip folder markers
                    if key.endswith('/'):
                        continue
                    
                    # Compute relative file path (strip prefix)
                    relative_path = key[len(prefix):]
                    local_file_path = os.path.join(local_dir, relative_path)
                    
                    # Ensure subdirectories exist
                    Path(local_file_path).parent.mkdir(parents=True, exist_ok=True)
                    
                    # Download the file
                    print(f"Downloading: {key}")
                    s3_client.download_file(bucket_name, key, local_file_path)
                    downloaded_files += 1
        
        print(f"\nDownload complete! Downloaded {downloaded_files} files to '{local_dir}' directory.")
        
    except Exception as e:
        print(f"Error downloading files: {e}")
        return False
    
    return True

if __name__ == "__main__":
    download_s3_files()
