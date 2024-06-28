from odoo import models, fields


class RealestatexComplaintStage(models.Model):
    _name = "realestatex.complaint.stage"
    _description = "Complaint Stage"
    _order = "sequence, id"

    name = fields.Char(string="Stage Name", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    fold = fields.Boolean(string="Folded in Kanban", default=False)
    complaint_ids = fields.One2many(
        "realestatex.complaint", "stage_id", string="Complaints"
    )
