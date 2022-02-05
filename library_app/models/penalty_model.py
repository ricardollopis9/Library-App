from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class PenaltyModel(models.Model):
    _name = 'library_app.penalty_model'
    _description = 'Penalty Model'
    _sql_constraints = [('penalty_unique_penaltyid','UNIQUE(penaltyid)','PENALTY ID must be unique!!')]

    penaltyid = fields.Integer(string="Penalty id", readonly=True, help="This is the penalty id")
    amount = fields.Float(string="Penalty Amount", help="This is the penalty amount")

    reader_id = fields.Many2one("library_app.reader_model", string="Reader", required=True)

    @api.model
    def create(self, vals):
        vals['penaltyid'] = self.env['ir.sequence'].next_by_code('reference.test')
        return super(PenaltyModel, self).create(vals)