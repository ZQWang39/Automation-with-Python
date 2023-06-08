import boto3
import schedule

ec2_client = boto3.client('ec2')


def create_snapshots():
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    'Prod',
                ]
            },
        ],
    )['Volumes']
    for volume in volumes:
        snap_shot = ec2_client.create_snapshot(
            VolumeId=volume['VolumeId'],
        )
        print(snap_shot)


schedule.every(3).seconds.do(create_snapshots)
while True:
    schedule.run_pending()