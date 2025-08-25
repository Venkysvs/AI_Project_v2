from services.aws_ec2 import AWSVMService

def handle_request(intent, params):
    provider = params.get("Provider")

    # If provider missing, ask user
    if not provider:
        provider = input("🤖 🌐 Which cloud provider do you want? (AWS / Azure / GCP): ")
        provider = provider.strip().lower()
        params["Provider"] = provider.upper()

    if provider.lower() == "aws":
        svc = AWSVMService()

        if intent == "create_vm":
            return svc.create_vm(params)
        elif intent == "list_vm":
            return svc.list_vms(params)
        elif intent == "delete_vm":
            return svc.delete_vm(params)
        else:
            return f"❌ Unsupported intent '{intent}' for AWS."

    elif provider.lower() in ["azure", "gcp"]:
        return f"🌐 {provider.upper()} integration still in progress and will be available soon."

    else:
        return f"❌ Unknown provider '{provider}'."

