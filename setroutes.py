# This script is to set the Routes

import boto3

ec2 = boto3.client('ec2', region_name='us-west-1')

rtb = ec2.create_route_table(
    VpcId='vpc-xxxxx'
)

rtbId = rtb['RouteTable']['RouteTableId']

rtbroute = ec2.create_route(
    RouteTableId=rtbId,
    GatewayId='igw-1xxxxx',
    DestinationCidrBlock='0.0.0.0/0'
)

rtbTags = ec2.create_tags(
    Resources=[rtbId],
    Tags=[
    {
    'Key': 'Name',
    'Value': 'NewTestRoute'
    },
    ]
)
