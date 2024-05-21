import boto3
import argparse

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

        print(f"IAM role '{role_name}' with the specified managed policies has been created.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Ensure that specific code only executes when the script is run directly, allowing for modular and reusable code
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create IAM role with specified managed policies")
    parser.add_argument("--auto-role-name", action="store_true", help="Automatically generate a role name")
    parser.add_argument("--role-name", help="The name of the IAM role to create")
    args = parser.parse_args()

    if args.auto_role_name:
        role_name = input("Enter a name for the IAM role: ")
    else:
        role_name = args.role_name

    if role_name:
        create_iam_role(role_name, managed_policy_arns)
    else:
        print("Please provide a valid IAM role name.")
