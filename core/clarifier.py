from services.aws_helpers import list_subnets, list_security_groups, list_key_pairs

REQUIRED_FIELDS = {
    "ec2": {
        "create": ["Provider", "Region", "InstanceType", "OS", "SubnetId", "SecurityGroupId", "KeyName", "Name"],
        "list":   ["Provider", "Region"],
        "delete": ["Provider", "Region", "InstanceId"]
    },
}

QUESTIONS = {
    "Provider":         "🌐 Which cloud provider do you want? (AWS / Azure / GCP)",
    "Region":           "📍 Which region should I use? (e.g., us-east-1, us-west-2)",
    "InstanceType":     "⚙️ Which VM size do you want? (e.g., t3.micro, m5.large)",
    "OS":               "💿 Which operating system would you like? (Amazon Linux / Ubuntu / Windows)",
    "SubnetId":         "🌐 Which subnet should I use?",
    "SecurityGroupId":  "🔒 Which security group should I attach?",
    "KeyName":          "🔑 Which key pair should I use for SSH access?",
    "Name":             "📝 What name should I assign to this instance?"
}

def needs_clarification(service, params, intent):
    required = REQUIRED_FIELDS.get(service, {}).get(intent, [])
    for field in required:
        if not params.get(field):
            return field
    return None

def resolve_resources(params):
    """
    Resolve user-friendly inputs (like 'default') into IDs for AWS.
    """
    region = params.get("Region")
    if not region:
        return params

    # Resolve Subnet by label
    if params.get("SubnetId"):
        subnets = list_subnets(region)
        for label, sid in subnets.items():
            if params["SubnetId"].lower() in label.lower() or params["SubnetId"] == sid:
                params["SubnetId"] = sid
                break

    # Resolve Security Group by name or ID
    if params.get("SecurityGroupId"):
        sgs = list_security_groups(region)
        for label, sgid in sgs.items():
            if params["SecurityGroupId"].lower() in label.lower() or params["SecurityGroupId"] == sgid:
                params["SecurityGroupId"] = sgid
                break

    return params
