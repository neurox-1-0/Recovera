class Evaluator:

    def evaluate(self, state):

        findings = []

        if state.monitoring:
            findings.append(
                "Monitoring evidence analysed."
            )

        if state.incidents:
            findings.append(
                f"{len(state.incidents)} incidents found."
            )

        if state.emails:
            findings.append(
                "Provider communications reviewed."
            )

        if state.finance:
            findings.append(
                "Financial impact calculated."
            )

        state.recommendation = (
            "Proceed with SLA credit recovery."
        )

        return findings