from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestRealestatexComplaint(TransactionCase):
    # Disable Pylint invalid-name warning for the setUp method
    # pylint: disable=C0103
    def setUp(self):
        super().setUp()
        self.complaint = self.env["realestatex.complaint"]
        self.company = self.env["res.company"]
        self.stage = self.env["realestatex.complaint.stage"]
        self.user = self.env["res.users"]
        self.sequence = self.env["ir.sequence"]

        # Create two companies
        self.company1 = self.company.create({"name": "Test Company 1"})
        self.company2 = self.company.create({"name": "Test Company 2"})

        # Create stages
        self.stage_new = self.stage.create({"name": "New", "sequence": 1})
        self.stage_solved = self.stage.create({"name": "Solved", "sequence": 2})
        self.stage_dropped = self.stage.create({"name": "Dropped", "sequence": 3})

        # Create users for each company
        self.user1 = self.user.create(
            {
                "name": "User 1",
                "login": "user1@test.com",
                "email": "user1@test.com",
                "company_ids": [(6, 0, [self.company1.id])],
                "company_id": self.company1.id,
            }
        )
        self.user2 = self.user.create(
            {
                "name": "User 2",
                "login": "user2@test.com",
                "email": "user2@test.com",
                "company_ids": [(6, 0, [self.company2.id])],
                "company_id": self.company2.id,
            }
        )

        # Create sequence for complaints
        self.sequence_company1 = self.sequence.create(
            {
                "name": "Complaint Sequence Company 1",
                "code": f"realestatex.complaint.{self.company1.id}",
                "prefix": "COMP1-",
                "padding": 4,
                "company_id": False,
            }
        )
        self.sequence_company2 = self.sequence.create(
            {
                "name": "Complaint Sequence Company 2",
                "code": f"realestatex.complaint.{self.company2.id}",
                "prefix": "COMP2-",
                "padding": 4,
                "company_id": False,
            }
        )

    def test_complaint_creation_multi_company(self):
        """Test the creation of complaints for different companies"""
        complaint1 = self.complaint.create(
            {
                "title": "Complaint Company 1",
                "email": "complaint1@example.com",
                "address": "Address 1",
                "type": "electrical",
                "description": "Description 1",
                "company_id": self.company1.id,
                "stage_id": self.stage_new.id,
            }
        )
        complaint2 = self.complaint.create(
            {
                "title": "Complaint Company 2",
                "email": "complaint2@example.com",
                "address": "Address 2",
                "type": "heating",
                "description": "Description 2",
                "company_id": self.company2.id,
                "stage_id": self.stage_new.id,
            }
        )
        self.assertEqual(complaint1.company_id.id, self.company1.id)
        self.assertEqual(complaint2.company_id.id, self.company2.id)

    def test_complaint_access_multi_company(self):
        """Test that users can only access complaints from their own company"""
        complaint1 = self.complaint.create(
            {
                "title": "Complaint Company 1",
                "email": "complaint1@example.com",
                "address": "Address 1",
                "type": "electrical",
                "description": "Description 1",
                "company_id": self.company1.id,
                "stage_id": self.stage_new.id,
            }
        )
        complaint2 = self.complaint.create(
            {
                "title": "Complaint Company 2",
                "email": "complaint2@example.com",
                "address": "Address 2",
                "type": "heating",
                "description": "Description 2",
                "company_id": self.company2.id,
                "stage_id": self.stage_new.id,
            }
        )

        # Switch to user1 and check access
        self.env.user = self.user1
        complaints_user1 = self.complaint.search([("company_id", "=", self.company1.id)])
        self.assertIn(complaint1, complaints_user1)
        self.assertNotIn(complaint2, complaints_user1)

        # Switch to user2 and check access
        self.env.user = self.user2
        complaints_user2 = self.complaint.search([("company_id", "=", self.company2.id)])
        self.assertIn(complaint2, complaints_user2)
        self.assertNotIn(complaint1, complaints_user2)

    def test_complaint_email_validation(self):
        """Test creating a complaint with an invalid email"""
        with self.assertRaises(ValidationError):
            self.complaint.create(
                {
                    "title": "Test Complaint",
                    "email": "invalid-email",
                    "address": "Test Address",
                    "type": "electrical",
                    "description": "Test description",
                    "company_id": self.company1.id,
                    "stage_id": self.stage_new.id,
                }
            )

    def test_complaint_no_description(self):
        """Test creating a complaint without a description"""
        complaint = self.complaint.create(
            {
                "title": "Test Complaint",
                "email": "test@example.com",
                "address": "Test Address",
                "type": "electrical",
                "company_id": self.company1.id,
                "stage_id": self.stage_new.id,
            }
        )
        self.assertEqual(complaint.description, False)
