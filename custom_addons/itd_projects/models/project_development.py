from odoo import models, fields

class ProjectsDevelopment(models.Model):
    _name = 'project.development'
    _description = 'Project nad development'
    name_project = fields.Many2one('project.list', string='Project')
    name_developer = fields.Many2one('hr.employee', string='Developer')
    status = fields.Selection([('available', 'Available'), ('unavailable', 'Unavailable'),
                               ('on_vacation', 'On Vacation'), ('project_completed', 'Project Completed')],
                              string="Status", default='available')

