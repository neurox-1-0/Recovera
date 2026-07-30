from agent.state import AgentState


class AIReasoningService:


    def analyze(self, state: AgentState):

        findings = []

        recommendation = ""


        # SLA Analysis

        if state.monitoring:

            latest = state.monitoring[-1]

            findings.append(
                f"Monitoring analysis identified "
                f"{latest['outage_minutes']} minutes of service disruption."
            )


        # Incident Analysis

        if state.incidents:

            findings.append(
                f"{len(state.incidents)} provider incident(s) "
                "were identified during investigation."
            )


        # Email Analysis

        if state.emails:

            findings.append(
                "Provider communication evidence was reviewed."
            )


        # Financial Analysis

        if state.finance:

            total = sum(
                invoice["amount"]
                for invoice in state.finance
            )

            findings.append(
                f"Financial impact analysis reviewed "
                f"invoices totaling {total}."
            )


        if state.incidents and state.monitoring:

            recommendation = (
                "Proceed with SLA credit recovery "
                "based on verified service disruption evidence."
            )

        else:

            recommendation = (
                "Insufficient evidence for recovery claim."
            )


        return {

            "summary":
                " ".join(findings),

            "findings":
                findings,

            "recommendation":
                recommendation
        }