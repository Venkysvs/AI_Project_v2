import re

def parse_intent(text):
    """
    Very simple NLP parser:
    Detects intent (create_vm, list_vm, delete_vm)
    and extracts parameters like provider, region, os, instance type.
    """
    text = text.lower()
    intent = None
    params = {}

    if any(word in text for word in ["create", "launch", "deploy"]):
        intent = "create_vm"
    elif any(word in text for word in ["delete", "terminate", "remove"]):
        intent = "delete_vm"
    elif any(word in text for word in ["list", "show", "get"]):
        intent = "list_vm"

    # Cloud provider
    if "aws" in text or "amazon" in text:
        params["Provider"] = "AWS"
    elif "azure" in text:
        params["Provider"] = "Azure"
    elif "gcp" in text or "google" in text:
        params["Provider"] = "GCP"

    # Region
    match = re.search(r"(us|eu|ap|sa|ca|af|me)-\w+-\d", text)
    if match:
        params["Region"] = match.group(0)

    # Instance type
    match = re.search(r"(t2|t3|m5|c5)\.\w+", text)
    if match:
        params["InstanceType"] = match.group(0)

    # OS
    if "amazon linux" in text:
        params["OS"] = "Amazon Linux"
    elif "ubuntu" in text:
        params["OS"] = "Ubuntu"
    elif "windows" in text:
        params["OS"] = "Windows"

    return intent, params
