# This script will display all the availibility zones on a region

import boto3

reg = raw_input("Enter the Region you want to connect to :")

ec2 = boto3.client('ec2', region_name=reg)

zones = ec2.describe_availability_zones()['AvailabilityZones']
az =[]

#zon = zones['AvailabilityZones']
print "The available zones are"

for i in zones:
    az.append(i['ZoneName'])

print az
