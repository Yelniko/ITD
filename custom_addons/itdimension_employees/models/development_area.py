from odoo import models, fields

class DevelopmentArea(models.Model):
    _name = 'development.area'
    _description = 'Development Area'
    name = fields.Char(string='Name', required=True)