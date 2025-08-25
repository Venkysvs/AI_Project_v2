import boto3

def list_subnets(region):
    ec2 = boto3.client("ec2", region_name=region)
    resp = ec2.describe_subnets()
    subnets = []
    for s in resp["Subnets"]:
        name = None
        for t in s.get("Tags", []):
            if t["Key"] == "Name":
                name = t["Value"]
        subnets.append({
            "id": s["SubnetId"],
            "name": name or "Unnamed"
        })
    return subnets

def list_security_groups(region):
    ec2 = boto3.client("ec2", region_name=region)
    resp = ec2.describe_security_groups()
    sgs = []
    for sg in resp["SecurityGroups"]:
        sgs.append({
            "id": sg["GroupId"],
            "name": sg.get("GroupName", "Unnamed")
        })
    return sgs

def list_key_pairs(region):
    ec2 = boto3.client("ec2", region_name=region)
    resp = ec2.describe_key_pairs()
    keys = []
    for k in resp["KeyPairs"]:
        keys.append({"name": k["KeyName"]})
    return keys

def list_instances(region, state_filter=None):
    ec2 = boto3.client("ec2", region_name=region)
    filters = []
    if state_filter in ["running", "stopped"]:
        filters = [{"Name": "instance-state-name", "Values": [state_filter]}]
    elif state_filter == "all":
        filters = [{"Name": "instance-state-name", "Values": ["running", "stopped"]}]

    resp = ec2.describe_instances(Filters=filters)
    instances = []
    for r in resp["Reservations"]:
        for inst in r["Instances"]:
            name = None
            for t in inst.get("Tags", []):
                if t["Key"] == "Name":
                    name = t["Value"]
            instances.append({
                "id": inst["InstanceId"],
                "state": inst["State"]["Name"],
                "name": name or "Unnamed"
            })
    return instances
