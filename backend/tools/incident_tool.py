from repositories.incident_repository import IncidentRepository


class IncidentTool:

    def __init__(self, db):
        self.repo = IncidentRepository(db)


    def run(self, contract_id):

        incidents = self.repo.get_by_contract(
            contract_id
        )

        return [
            {
                "code": i.incident_code,
                "title": i.title,
                "severity": str(i.severity),
                "description": i.description
            }
            for i in incidents
        ]