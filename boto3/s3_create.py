import boto3

region = input("Enter the region: ")

s3 = boto3.client('s3', region_name=region)

bucket_name = input("Enter the bucket name: ")

s3.create_bucket(Bucket=bucket_name)
print(f"Bucket '{bucket_name}' created successfully.")

tags = {
    'TagSet': [
        {
            'Key': 'project',
            'Value': 'tfbd-nll'
        }
    ]
}

s3.put_bucket_tagging(
    Bucket=bucket_name,
    Tagging=tags
)
print(f"Tag added to bucket '{bucket_name}' successfully.")

local_file_path = '../HTML/index.html'
s3_key = 'index.html'

s3.upload_file(local_file_path, bucket_name, s3_key)
print(f"File '{local_file_path}' uploaded to '{bucket_name}' as '{s3_key}' successfully.")
