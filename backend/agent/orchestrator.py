from agent.state import AgentState
from agent.planner import Planner
from agent.router import ToolRouter
from agent.memory import AgentMemory
from agent.logger import AgentLogger
from agent.evaluator import Evaluator
from agent.confidence import ConfidenceEngine


class AgentOrchestrator:

    def __init__(self, db):

        self.db = db

        self.planner = Planner()

        self.router = ToolRouter(db)

        self.memory = AgentMemory()

        self.logger = AgentLogger()

        self.evaluator = Evaluator()

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
            # Run Tool
            # ---------------------------------

            result = self.router.run(
                tool,
                context
            )



            # ---------------------------------
            # Store Result
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

                details=
                    "Tool executed successfully."

            )



        # ---------------------------------
        # Evaluate Investigation
        # ---------------------------------

        findings = self.evaluator.evaluate(
            state
        )



        # ---------------------------------
        # Calculate Confidence
        # ---------------------------------

        confidence = self.confidence.calculate(
            state
        )



        state.confidence = confidence



        self.logger.log(
            "AI Investigation completed."
        )



        # ---------------------------------
        # Return Agent Report
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


            "findings":
                findings,


            "confidence":
                confidence,


            "recommendation":
                state.recommendation,


            "memory":
                self.memory.history()
        }