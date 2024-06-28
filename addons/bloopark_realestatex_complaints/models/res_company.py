from odoo import models, api


class ResCompany(models.Model):
    _inherit = "res.company"

    def create_complaint_sequence(self):
        self.env["ir.sequence"].create(
            {
                "name": f"Complaint Sequence {self.name}",
                "code": f"realestatex.complaint.{self.id}",
                "prefix": "COMP-",
                "padding": 4,
                "company_id": False,
                "implementation": "no_gap",
            }
        )

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)
        for company in companies:
            company.create_complaint_sequence()
        return companies
