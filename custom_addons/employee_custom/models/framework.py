from odoo import models, fields

class KeyFramework(models.Model):
    _name = 'key.framework'
    _description = 'Key Framework'
    name = fields.Char(string='Name', required=True)