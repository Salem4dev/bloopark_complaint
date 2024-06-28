import re
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class RealestatexComplaint(models.Model):
    _name = "realestatex.complaint"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Realestatex Complaint"

    name = fields.Char(string="Name", readonly=True, copy=False, default="New")
    title = fields.Char(string="Complaint Title", required=True)
    type = fields.Selection(
        [
            ("question", "Question"),
            ("electrical", "Electrical Issue"),
            ("heating", "Heating Issue"),
            ("other", "Other"),
        ],
        string="Type",
        required=True,
        tracking=True,
    )
    email = fields.Char(string="Email", required=True, tracking=True)
    address = fields.Char(string="Address", required=True, tracking=True)
    active = fields.Boolean("Active", default=True, tracking=True)
    stage_id = fields.Many2one(
        "realestatex.complaint.stage",
        string="Stage",
        group_expand="_read_group_stage_ids",
        readonly=False,
        tracking=True,
        store=True,
        copy=False,
        ondelete="restrict",
        default=lambda self: self._default_stage(),
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        readonly=True,
        default=lambda self: self.env.user.company_id.id,
    )
    create_date = fields.Datetime(string="Creation Date", default=fields.Datetime.now)
    description = fields.Text(string="Description", tracking=True)
    priority = fields.Selection(
        [("0", "Low"), ("1", "Normal"), ("2", "High"), ("3", "Very High")],
        string="Priority",
        default="1",
        tracking=True,
    )
    user_id = fields.Many2one(
        "res.users", string="Assigned To", readonly=True, tracking=True
    )
    is_readonly = fields.Boolean(string="Readonly", compute="_compute_is_readonly")

    def _get_new_stage(self):
        return self.env.ref("bloopark_realestatex_complaints.stage_new")

    def _get_solved_stage(self):
        return self.env.ref("bloopark_realestatex_complaints.stage_solved")

    def _get_dropped_stage(self):
        return self.env.ref("bloopark_realestatex_complaints.stage_dropped")

    @api.depends("stage_id")
    def _compute_is_readonly(self):
        readonly_stage_ids = [
            self.env.ref("bloopark_realestatex_complaints.stage_solved").id,
            self.env.ref("bloopark_realestatex_complaints.stage_dropped").id,
        ]
        for record in self:
            if record.stage_id.id in readonly_stage_ids:
                record.is_readonly = True
            else:
                record.is_readonly = False

    @api.constrains("email")
    def _check_email(self):
        for record in self:
            if not record.email:
                continue
            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_regex, record.email):
                raise ValidationError("Invalid email format: %s" % record.email)

    @api.model
    def _default_stage(self):
        return self.env.ref("bloopark_realestatex_complaints.stage_new").id

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env["realestatex.complaint.stage"].search([])

    @api.model
    def _get_next_user(self):
        # Get all user ids from the "Complaint User" group
        complaint_user_group = self.env.ref(
            "bloopark_realestatex_complaints.group_complaint_user"
        )
        user_ids = complaint_user_group.users.ids
        if not user_ids:
            return False  # No users found
        # Retrieve the last assigned user from ir.config_parameter
        param = self.env["ir.config_parameter"].sudo()
        last_assigned_user = int(
            param.get_param("realestatex.last_assigned_user", default=0)
        )
        # Determine the next user id
        if last_assigned_user in user_ids:
            next_user_index = (user_ids.index(last_assigned_user) + 1) % len(user_ids)
        else:
            next_user_index = 0
        next_user_id = user_ids[next_user_index]
        # Store the next user as the last assigned user
        param.set_param("realestatex.last_assigned_user", next_user_id)
        return next_user_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals.get("name") in _("New"):
                company_id = vals.get("company_id") or self.env.user.company_id.id
                code = f"realestatex.complaint.{company_id}"
                vals["name"] = self.env["ir.sequence"].next_by_code(code)
        records = super().create(vals_list)
        records._send_email_by_stage(create=True)
        return records

    def write(self, values):
        res = super().write(values)
        self._send_email_by_stage()
        return res

    def _send_email_by_stage(self, create=False):
        submitted_template = self.env.ref(
            "bloopark_realestatex_complaints.mail_template_complaint_submitted"
        )
        solved_template = self.env.ref(
            "bloopark_realestatex_complaints.mail_template_complaint_solved"
        )
        dropped_template = self.env.ref(
            "bloopark_realestatex_complaints.mail_template_complaint_dropped"
        )
        template = False
        for rec in self:
            if (
                create
                and submitted_template
                and rec._get_new_stage().id == rec.stage_id.id
            ):
                template = submitted_template
            elif solved_template and rec._get_solved_stage().id == rec.stage_id.id:
                template = solved_template
            elif dropped_template and rec._get_dropped_stage().id == rec.stage_id.id:
                template = dropped_template
            if rec.email and template:  # Ensure the record has an email before sending
                render_ctx = dict(
                    rec.env.context,
                    email_to=rec.email,
                    email_from=rec.company_id.email or "info@yourcompany.com",
                    send_to_name=rec.name,
                )
                template.with_context(render_ctx).send_mail(
                    rec.id,
                    force_send=True,
                    email_layout_xmlid="mail.mail_notification_light",
                )
            return True
        return False
