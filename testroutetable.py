# This is a test script to create a Route Table for a specific VPC
# Author: Vishwa Kurakundi

import boto3

ec2 = boto3.client('ec2', region_name='us-west-1')

routetable = ec2.create_route_table(
    VpcId='vpc-xxxx'
)

rtid = routetable['RouteTable']['RouteTableId']

print "Route Table created successfully with ID: :" + rtid

# Create Tags for your Route Table
rtbtags = ec2.create_tags(
    Resources=[rtid],
    Tags = [
    {
    'Key': 'Name',
    'Value': 'NewTestRoute'
    },
    ]
)
