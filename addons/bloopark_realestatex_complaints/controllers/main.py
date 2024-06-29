import re
from odoo import http
from odoo.http import request


class ComplaintController(http.Controller):

    def _get_company_ids(self):
        return request.env["res.company"].sudo().search([])

    @http.route("/complaint", type="http", auth="public", website=True)
    def bloopark_complaint_form(self, **kwargs):
        return request.render(
            "bloopark_realestatex_complaints.complaint_land_page_form",
            {
                "errors": {},
                "values": {"type": "0"},
                "company_ids": self._get_company_ids(),
            },
        )

    @http.route(
        "/complaint/submit",
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
        csrf=True,
    )
    def submit_bloopark_complaint_form(self, **kwargs):
        # Extract and validate the form data
        title = kwargs.get("title")
        email = kwargs.get("email")
        address = kwargs.get("address")
        complaint_type = kwargs.get("type")
        description = kwargs.get("description")
        company = kwargs.get("company_id")
        errors = {}
        if not title.strip():
            errors["title"] = "Please enter your name."
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors["email"] = "Please enter a valid email address."
        if not address.strip():
            errors["address"] = "Please enter your address."
        if not complaint_type or complaint_type not in [
            "question",
            "electrical",
            "heating",
            "other",
        ]:
            errors["type"] = (
                f"{complaint_type} is Invlaid Type, Please select a complaint type."
            )
        if not description.strip():
            errors["description"] = "Please enter a description."
        if not company.strip():
            errors["company_id"] = "Please select a company."
        if errors:
            return request.render(
                "bloopark_realestatex_complaints.complaint_land_page_form",
                {
                    "errors": errors,
                    "values": kwargs,
                    "company_ids": self._get_company_ids(),
                },
            )
        # If no errors, create the complaint
        complaint = (
            request.env["realestatex.complaint"]
            .sudo()
            .create(
                {
                    "title": title,
                    "email": email,
                    "address": address,
                    "type": complaint_type,
                    "description": description,
                    "company_id": company,
                }
            )
        )
        return request.env["ir.ui.view"]._render_template(
            "bloopark_realestatex_complaints.complaint_success",
            {"complaint_id": complaint.name},
        )
