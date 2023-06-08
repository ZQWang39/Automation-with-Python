import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name="ap-southeast-2")
ec2_resource = boto3.resource('ec2', region_name="ap-southeast-2")

reservations = ec2_client.describe_instances()['Reservations']
instance_ids = []
for reservation in reservations:
    instances = reservation['Instances']
    for instance in instances:
        instance_ids.append(instance["InstanceId"])
print(instance_ids)

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': instance_ids
        },
    ],
)['Volumes']

volume_ids = []
for volume in volumes:
    volume_ids.append(volume['VolumeId'])

snapshots = ec2_client.describe_snapshots(
    Filters=[
        {
            'Name': 'volume-id',
            'Values': volume_ids
        },
    ],
    OwnerIds=[
        'self',
    ],
)['Snapshots']
sorted_snapshots = sorted(snapshots, key=itemgetter('StartTime'), reverse=True)
latest_snapshot = sorted_snapshots[0]
latest_snapshot_id = latest_snapshot['SnapshotId']

new_volume = ec2_client.create_volume(
    AvailabilityZone='ap-southeast-2c',
    SnapshotId=latest_snapshot_id,
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'Prod'
                },
            ]
        },
    ],
)
print(new_volume['VolumeId'])
while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    print(vol.state)
    volume_statue = vol.state
    if volume_statue == 'available':
        instance = ec2_resource.Instance(instance_ids[1])
        instance.attach_volume(
            Device='/dev/xvdar',
            VolumeId=new_volume['VolumeId']
        )
        break
