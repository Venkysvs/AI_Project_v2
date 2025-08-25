from services.aws_ec2 import AWSVMService
from services.azure_vm import AzureVMService
from services.gcp_vm import GCPVMService

PROVIDER_REGISTRY = {
    "aws": AWSVMService,
    "azure": AzureVMService,
    "gcp": GCPVMService
}

DEFAULT_PROVIDER = "aws"
DEFAULT_REGION = "us-east-1"
