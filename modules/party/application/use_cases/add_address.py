from modules.party.domain.entities.address import Address
from modules.party.domain.events.party_events import AddressAdded
from modules.party.domain.repositories.party_repository import PartyRepository
from modules.party.application.commands.party_commands import AddAddress, RemoveAddress


class AddAddressUseCase:
    def __init__(self, repository: PartyRepository):
        self.repository = repository
        self.events: list = []

    def execute(self, cmd: AddAddress) -> Address:
        party = self.repository.find_by_id(cmd.party_id)
        if not party:
            raise ValueError(f'Party not found: {cmd.party_id}')

        addr = Address(
            street=cmd.street,
            number=cmd.number,
            complement=cmd.complement,
            district=cmd.district,
            city=cmd.city,
            state=cmd.state,
            postal_code=cmd.postal_code,
            ibge_code=cmd.ibge_code,
            country=cmd.country,
            address_type=cmd.address_type,
            is_main=cmd.is_main
        )
        party.add_address(addr)
        self.repository.save(party)
        self.events.append(AddressAdded(party_id=cmd.party_id, address=addr))
        return addr

    def remove(self, cmd: RemoveAddress) -> None:
        party = self.repository.find_by_id(cmd.party_id)
        if not party:
            raise ValueError(f'Party not found: {cmd.party_id}')
        party.remove_address(cmd.address_index)
        self.repository.save(party)
