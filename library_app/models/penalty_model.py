from attr import validate
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class PenaltyModel(models.Model):
    _name = 'library_app.penalty_model'
    _description = 'Penalty Model'
    _sql_constraints = [('penalty_unique_penaltyid','UNIQUE(penaltyid)','PENALTY ID must be unique!!')]

    penaltyid = fields.Integer(string="Penalty id", readonly=True, help="This is the penalty id")
    amount = fields.Float(string="Penalty Amount", required=True, help="This is the penalty amount")
    state = fields.Selection(selection=[('Draft','Draft'),('Confirmed','Confirmed')], default="Draft")
    pay_state = fields.Selection(selection=[('Not Paid','Not Paid'),('Paid','Paid')], default="Not Paid")
    name = fields.Char(compute="_changename")

    reader_id = fields.Many2one("library_app.reader_model", string="Reader", required=True)

    @api.model
    def create(self, vals):
        vals['penaltyid'] = self.env['ir.sequence'].next_by_code('reference.test')
        return super(PenaltyModel, self).create(vals)

    @api.depends("name")
    def _changename(self):
        self.name = "Penalty Id " + str(self.penaltyid)

    @api.constrains("amount")
    def check_amount(self):
        if(self.amount <= 0):
            raise ValidationError("Esta cantidad de dinero no es valida!")
        return True

    def change_state(self):
        self.state = "Confirmed"
        self.reader_id.penaltyamount += self.amount

    def pay(self):
        if(self.state == "Confirmed"):
            if(self.pay_state == "Not Paid"):
                self.pay_state = "Paid"
                self.reader_id.money -= self.amount
                self.reader_id.penaltyamount -= self.amount
            elif(self.reader_id.money < self.reader_id.penaltyamount):
                raise ValidationError("No tiene suficiente dinero para pagar!")
        else:
            raise ValidationError("Primero necesitas confirmar la multa!")