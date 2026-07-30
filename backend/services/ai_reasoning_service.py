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

You are an enterprise SLA recovery AI agent.

Analyze the following SLA investigation data.

Generate a structured investigation report.

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


Return the report with these sections:

1. executive_summary
2. root_cause_analysis
3. evidence_analysis
4. recovery_justification
5. recommended_actions
6. risk_assessment

The analysis must determine:
- whether SLA breach occurred
- why it occurred
- available evidence
- recovery eligibility
- recommended business action

"""


        report = self.llm.generate(
            prompt
        )


        return {


            "summary":
                report.get(
                    "executive_summary",
                    ""
                ),



            "findings":
                report.get(
                    "evidence_analysis",
                    []
                ),



            "recommendation":
                report.get(
                    "recovery_justification",
                    ""
                ),



            "full_report":
                report


        }