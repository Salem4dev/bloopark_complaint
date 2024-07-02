# Disable Pylint invalid-name warning for the setUp method
# pylint: disable=W0104
{
    "name": "Bloopark RealEstateX Complaints",
    "version": "16.0.0.1",
    "summary": "Complaint Management for RealEstateX",
    "author": "Salem Ouda",
    "category": "Website",
    "Website": "bloopark.de",
    "license": "LGPL-3",
    "depends": ["website", "base_automation"],
    "data": [
        "security/complaint_security.xml",
        "security/ir.model.access.csv",
        "data/complaint_data.xml",
        "data/complaint_automated.xml",
        "data/complaint_mail_templates.xml",
        "views/complaint_website_form.xml",
        "views/complaint_views.xml",
        "views/complaint_stage_views.xml",
        "views/complaint_website_templates.xml",
        "report/complaint_work_order_report.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "/bloopark_realestatex_complaints/static/src/js/complaint_form_validate.js"
        ],
    },
    "installable": True,
    "application": True,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
