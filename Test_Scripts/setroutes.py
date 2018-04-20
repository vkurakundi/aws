# This script is to set the Routes
# Made this change 

import boto3

ec2 = boto3.client('ec2', region_name='us-west-1')  # Set Region

rtb = ec2.create_route_table(
    VpcId='vpc-xxxxx'                               # Set VPC ID
)

rtbId = rtb['RouteTable']['RouteTableId']

rtbroute = ec2.create_route(
    RouteTableId=rtbId,
    GatewayId='igw-1xxxxx',                 # Set the Internet Gateway ID
    DestinationCidrBlock='0.0.0.0/0'        # Set Destination CIDR Block
)

rtbTags = ec2.create_tags(
    Resources=[rtbId],
    Tags=[
    {
    'Key': 'Name',
    'Value': 'NewTestRoute'                 # Set Route Table Route
    },
    ]
)
