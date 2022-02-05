from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class RentModel(models.Model):
    _name = 'library_app.rent_model'
    _description = 'Rent Model'

    date = fields.Date(string="Date", required=True)
    state = fields.Selection(selection=[('Draft','Draft'),('Confirmed','Confirmed')], default="Draft")

    book_id = fields.Many2one("library_app.book_model", string="Book", required=True)
    employe_id = fields.Many2one("library_app.employe_model", string="Employe", required=True)
    reader_id = fields.Many2one("library_app.reader_model", string="Reader", required=True)

    def change_state(self):
        self.state = "Confirmed"
        self.ensure_one()
        self._cr.autocommit(False)

        for rec in self.lines_ids:
            if rec.quantity <= rec.product_id.stock:
                rec.product_id.stock -= rec.quantity
            else:
                self._cr.rollback()
                self._cr.autocommit(True)
                raise ValidationError("No hay suficiente stock.")
        self._cr.commit()
        self._cr.autocommit(True)
        return True