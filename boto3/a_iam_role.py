import boto3

iam_client = boto3.client('iam')

# List of managed policy ARNs to attach to the role
managed_policy_arns = [
    "arn:aws:iam::aws:policy/AmazonAPIGatewayAdministrator",
    "arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess",
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
    "arn:aws:iam::aws:policy/AmazonSNSFullAccess",
    "arn:aws:iam::aws:policy/AmazonSQSFullAccess",
    "arn:aws:iam::aws:policy/AWSCloudFormationFullAccess",
    "arn:aws:iam::aws:policy/AWSLambda_FullAccess",
    "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess",
    "arn:aws:iam::aws:policy/IAMFullAccess"
]

def create_iam_role(role_name, managed_policy_arns):
    try:
        # Create IAM role
        role_response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument='{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
        )

        # Attach managed policies to the role
        for policy_arn in managed_policy_arns:
            iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )

        role_arn = role_response['Role']['Arn']
        print(f"IAM role '{role_name}' with ARN '{role_arn}' and the specified managed policies has been created.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Main script execution
if __name__ == "__main__":
    role_name = input("Enter the name for the IAM role: ")

    if role_name:
        create_iam_role(role_name, managed_policy_arns)
    else:
        print("Please provide a valid IAM role name.")
