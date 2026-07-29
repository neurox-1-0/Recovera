class AgentMemory:

    def __init__(self):
        self.steps = []

    def add(self, title: str, details: str):

        self.steps.append(
            {
                "title": title,
                "details": details,
            }
        )

    def history(self):
        return self.steps