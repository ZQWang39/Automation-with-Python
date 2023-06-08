import boto3
import schedule
import time

ec2_client = boto3.client('ec2', region_name="ap-southeast-2")
ec2_resource = boto3.resource('ec2', region_name="ap-southeast-2")


# reservations = ec2_client.describe_instances()
# print(reservations["Reservations"])
#
# for reservation in reservations["Reservations"]:
#     Instances = (reservation["Instances"])
#     for instance in Instances:
#         print(f"Instance {instance['InstanceId']} is currently {instance['State']['Name']}.")
def check_instance_status():
    instanceStatuses = ec2_client.describe_instance_status(
        IncludeAllInstances = True
    )
    # print(instanceStatuses["InstanceStatuses"])
    for instanceStatus in instanceStatuses["InstanceStatuses"]:
        # print(instanceStatus["InstanceId"])
        # print(instanceStatus["InstanceState"]["Name"])
        Inst_Status = instanceStatus['InstanceStatus']['Status']
        Sys_Status = instanceStatus['SystemStatus']['Status']
        # systemStatuses = instanceStatus["SystemStatus"]["Details"]
        # for systemStatus in systemStatuses:
            # print(systemStatus["Status"])
        print(f"Instance {instanceStatus['InstanceId']} is {instanceStatus['InstanceState']['Name']} and the instance status is {Inst_Status}, system status is {Sys_Status}.")

schedule.every(5).seconds.do(check_instance_status)
while True:
    schedule.run_pending()
    # time.sleep(5)