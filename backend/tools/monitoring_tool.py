from repositories.monitoring_repository import MonitoringRepository


class MonitoringTool:

    def __init__(self, db):
        self.repo = MonitoringRepository(db)


    def run(self, contract_id):

        logs = self.repo.get_by_contract(
            contract_id
        )

        return [
            {
                "uptime_percentage": log.uptime_percentage,
                "outage_minutes": log.outage_minutes,
                "source": log.source
            }
            for log in logs
        ]