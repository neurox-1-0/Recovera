from agent.state import AgentState

from services.llm_service import LLMService



class AIReasoningService:


    def __init__(self):

        self.llm = LLMService()



    def analyze(
        self,
        state: AgentState
    ):


        prompt = f"""

        Analyse this SLA investigation.

        CONTRACT:

        {state.contract}


        MONITORING:

        {state.monitoring}


        INCIDENTS:

        {state.incidents}


        EMAILS:

        {state.emails}


        FINANCE:

        {state.finance}


        Generate an enterprise investigation report.

        """


        report = self.llm.generate(
            prompt
        )


        return {


            "summary":
                report["executive_summary"],


            "findings":
                report["evidence_analysis"],


            "recommendation":
                report["recovery_justification"],


            "full_report":
                report

        }