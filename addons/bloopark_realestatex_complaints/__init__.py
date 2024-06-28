# -*- coding: utf-8 -*-

from odoo import api, SUPERUSER_ID
from . import models
from . import controllers


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    companies = env["res.company"].search([])
    for company in companies:
        company.create_complaint_sequence()


def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    sequences = env["ir.sequence"].search([("code", "like", "realestatex.complaint.%")])
    sequences.unlink()
