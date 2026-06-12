from odoo import models, fields

class Projects(models.Model):
    _name = 'project.list'
    _description = 'Projects'
    name = fields.Char(string="Projects Name", required=True)