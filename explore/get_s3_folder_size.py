#!/usr/bin/env python3
"""
Script to get the total size of s3://kumo-public-datasets/hm_with_images/
"""

import boto3
from botocore import UNSIGNED
from botocore.config import Config

def get_folder_size():
    bucket_name = "kumo-public-datasets"
    prefix = "hm_with_images/"
    
    # Create S3 client with unsigned requests for public buckets
    s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    
    try:
        # List objects with pagination
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        
        total_size = 0
        
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    total_size += obj['Size']
        
        print(format_size(total_size))
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

def format_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

if __name__ == "__main__":
    get_folder_size()