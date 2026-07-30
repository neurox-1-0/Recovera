from agent.state import AgentState
from agent.planner import Planner
from agent.router import ToolRouter
from agent.memory import AgentMemory
from agent.logger import AgentLogger
from agent.confidence import ConfidenceEngine

from services.ai_reasoning_service import AIReasoningService



class AgentOrchestrator:


    def __init__(self, db):

        self.db = db

        # ---------------------------------
        # Agent Components
        # ---------------------------------

        self.planner = Planner()

        self.router = ToolRouter(db)

        self.memory = AgentMemory()

        self.logger = AgentLogger()


        # ---------------------------------
        # Intelligence Layer
        # ---------------------------------

        self.reasoning = AIReasoningService()

        self.confidence = ConfidenceEngine()



    def investigate(
        self,
        goal: str,
        contract_number: str
    ):


        # ---------------------------------
        # Create Agent State
        # ---------------------------------

        state = AgentState(
            goal=goal
        )


        self.logger.log(
            "AI Investigation started."
        )



        # ---------------------------------
        # Execute Investigation Plan
        # ---------------------------------

        while True:


            tool = self.planner.next_tool(
                state
            )


            if tool is None:
                break



            self.logger.log(
                f"Executing tool: {tool}"
            )



            # ---------------------------------
            # Build Tool Context
            # ---------------------------------

            if tool == "contract":

                context = {

                    "contract_number":
                        contract_number

                }


            else:

                if not state.contract:

                    raise Exception(
                        "Contract information missing."
                    )


                context = {

                    "contract_id":
                        state.contract["id"]

                }



            # ---------------------------------
            # Execute Tool
            # ---------------------------------

            result = self.router.run(
                tool,
                context
            )



            # ---------------------------------
            # Save Tool Result
            # ---------------------------------

            if tool == "contract":

                state.contract = result


            elif tool == "monitoring":

                state.monitoring = result


            elif tool == "incident":

                state.incidents = result


            elif tool == "email":

                state.emails = result


            elif tool == "finance":

                state.finance = result



            state.completed_tools.append(
                tool
            )



            self.memory.add(

                title=tool,

                details="Tool executed successfully."

            )



        # ---------------------------------
        # AI Reasoning
        # ---------------------------------

        ai_analysis = self.reasoning.analyze(
            state
        )


        state.recommendation = (
            ai_analysis["recommendation"]
        )



        findings = (
            ai_analysis["findings"]
        )



        # ---------------------------------
        # Confidence Calculation
        # ---------------------------------

        confidence = self.confidence.calculate(
            state
        )


        state.confidence = confidence



        self.logger.log(
            "AI Investigation completed."
        )



        # ---------------------------------
        # Return Report
        # ---------------------------------

        return {

            "goal":
                state.goal,


            "contract":
                state.contract,


            "monitoring":
                state.monitoring,


            "incidents":
                state.incidents,


            "emails":
                state.emails,


            "finance":
                state.finance,


            "completed_tools":
                state.completed_tools,


            # AI structured analysis

            "summary":
                ai_analysis["summary"],


            "findings":
                findings,


            "recommendation":
                state.recommendation,


            "full_report":
                ai_analysis["full_report"],


            "confidence":
                confidence,


            "memory":
                self.memory.history()

        }