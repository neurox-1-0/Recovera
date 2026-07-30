from repositories.email_repository import EmailRepository


class EmailTool:

    def __init__(self, db):
        self.repo = EmailRepository(db)


    def run(self, contract_id):

        emails = self.repo.get_by_contract(
            contract_id
        )

        return [
            {
                "sender": e.sender,
                "subject": e.subject,
                "body": e.body
            }
            for e in emails
        ]