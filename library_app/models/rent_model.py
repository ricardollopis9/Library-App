from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class RentModel(models.Model):
    _name = 'library_app.rent_model'
    _description = 'Rent Model'

    date = fields.Date(string="Date", required=True)
    state = fields.Selection(selection=[('Draft','Draft'),('Confirmed','Confirmed')], default="Draft")
    returned_state = fields.Selection(selection=[('true','true'),('false','false')], default="false")
    name = fields.Char(compute="_changename")

    book_id = fields.Many2one("library_app.book_model", string="Book", required=True)
    employe_id = fields.Many2one("library_app.employe_model", string="Employe", required=True)
    reader_id = fields.Many2one("library_app.reader_model", string="Reader", required=True)

    def change_state(self):
        self.state = "Confirmed"
        self.returned_state = "true"

        if(self.book_id.stock > 0):
            self.book_id.stock -= 1
            return True
        else:
            raise ValidationError("No queda stock de este libro!")

    def returned(self):
        self.returned_state = "false"
        self.book_id.stock += 1

        return True

    @api.depends("name")
    def _changename(self):
        if len(self.env['library_app.rent_model'].search([])) == 0:
            id = 1
        id = (self.env['library_app.rent_model'].search([])[-1].id + 1)
        ids = "Rent Id " + str(id)
        self.name = ids