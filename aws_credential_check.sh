#!/bin/bash
echo "Checking AWS CLI installation..."
if ! command -v aws &> /dev/null
then
    echo "AWS CLI could not be found. Please install it first."
    exit 1
fi

echo "Checking AWS CLI credentials configuration..."
aws sts get-caller-identity
if [ $? -ne 0 ]; then
    echo "AWS CLI credentials not properly configured or invalid."
else
    echo "AWS CLI credentials are configured properly."
fi

echo "Checking environment variables..."
echo "AWS_ACCESS_KEY_ID   = $AWS_ACCESS_KEY_ID"
echo "AWS_SECRET_ACCESS_KEY = $(if [ -z \"$AWS_SECRET_ACCESS_KEY\" ]; then echo 'Not Set'; else echo '****'; fi)"
echo "AWS_REGION = $AWS_REGION"

echo "You can also verify credentials configuration inside your Docker container by running:"
echo "docker exec -it <container_name_or_id> bash"
echo "and then manually running"
echo "aws sts get-caller-identity"
echo "or checking environment variables inside the container."
