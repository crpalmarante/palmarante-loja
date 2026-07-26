from business_core.shared.command import BusinessCommand


class CreateParty(BusinessCommand):
    def __init__(self, party_type: str = "person", **kwargs):
        super().__init__(command_type="CreateParty")
        self.party_type = party_type
        for k, v in kwargs.items():
            setattr(self, k, v)


class UpdateParty(BusinessCommand):
    def __init__(self, party_id: str = "", **kwargs):
        super().__init__(command_type="UpdateParty")
        self.party_id = party_id
        for k, v in kwargs.items():
            setattr(self, k, v)


class ActivateParty(BusinessCommand):
    def __init__(self, party_id: str = ""):
        super().__init__(command_type="ActivateParty")
        self.party_id = party_id


class SuspendParty(BusinessCommand):
    def __init__(self, party_id: str = ""):
        super().__init__(command_type="SuspendParty")
        self.party_id = party_id


class ArchiveParty(BusinessCommand):
    def __init__(self, party_id: str = ""):
        super().__init__(command_type="ArchiveParty")
        self.party_id = party_id


class AssignRole(BusinessCommand):
    def __init__(self, party_id: str = "", role: str = ""):
        super().__init__(command_type="AssignRole")
        self.party_id = party_id
        self.role = role


class RemoveRole(BusinessCommand):
    def __init__(self, party_id: str = "", role: str = ""):
        super().__init__(command_type="RemoveRole")
        self.party_id = party_id
        self.role = role
