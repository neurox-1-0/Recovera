from repositories.invoice_repository import InvoiceRepository


class FinanceTool:

    def __init__(self, db):
        self.repo = InvoiceRepository(db)


    def run(self, contract_id):

        invoices = self.repo.get_by_contract(
            contract_id
        )

        return [
            {
                "invoice_number": i.invoice_number,
                "amount": i.amount,
                "billing_month": i.billing_month
            }
            for i in invoices
        ]