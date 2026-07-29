from datetime import datetime


class AgentLogger:

    def log(self, message: str):

        print(
            f"[{datetime.utcnow()}] {message}"
        )