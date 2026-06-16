from odoo import fields, models

class ProjectReport(models.Model):
    _name = 'project.report'
    _description = 'Project Report'

    date = fields.Datetime(string="Date")
    name_developer = fields.Many2one('hr.employee', string='Developer')
    name_project = fields.Many2one('project.list', string='Project')
    task = fields.Char(string='Task(s)')
    logged = fields.Float(string='Logged')
    status = fields.Selection([('not_info', '-'), ('done', 'Done'),
                               ('in_progress', 'In Progress'),],
                              string="Status", default='not_info')