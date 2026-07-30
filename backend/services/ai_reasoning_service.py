from agent.state import AgentState

from services.llm_service import LLMService



class AIReasoningService:


    def __init__(self):

        self.llm = LLMService()



    def analyze(
        self,
        state: AgentState
    ):


        prompt = self.build_prompt(
            state
        )


        ai_report = self.llm.generate(
            prompt
        )


        return {

            "summary":
                ai_report,

            "findings":
                [
                    ai_report
                ],

            "recommendation":
                ai_report

        }



    def build_prompt(
        self,
        state: AgentState
    ):


        return f"""

        Investigate this SLA recovery case.

        CONTRACT INFORMATION:

        {state.contract}


        MONITORING DATA:

        {state.monitoring}


        INCIDENT DATA:

        {state.incidents}


        PROVIDER EMAILS:

        {state.emails}


        FINANCIAL DATA:

        {state.finance}


        Provide a professional investigation report.

        """
