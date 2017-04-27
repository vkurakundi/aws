import boto3

newinst = boto3.resource('ec2', region_name='us-west-1')

newinst.create_instances(ImageId='ami-165a0876', MinCount=1, MaxCount=1, InstanceType='t2.nano', SubnetId='subnet-0ae39f6e' )



