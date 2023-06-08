import boto3

client = boto3.client('eks')
clusters_name = client.list_clusters()['clusters']

for cluster_name in clusters_name:
    response = client.describe_cluster(
        name=cluster_name
    )
    cluster_info = response['cluster']
    cluster_status = cluster_info['status']
    cluster_endpoint = cluster_info['endpoint']
    cluster_version = cluster_info['version']
    print(f"EKS of {cluster_name} is {cluster_status}")
    print(f"cluster endpoint: {cluster_endpoint}")
    print(f"cluster version:{cluster_version}")
