from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class ReaderModel(models.Model):
    _name = 'library_app.reader_model'
    _description = 'Reader Model'
    _sql_constraints = [('reader_unique_dni','UNIQUE(dni)','DNI must be unique!!')]

    partnerid = fields.Integer(string="Partner id", readonly=True, help="This is the reader partner id")
    name = fields.Char(string="Reader Name", required=True, index=True, help="Reader Name")
    surname = fields.Char(string="Surname", index=True, help="Surname")
    dni = fields.Char(string="DNI", size=9, required=True, help="Reader DNI")
    phone = fields.Char(string="Phone", size=9, required=True, help="This is the reader phone")
    photo = fields.Binary(string="Photo", help="This is a reader photo")
    email = fields.Char(string="Email", required=True, help="This is the reader email")
    postalcode = fields.Char(string="Postal Code", required=True, index=True, help="Postal Code")
    city = fields.Char(string="City", required=True, index=True, help="City")
    direction = fields.Char(string="Direction", required=True, index=True, help="Direction")
    money = fields.Float(string="Money", required=True, default=0, help="This is the reader money")
    penaltyamount = fields.Float (string="Penalty Amount", readonly=True, default=0, help="This is the reader debt.")

    rent_ids = fields.One2many("library_app.rent_model", "reader_id", string="Rent", required=True)
    penalty_ids = fields.One2many("library_app.penalty_model", "reader_id", readonly=True, string="Penalty", required=True)

    @api.model
    def create(self, vals):
        vals['partnerid'] = self.env['ir.sequence'].next_by_code('reference.test')
        return super(ReaderModel, self).create(vals)

    @api.constrains("dni")

    def _check_dni(self):
        dniList = "TRWAGMYFPDXBNJZSQVHLCKE"
        while True:
            if len(self.dni) == 9 and self.dni[:-1].isdigit and self.dni[-1].isalpha:
                decimals = int(self.dni[:-1]) % 23

                if self.dni[-1] == dniList[decimals]:
                    return True
                else:
                    raise ValidationError("Dni is not correct!")
            else:
                raise ValidationError("Dni is not correct!")

    @api.constrains("email")

    def _check_email(self):
        pEmail = '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(pEmail,self.email):

            raise ValidationError("Email is not correct!")

        return True