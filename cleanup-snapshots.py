import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2')

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
    print(volume['VolumeId'])

    snapshots = ec2_client.describe_snapshots(
        OwnerIds=[
            'self',
        ],
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [
                    volume['VolumeId'],
                ]
            },
        ],
    )['Snapshots']

sorted_snapshots = sorted(snapshots, key=itemgetter('StartTime'), reverse=True)
for snapshot in sorted_snapshots[2:]:
    ec2_client.delete_snapshot(
        SnapshotId=snapshot['SnapshotId'],
    )

for snapshot in sorted_snapshots:
    print(snapshot['SnapshotId'], snapshot['StartTime'])
