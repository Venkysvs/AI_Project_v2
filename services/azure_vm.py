from services.vm_interface import VMService

class AzureVMService(VMService):
    def __init__(self, region="eastus"):
        self.region = region

    def create_vm(self, params):
        return f"⚙️ Azure VM integration (region {self.region}) still in progress."

    def delete_vm(self, params):
        return f"⚙️ Azure VM integration (region {self.region}) still in progress."

    def list_vms(self, params):
        return [f"⚙️ Azure VM integration (region {self.region}) still in progress."]
