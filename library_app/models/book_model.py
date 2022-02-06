from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class BookModel(models.Model):
    _name = 'library_app.book_model'
    _description = 'Book Model'
    _sql_constraints = [('book_unique_bookid','UNIQUE(bookid)','BOOK ID must be unique!!')]

    bookid = fields.Integer(string="Book id", readonly=True, index=True, help="This is the book id")
    title = fields.Char(string="Book Name", required=True, index=True, help="Book Name")
    gender = fields.Selection(string="Gender", required=True, selection=[('Theater','Theater'), ('Novel','Novel'), ('Poetry','Poetry'), ('Scary','Scary'), ('', '')], default='', help="This is the book categories")
    year = fields.Integer(string="Year", required=True, size=4, help="This is the book year")
    photo = fields.Binary(string="Photo", help="This is a book photo")
    stock = fields.Integer(string='Stock', required=True, help="Book quantity", default = 0, store=True)
    name = fields.Char(compute="_changename")

    rent_ids = fields.One2many("library_app.rent_model", "book_id", string="Rent", required=True)
    book_ids = fields.Many2many("library_app.author_model", string="Author", required=True)

    @api.constrains("gender")

    def check_category(self):
        if(self.gender == ''):
            raise ValidationError("You must select a book gender.")
        else:
            return True

    @api.model
    def create(self, vals):
        vals['bookid'] = self.env['ir.sequence'].next_by_code('reference.test')
        return super(BookModel, self).create(vals)

    @api.depends("name")
    def _changename(self):
        self.name = self.title