# This is a test script to spin up a VPC on Amazon Web Services
# CIDR IP Addresses will be hard coded here in the script as it is for testing purpose
# Author: Vishwa Kurakundi

import boto3
import sys
from termcolor import *

# This is a list that stores all the subnet Ids
subnets = []

# Basic information that will be displayed at the start


def nprint(msg):
        print colored(msg, 'yellow')


def readme():
    nprint("""
************ READ THIS BEFORE YOU BEGIN ************

In order to spin a VPC on AWS, you will be needing the follwing details,
before you move forward with this VPC creation. Here are the details you need:

        1. AWS Region Name (Ex. us-east-1)
        2. CIDR Address of the VPC (If you dont know how to select the CIDR range, refer documentation)
        3. Number of Subnets you want in the VPC (you can even add/delete/modify subnets later on)
        4. CIDR Address of the Subnets (If you dont know how to select the CIDR range, refer documentation)

Now that you have these information handy, go ahaed and continue.

Happy VPCing! ;-)
    """)


readme()

print colored("\nNote: DO NOT ENTER ANY DATA INCORRECTLY, THIS SCRIPT CURRENTLY DOES NOT SUPPORT FORMAT-CHECKING\n", 'magenta')

# Take Inputs at Once
vpcreg = raw_input("Enter the AWS Region you want your VPC to be in (if you are not sure, enter us-east-1): ")
cidraddr = raw_input("\n\nGreat, now enter the CIDR address of VPC: ")
vpcname = raw_input("\nAlrighty, now enter the name of VPC :")


# Ask for the region where they want to create VPC
### vpcreg = raw_input("Enter the AWS Region you want your VPC to be in (if you are not sure, enter us-east-1): ")

# Connect to EC2 in region North California (us-west-1)
ec2 = boto3.client('ec2', region_name=vpcreg)

all_az = []
# Saves the availability zones

az = ec2.describe_availability_zones()['AvailabilityZones']
for zone in az:
    all_az.append(zone['ZoneName'])


# Takes the CIDR address of VPC
### cidraddr = raw_input("\n\nGreat, now enter the CIDR address of VPC: ")

# Creates VPC with the entered CIDR
vpc = ec2.create_vpc(
    CidrBlock=cidraddr
)

# Get VPC ID which will be used to create subnets in that VPC
vpcId = vpc['Vpc']['VpcId']
# Say, VPC created successful and then print the VPC
# ID for the user (this is entirely optional)
print "\nVPC created successfully with ID :" + vpcId


# How many subnets?
no_of_sub = input("\nEnter the number of Subnets you want to create: ")
which_az = 1
# Create Subnets
for i in range(no_of_sub):
    # This is a small conditional statement that creates subnets in alternate Availability Zones
    if which_az == 1:
        sub_az = all_az[0]
        which_az = 0
    else:
        sub_az = all_az[1]
        which_az = 1

    subcidr = raw_input("\nEnter the CIDR range for Subnet(s): ")
    vpcsubnet = ec2.create_subnet(
        VpcId=vpcId,
        CidrBlock=subcidr,
        AvailabilityZone=sub_az
    )
    subId = vpcsubnet['Subnet']['SubnetId']
    subnets.append(subId)                               # Store all the Subnet IDs in list subnets

    sub_name = raw_input("\nEnter the name of this subnet :")
    subTag = ec2.create_tags(
        Resources=[subId],
        Tags=[
        {
        'Key': 'Name',
        'Value':sub_name
        },
        ]
    )
    print "Subnet created! With Subnet ID: " + subId

# Create Tags for your VPC
### vpcname = raw_input("\nAlrighty, now enter the name of VPC :")

vpctag = ec2.create_tags(
    Resources=[vpcId],
    Tags=[
    {
    'Key': 'Name',
    'Value':vpcname
    },
    ]
)

# Create Internet Gateway
igw = ec2.create_internet_gateway()
igwId = igw['InternetGateway']['InternetGatewayId']
print "\nInternet Gateway created with ID :" + igwId

# Tag Internet Gateway
igwTag = ec2.create_tags(
    Resources=[igwId],
    Tags=[
    {
    'Key':'Name',
    'Value':vpcname
    },
    ]
)

# Attach Internet Gateway to VPC
attach_igw = ec2.attach_internet_gateway(
    VpcId=vpcId,
    InternetGatewayId=igwId
)

print "\nInternet Gateway attached successfully"

# Create Route Table
rtb = ec2.create_route_table(
    VpcId=vpcId,
)

# Get Route Table ID
rtbId = rtb['RouteTable']['RouteTableId']
print "\nRoute Table created successfully with ID :" + rtbId

# Create Tags for your Route Table
rtbTag = ec2.create_tags(
    Resources=[rtbId],
    Tags=[
    {
    'Key':'Name',
    'Value':vpcname
    },
    ]
)

# Create Routes to your Internet Gateway in your Route Table

rtbroute = ec2.create_route(
    RouteTableId=rtbId,
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=igwId
)

# Associate Subnets to your Route Table
# Here we will be assigning subnets to our Route Table, which has route to IGW
# So technically, it means that all subnets are public, however, we can disable Auto-Assign IP Addresses
# to subnets to make them private. Although, it is recommended that to make a subnet completely private
# do not create any route to the internet!

for j in subnets:
    subId_rtb = j
    sub_associate = ec2.associate_route_table(
        RouteTableId=rtbId,
        SubnetId=subId_rtb
    )



# Information
print """"\nFANTASTIC! \nYour custom VPC has now been created"
\nHere are the details:"""
print "\nRegion: " + vpcreg
print "VPC Name: " + vpcname
print "VPC CIDR Address: ", cidraddr
print "Total Number of Subnet: ", no_of_sub
print "\n"
