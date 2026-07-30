from repositories.contract_repository import ContractRepository


class ContractTool:

    def __init__(self, db):
        self.repo = ContractRepository(db)


    def run(self, contract_number):

        contract = self.repo.get_by_number(
            contract_number
        )

        if not contract:
            raise Exception(
                "Contract not found"
            )

        return {
            "id": contract.id,
            "contract_number": contract.contract_number,
            "provider": contract.provider,
            "customer": contract.customer,
            "service_name": contract.service_name,
            "guaranteed_uptime": contract.guaranteed_uptime,
            "credit_percentage": contract.credit_percentage
        }