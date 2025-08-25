from services.vm_interface import VMService

class GCPVMService(VMService):
    def __init__(self, region="us-east1"):
        self.region = region

    def create_vm(self, params):
        return f"⚙️ GCP VM integration (region {self.region}) still in progress."

    def delete_vm(self, params):
        return f"⚙️ GCP VM integration (region {self.region}) still in progress."

    def list_vms(self, params):
        return [f"⚙️ GCP VM integration (region {self.region}) still in progress."]
