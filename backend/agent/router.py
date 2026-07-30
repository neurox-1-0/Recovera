from tools.contract_tool import ContractTool
from tools.monitoring_tool import MonitoringTool
from tools.incident_tool import IncidentTool
from tools.email_tool import EmailTool
from tools.finance_tool import FinanceTool


class ToolRouter:

    def __init__(self, db):

        self.tools = {

            "contract": ContractTool(db),

            "monitoring": MonitoringTool(db),

            "incident": IncidentTool(db),

            "email": EmailTool(db),

            "finance": FinanceTool(db),
        }


    def run(self, tool_name, context):

        if tool_name not in self.tools:
            raise Exception(
                f"Unknown tool: {tool_name}"
            )


        return self.tools[tool_name].run(
            **context
        )