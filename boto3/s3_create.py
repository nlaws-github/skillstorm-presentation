import boto3

region = input("Enter the region: ")

s3 = boto3.client('s3', region_name=region)

bucket_name = input("Enter the bucket name: ")

s3.create_bucket(Bucket=bucket_name)

print(f"Bucket '{bucket_name}' created successfully.")

# Specify the local file path and desired S3 key
local_file_path = '../HTML/index.html'
s3_key = 'index.html'

# Upload the file to the S3 bucket
s3.upload_file(local_file_path, bucket_name, s3_key)

print(f"File '{local_file_path}' uploaded to '{bucket_name}' as '{s3_key}' successfully.")
