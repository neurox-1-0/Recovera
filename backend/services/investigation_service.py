from services.sla_service import SLAService
from services.recovery_service import RecoveryService
from services.evidence_service import EvidenceService

from agent.orchestrator import AgentOrchestrator


from repositories.contract_repository import ContractRepository
from repositories.monitoring_repository import MonitoringRepository
from repositories.incident_repository import IncidentRepository
from repositories.email_repository import EmailRepository
from repositories.invoice_repository import InvoiceRepository
from repositories.user_repository import UserRepository
from repositories.investigation_repository import InvestigationRepository

from repositories.evidence_repository import EvidenceRepository
from repositories.recovery_repository import RecoveryRepository
from repositories.audit_repository import AuditRepository


from models.recovery_case import RecoveryCase
from models.audit_log import AuditLog



class InvestigationService:


    def __init__(self, db):

        self.db = db


        # ---------------------------------
        # Repositories
        # ---------------------------------

        self.contract_repo = ContractRepository(db)

        self.monitoring_repo = MonitoringRepository(db)

        self.incident_repo = IncidentRepository(db)

        self.email_repo = EmailRepository(db)

        self.invoice_repo = InvoiceRepository(db)

        self.user_repo = UserRepository(db)


        self.investigation_repo = InvestigationRepository(db)


        self.evidence_repo = EvidenceRepository(db)

        self.recovery_repo = RecoveryRepository(db)

        self.audit_repo = AuditRepository(db)



        # ---------------------------------
        # Services
        # ---------------------------------

        self.sla_service = SLAService()

        self.recovery_service = RecoveryService()


        self.evidence_service = EvidenceService(
            self.evidence_repo
        )



        # ---------------------------------
        # AI Agent
        # ---------------------------------

        self.agent = AgentOrchestrator(
            db
        )



    def investigate(
        self,
        contract_id: int,
        goal: str = "Investigate SLA breach"
    ):


        # ---------------------------------
        # Load Contract
        # ---------------------------------

        contract = self.contract_repo.get_by_id(
            contract_id
        )


        if not contract:
            raise Exception(
                "Contract not found"
            )



        # ---------------------------------
        # Run AI Investigation Agent
        # ---------------------------------

        agent_result = self.agent.investigate(

            goal=goal,

            contract_number=
                contract.contract_number

        )



        # ---------------------------------
        # Load System User
        # ---------------------------------

        system_user = self.user_repo.get_by_email(
            "admin@recovera.ai"
        )


        if not system_user:
            raise Exception(
                "System administrator not found. Please run database.seed."
            )



        # ---------------------------------
        # Create Investigation
        # ---------------------------------

        investigation = (
            self.investigation_repo.create_investigation(

                contract_id=contract.id,

                created_by=system_user.id,

                confidence_score=
                    agent_result.get(
                        "confidence",
                        0
                    )

            )
        )



        # ---------------------------------
        # Load Related Data
        # ---------------------------------

        monitoring_logs = (
            self.monitoring_repo
            .get_by_contract(contract.id)
        )


        incidents = (
            self.incident_repo
            .get_by_contract(contract.id)
        )


        emails = (
            self.email_repo
            .get_by_contract(contract.id)
        )


        invoices = (
            self.invoice_repo
            .get_by_contract(contract.id)
        )



        if not monitoring_logs:
            raise Exception(
                "No monitoring data found"
            )


        if not invoices:
            raise Exception(
                "No invoice data found"
            )



        # ---------------------------------
        # Generate Evidence
        # ---------------------------------

        self.evidence_service.generate(

            investigation_id=
                investigation.id,

            monitoring_logs=
                monitoring_logs,

            incidents=
                incidents,

            emails=
                emails

        )



        # ---------------------------------
        # Latest Records
        # ---------------------------------

        latest_monitoring = monitoring_logs[-1]

        latest_invoice = invoices[-1]



        # ---------------------------------
        # SLA Analysis
        # ---------------------------------

        sla_result = self.sla_service.check_breach(

            contract.guaranteed_uptime,

            latest_monitoring.uptime_percentage

        )



        # ---------------------------------
        # Recovery Calculation
        # ---------------------------------

        eligible = self.recovery_service.check_eligibility(

            sla_result["breach"]

        )


        estimated_credit = (

            self.recovery_service.calculate_credit(

                latest_invoice.amount,

                contract.credit_percentage

            )

            if eligible

            else 0

        )



        # ---------------------------------
        # Save Recovery Case
        # ---------------------------------

        recovery_case = RecoveryCase(

            investigation_id=
                investigation.id,

            eligible=
                eligible,

            estimated_credit=
                estimated_credit,

            justification=(

                "SLA breached based on monitoring logs."

                if eligible

                else "No SLA breach detected."

            )

        )


        self.recovery_repo.create(
            recovery_case
        )



        # ---------------------------------
        # Save Audit Log
        # ---------------------------------

        audit_log = AuditLog(

            user_id=
                system_user.id,

            action=
                "AI Investigation Completed",

            details=
                f"Investigation #{investigation.id} completed."

        )


        self.audit_repo.create(
            audit_log
        )



        # ---------------------------------
        # Complete Investigation
        # ---------------------------------

        self.investigation_repo.complete_investigation(
            investigation
        )



        self.db.commit()



        # ---------------------------------
        # Final Report
        # ---------------------------------

        report = {


            "investigation_id":
                investigation.id,


            "contract_number":
                contract.contract_number,


            "service":
                contract.service_name,


            "provider":
                contract.provider,


            "customer":
                contract.customer,


            "required_uptime":
                contract.guaranteed_uptime,


            "actual_uptime":
                latest_monitoring.uptime_percentage,


            "sla_breach":
                sla_result["breach"],


            "incident_count":
                len(incidents),


            "email_count":
                len(emails),


            "estimated_credit":
                estimated_credit,


            "eligible":
                eligible,



            # ---------------------------------
            # AI REPORT
            # ---------------------------------

            "ai_report":
                agent_result.get(
                    "full_report",
                    {}
                ),



            "ai_findings":
                agent_result.get(
                    "findings",
                    []
                ),



            "ai_confidence":
                agent_result.get(
                    "confidence",
                    0
                ),



            "ai_recommendation":
                agent_result.get(
                    "recommendation",
                    ""
                ),



            "agent_memory":
                agent_result.get(
                    "memory",
                    []
                )

        }


        return report