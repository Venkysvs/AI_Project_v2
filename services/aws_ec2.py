import boto3
from services.aws_helpers import list_subnets, list_security_groups, list_key_pairs


def get_latest_ami(region, os_choice):
    """Dynamically fetch the latest AMI for a given OS and region"""
    ec2 = boto3.client("ec2", region_name=region)

    if os_choice.lower() == "amazon linux":
        filters = [{"Name": "name", "Values": ["amzn2-ami-hvm-*-x86_64-gp2"]}]
        owners = ["amazon"]
    elif os_choice.lower() == "ubuntu":
        filters = [{"Name": "name", "Values": ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]}]
        owners = ["099720109477"]  # Canonical
    elif os_choice.lower() == "windows":
        filters = [{"Name": "name", "Values": ["Windows_Server-2019-English-Full-Base-*"]}]
        owners = ["amazon"]
    else:
        raise ValueError(f"Unsupported OS: {os_choice}")

    images = ec2.describe_images(Owners=owners, Filters=filters)
    if not images["Images"]:
        raise RuntimeError(f"No AMIs found for {os_choice} in {region}")

    # Pick latest
    latest = sorted(images["Images"], key=lambda x: x["CreationDate"], reverse=True)[0]
    return latest["ImageId"]


class AWSVMService:
    def create_vm(self, params):
        region = params.get("Region") or input("🤖 📍 Which region should I use? (e.g., us-east-1, us-west-2): ")
        instance_type = params.get("InstanceType") or input("🤖 ⚙️ Which VM size do you want? (e.g., t3.micro, m5.large): ")
        os_choice = params.get("OS") or input("🤖 💿 Which operating system would you like? (Amazon Linux / Ubuntu / Windows): ")

        # --- Subnets ---
        subnets = list_subnets(region)
        if not subnets:
            return "❌ No subnets found."
        print("🤖 🌐 Available Subnets:")
        for i, s in enumerate(subnets, 1):
            print(f"  {i}. {s['name']} ({s['id']})")

        subnet_input = input("👉 Select a subnet (number, name, or ID): ").strip()
        if subnet_input.isdigit():
            subnet_id = subnets[int(subnet_input) - 1]["id"]
        else:
            match = next((s for s in subnets if s["name"].lower() == subnet_input.lower()
                         or s["id"] == subnet_input), None)
            if not match:
                return f"❌ Subnet '{subnet_input}' not found."
            subnet_id = match["id"]

        # --- Security Groups ---
        sgs = list_security_groups(region)
        if not sgs:
            return "❌ No security groups found."
        print("🤖 🔒 Available Security Groups:")
        for i, sg in enumerate(sgs, 1):
            print(f"  {i}. {sg['name']} ({sg['id']})")

        sg_input = input("👉 Select a security group (number, name, or ID): ").strip()
        if sg_input.isdigit():
            sg_id = sgs[int(sg_input) - 1]["id"]
        else:
            match = next((sg for sg in sgs if sg["name"].lower() == sg_input.lower()
                         or sg["id"] == sg_input), None)
            if not match:
                return f"❌ Security Group '{sg_input}' not found."
            sg_id = match["id"]

        # --- Key Pairs ---
        keys = list_key_pairs(region)
        if not keys:
            return "❌ No key pairs found."
        print("🤖 🔑 Available Key Pairs:")
        for i, k in enumerate(keys, 1):
            print(f"  {i}. {k['name']}")

        key_input = input("👉 Select a key pair (number or name): ").strip()
        if key_input.isdigit():
            key_name = keys[int(key_input) - 1]["name"]
        else:
            match = next((k for k in keys if k["name"].lower() == key_input.lower()), None)
            if not match:
                return f"❌ Key pair '{key_input}' not found."
            key_name = match["name"]

        # --- Name ---
        name = params.get("Name") or input("🤖 📝 What name should I assign to this instance? ")

        # --- Find latest AMI dynamically ---
        try:
            ami = get_latest_ami(region, os_choice)
        except Exception as e:
            return f"❌ Could not find AMI for {os_choice} in {region}: {str(e)}"

        # --- Confirmation ---
        print("\n🤖 Please confirm the following before launch:")
        print(f"   Region: {region}")
        print(f"   InstanceType: {instance_type}")
        print(f"   OS: {os_choice} (AMI {ami})")
        print(f"   Subnet: {subnet_id}")
        print(f"   SecurityGroup: {sg_id}")
        print(f"   KeyPair: {key_name}")
        print(f"   Name: {name}")

        confirm = input("👉 Proceed with launch? (yes/no): ").strip().lower()
        if confirm != "yes":
            return "❌ Launch cancelled."

        # --- Launch EC2 ---
        ec2 = boto3.client("ec2", region_name=region)
        resp = ec2.run_instances(
            ImageId=ami,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
            KeyName=key_name,
            NetworkInterfaces=[{
                "DeviceIndex": 0,
                "SubnetId": subnet_id,
                "Groups": [sg_id],
                "AssociatePublicIpAddress": True
            }],
            TagSpecifications=[{
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": name}]
            }]
        )
        instance_id = resp["Instances"][0]["InstanceId"]
        return f"🎉 Successfully launched instance {instance_id} ({instance_type}, {os_choice}) in {region}"

    def list_vms(self, params):
        region = params.get("Region") or input("🤖 📍 Which region should I check?: ")
        state_filter = input("🤖 🔎 Do you want to see [running/stopped/all] instances?: ").strip().lower()

        ec2 = boto3.client("ec2", region_name=region)
        filters = []
        if state_filter in ["running", "stopped"]:
            filters.append({"Name": "instance-state-name", "Values": [state_filter]})

        resp = ec2.describe_instances(Filters=filters)
        instances = []
        for r in resp["Reservations"]:
            for i in r["Instances"]:
                name_tag = next((t["Value"] for t in i.get("Tags", []) if t["Key"] == "Name"), "Unnamed")

                # Detect OS type
                if "PlatformDetails" in i:
                    os_type = i["PlatformDetails"]
                elif "Platform" in i:
                    os_type = i["Platform"]
                else:
                    os_type = "Linux/Unix"

                # IP addresses
                private_ip = i.get("PrivateIpAddress", "N/A")
                public_ip = i.get("PublicIpAddress", "N/A")

                instances.append((i["InstanceId"], i["State"]["Name"], name_tag, os_type, private_ip, public_ip))

        if not instances:
            return "❌ No instances found."

        print("📋 Instances:")
        for idx, (iid, state, name, os_type, private_ip, public_ip) in enumerate(instances, 1):
            print(f"  {idx}. {iid} ({state}) - {name} | OS: {os_type} | PrivateIP: {private_ip} | PublicIP: {public_ip}")

        return f"✅ Displayed {len(instances)} instances."

    def delete_vm(self, params):
        region = params.get("Region") or input("🤖 📍 Which region should I use?: ")
        ec2 = boto3.client("ec2", region_name=region)

        # List running instances
        resp = ec2.describe_instances(Filters=[{"Name": "instance-state-name", "Values": ["running"]}])
        instances = []
        for r in resp["Reservations"]:
            for i in r["Instances"]:
                name_tag = next((t["Value"] for t in i.get("Tags", []) if t["Key"] == "Name"), "Unnamed")
                instances.append((i["InstanceId"], name_tag))

        if not instances:
            return "❌ No running instances to delete."

        print("🤖 🗑️ Running instances:")
        for idx, (iid, name) in enumerate(instances, 1):
            print(f"  {idx}. {iid} - {name}")

        choice = input("👉 Select instance to terminate (number, ID, or Name): ").strip()
        if choice.isdigit():
            instance_id = instances[int(choice) - 1][0]
        else:
            match = next((i for i in instances if i[0] == choice or i[1].lower() == choice.lower()), None)
            if not match:
                return f"❌ Instance '{choice}' not found."
            instance_id = match[0]

        confirm = input(f"⚠️ Really terminate {instance_id}? (yes/no): ").strip().lower()
        if confirm != "yes":
            return "❌ Termination cancelled."

        ec2.terminate_instances(InstanceIds=[instance_id])
        return f"🗑️ Termination requested for {instance_id}"
