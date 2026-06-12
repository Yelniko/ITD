from odoo import models, fields

class ProgrammingLanguage(models.Model):
    _name = 'programming.language'
    _description = 'Programming Language'
    name = fields.Char(string='Name', required=True)