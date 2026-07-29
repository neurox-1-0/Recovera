class ConfidenceEngine:

    def calculate(self, state):

        score = 0

        if state.contract:
            score += 20

        if state.monitoring:
            score += 20

        if state.incidents:
            score += 20

        if state.emails:
            score += 20

        if state.finance:
            score += 20

        state.confidence = score / 100

        return state.confidence