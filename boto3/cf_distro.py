import boto3
import botocore
import time

def create_oai(caller_reference):
    cloudfront_client = boto3.client('cloudfront')

    # Create OAI
    response = cloudfront_client.create_cloud_front_origin_access_identity(
        CloudFrontOriginAccessIdentityConfig={
            'CallerReference': caller_reference,
            'Comment': 'OAI for nlaws-proj CF distro'
        }
    )

    # Return OAI ID
    return response['CloudFrontOriginAccessIdentity']['Id']

def fetch_acm_certificate_arn(domain_name):
    acm_client = boto3.client('acm')
    certificates = acm_client.list_certificates()

    if certificates['CertificateSummaryList']:
        for cert in certificates['CertificateSummaryList']:
            response = acm_client.describe_certificate(CertificateArn=cert['CertificateArn'])
            subject_alternative_names = response['Certificate']['SubjectAlternativeNames']
            if domain_name in subject_alternative_names:
                return cert['CertificateArn']
        raise Exception("No ACM certificates found for the specified domain name.")
    else:
        raise Exception("No ACM certificates found.")

def fetch_s3_bucket_domain(local_file_path, s3_key):
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()

    for bucket in response['Buckets']:
        try:
            tags = s3_client.get_bucket_tagging(Bucket=bucket['Name'])
            for tag in tags['TagSet']:
                if tag['Key'] == 'project' and tag['Value'] == 'tfbd-nll':
                    domain_name = f"{bucket['Name']}.s3.amazonaws.com"
                    return domain_name
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchTagSet':
                pass
            elif e.response['Error']['Code'] == 'NoSuchBucket':
                pass
            else:
                raise

    bucket_name = input("Enter the bucket name: ")  
    s3_client.create_bucket(Bucket=bucket_name)
    s3_client.put_bucket_tagging(
        Bucket=bucket_name,
        Tagging={
            'TagSet': [
                {
                    'Key': 'project',
                    'Value': 'tfbd-nll'
                }
            ]
        }
    )
    local_file_path = '../HTML/index.html'
    s3_key = 'index.html'
    domain_name = f"{bucket_name}.s3.amazonaws.com"
   
    s3_client.upload_file(local_file_path, bucket_name, s3_key)

    return domain_name

def create_cloudfront_distribution(caller_reference, s3_bucket_domain, acm_certificate_arn, oai_id):
    cloudfront_client = boto3.client('cloudfront')

    # Define distro config
    distribution_config = {
        'CallerReference': caller_reference,
        'Comment': 'nlaws-proj CF distro',
        'DefaultRootObject': 'index.html',
        'Origins': {
            'Quantity': 1,
            'Items': [
                {
                    'Id': 'nlaws-project2-distro',
                    'DomainName': s3_bucket_domain,
                    'S3OriginConfig': {
                        'OriginAccessIdentity': f'origin-access-identity/cloudfront/{oai_id}'
                    }
                }
            ]
        },
        'ViewerCertificate': {
            'ACMCertificateArn': acm_certificate_arn,
            'SSLSupportMethod': 'sni-only',
            'MinimumProtocolVersion': 'TLSv1.2_2018'
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': 'nlaws-project2-distro',
            'ForwardedValues': {
                'QueryString': False,
                'Cookies': {
                    'Forward': 'none'
                }
            },
            'ViewerProtocolPolicy': 'redirect-to-https', 
            'MinTTL': 0,
            'AllowedMethods': {
                'Quantity': 7,
                'Items': ['HEAD', 'DELETE', 'POST', 'GET', 'OPTIONS', 'PUT', 'PATCH']
            },
            'DefaultTTL': 86400,
            'MaxTTL': 31536000,
            'Compress': True
        },
        'Enabled': True
    }

    # Create CF distro
    response = cloudfront_client.create_distribution(DistributionConfig=distribution_config)
    print("Successfully created CloudFront distribution:", response)

#run main workflow
if __name__ == "__main__":
    caller_reference = 'project-' + str(int(time.time())) 
    local_file_path = '../HTML/index.html'
    s3_key = 'index.html'
    s3_bucket_domain = fetch_s3_bucket_domain(local_file_path, s3_key)

    
    domain_name = input("Enter the domain name for the ACM certificate: ")
    
    acm_certificate_arn = fetch_acm_certificate_arn(domain_name)

    # Call function to create OAI
    oai_id = create_oai(caller_reference)

    # Call function to create CF distro
    create_cloudfront_distribution(caller_reference, s3_bucket_domain, acm_certificate_arn, oai_id)