from agent.state import AgentState
from agent.planner import Planner
from agent.router import ToolRouter
from agent.memory import AgentMemory
from agent.logger import AgentLogger
from agent.evaluator import Evaluator
from agent.confidence import ConfidenceEngine


class AgentOrchestrator:

    def __init__(self):

        self.planner = Planner()
        self.router = ToolRouter()

        self.memory = AgentMemory()
        self.logger = AgentLogger()

        self.evaluator = Evaluator()
        self.confidence = ConfidenceEngine()

    def investigate(self, goal: str):

        state = AgentState(goal=goal)

        self.logger.log("Investigation started.")

        while True:

            tool = self.planner.next_tool(state)

            if tool is None:
                break

            self.logger.log(f"Running tool: {tool}")

            result = self.router.run(tool)

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

            state.completed_tools.append(tool)

            self.memory.add(
                title=tool,
                details="Tool execution completed."
            )

        findings = self.evaluator.evaluate(state)

        confidence = self.confidence.calculate(state)

        self.logger.log("Investigation completed.")

        return {
            "goal": state.goal,
            "completed_tools": state.completed_tools,
            "findings": findings,
            "confidence": confidence,
            "recommendation": state.recommendation,
            "memory": self.memory.history(),
        }