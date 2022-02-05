from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class AuthorModel(models.Model):
    _name = 'library_app.author_model'
    _description = 'Author Model'

    authorid = fields.Integer(string="Author id", readonly=True, help="This is the author id")
    name = fields.Char(string="Author Name", required=True, index=True, help="Author Name")
    surname = fields.Char(string="Surname", index=True, help="Surname")
    year = fields.Char(string="Year", required=True, help="This is the author birthday")
    photo = fields.Binary(string="Photo", help="This is a author photo")

    author_ids = fields.Many2many("library_app.book_model", string="Author", required=True)
                
    @api.model
    def create(self, vals):
        vals['authorid'] = self.env['ir.sequence'].next_by_code('reference.test')
        return super(AuthorModel, self).create(vals)