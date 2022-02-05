from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class EmployeModel(models.Model):
    _name = 'library_app.employe_model'
    _description = 'Employe Model'
    _sql_constraints = [('employe_unique_dni','UNIQUE(dni)','DNI must be unique!!')]

    name = fields.Char(string="Employe Name", required=True, index=True, help="Employe Name")
    surname = fields.Char(string="Surname", index=True, help="Surname")
    photo = fields.Binary(string="Photo", help="This is a employe photo")
    dni = fields.Char(string="DNI", size=9, required=True, help="Employe DNI")
    phone = fields.Char(string="Phone", size=9, required=True, help="This is the employe phone number")

    rent_ids = fields.One2many("library_app.rent_model", "employe_id", string="Employe", required=True)

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
                