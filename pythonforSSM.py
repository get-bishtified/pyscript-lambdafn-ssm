#Install and Configure Apache HTTP Server on an Existing EC2 via Lambda + Secrets Manager + SSM

import boto3
import json

REGION = "ap-south-1"
INSTANCE_ID = "i-***********"  # Replace with your EC2 instance ID
SECRET_NAME = "secretname"

# AWS Clients
ssm = boto3.client('ssm', region_name=REGION)
secretsmanager = boto3.client('secretsmanager', region_name=REGION)

def lambda_handler(event, context):
    # Step 1: Fetch the secret
    try:
        secret_response = secretsmanager.get_secret_value(SecretId=SECRET_NAME)
        secret = json.loads(secret_response['SecretString'])

        site_title = secret.get("SiteTitle", "Default Site")
        contact_me = secret.get("ContactMe", "#")

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Failed to fetch secret: {str(e)}"
        }

    # Step 2: Apache install & HTML generation
    commands = [
        "#!/bin/bash",
        "yum update -y",  # For Amazon Linux. Use apt-get for Ubuntu
        "yum install -y httpd",
        "systemctl start httpd",
        "systemctl enable httpd",
        "mkdir -p /var/www/html",
        f"echo '<html><head><title>{site_title}</title></head>' > /var/www/html/index.html",
        f"echo '<body><h1>{site_title}</h1><p><a href=\"{contact_me}\">Contact Me</a></p></body>' >> /var/www/html/index.html",
        "echo '</html>' >> /var/www/html/index.html",
        "systemctl restart httpd"
    ]

    # Step 3: Send SSM command to EC2
    try:
        ssm.send_command(
            InstanceIds=[INSTANCE_ID],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': commands},
            TimeoutSeconds=60,
            Comment="Install Apache and set homepage using Secrets Manager"
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Failed to send SSM command: {str(e)}"
        }

    return {
        'statusCode': 200,
        'body': f"Apache install and homepage configured on EC2 instance {INSTANCE_ID}."
    }