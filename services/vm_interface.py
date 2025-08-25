from abc import ABC, abstractmethod

class VMService(ABC):
    @abstractmethod
    def create_vm(self, params: dict):
        pass

    @abstractmethod
    def delete_vm(self, params: dict):
        pass

    @abstractmethod
    def list_vms(self, params: dict):
        pass
