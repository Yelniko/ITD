from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    development_area_id = fields.Many2many(
        'development.area',
        relation='employee_development_areas',
        column1='employee_id',
        column2='development_area_id',
        string='Development Area'
    )

    key_development_area_id = fields.Many2many(
        'development.area',
        relation='employee_key_development_areas',
        column1='employee_id',
        column2='development_area_id',
        string='Key Development Area'
    )

    programming_language_id = fields.Many2many(
        'programming.language',
        relation='employee_programming_languages',
        column1='employee_id',
        column2='programming_language_id',
        string='Programming Language'
    )

    key_programming_language_id = fields.Many2many(
        'programming.language',
        relation='employee_key_programming_languages',
        column1='employee_id',
        column2='programming_language_id',
        string='Key Programming Language'
    )

    key_framework = fields.Many2many(
        'key.framework',
        string='Key Framework',
    )

    start_work_time = fields.Float(
        string='Start Work Time',
    )

    end_work_time = fields.Float(
        string='End Work Time',
    )
