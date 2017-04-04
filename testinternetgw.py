# This is a Test Scrip to create an Internet Gateway and then try to associate it with

import boto3

ec2 = boto3.client('ec2', region_name='us-west-1')

igw = ec2.create_internet_gateway()

igwId = igw['InternetGateway']['InternetGatewayId']

igwTags = ec2.create_tags(
    Resources=[igwId],
    Tags=[
    {
    'Key': 'Name',
    'Value': 'NewTestIGW'
    },
    ]
)

print "Internet Gateway created successfully with ID :" + igwId

# This will attach the Internet Gateway to a VPC
attach_igw = ec2.attach_internet_gateway(
    VpcId = 'vpc-xxxxx',
    InternetGatewayId=igwId,
)

print "Internet Gateway attached successfully"
