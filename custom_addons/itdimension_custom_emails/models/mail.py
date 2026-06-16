from odoo import models, fields
from datetime import datetime

class DailyReport(models.Model):
    _name = 'daily.report.generator'

    def _build_report_html(self, employee):
        pass

    def _compute_scheduled_date(self, employee):
        if not employee.end_work_time:
            return False
        hours = int(employee.end_work_time)
        minutes = int(round((employee.end_work_time - hours) * 60))

        name = employee.tz or self.env.user.tz or 'UTC'
        tz = pytz.timezone(name)

        today = fields.Date.context_today(self)
        naive_local = datetime.combine(today, datetime.min.time()) + timedelta(hours=hours, minutes=minutes)
        local_dt = tz.localize(naive_local)

        send_dt_utc = local_dt.astimezone(pytz.utc).replace(tzinfo=None)
        return send_dt_utc - timedelta(minutes=30)

    def generate_daily_reports(self):
        current_date = fields.Date.today()
        employees = self.env['hr.employee'].search([])
        for emp in employees:
            if not emp.work_email:
                continue
            html = self._build_report_html(emp)
            scheduled_date = self._compute_scheduled_date(emp)
            mail_vals = {
                'subject': f'Time Report for {current_date}',
                'email_to': emp.work_email,
                'body_html': html,
            }
            if scheduled_date:
                mail_vals['scheduled_date'] = scheduled_date
            self.env['mail.mail'].create(mail_vals)

    def test(self):
        emp = self.env['hr.employee'].search([('work_email', '=', 'xoleg2006x@gmail.com')], limit=1)
        html = self._build_report_html(emp)
        mail = self.env['mail.mail'].create({
            'subject': f'Time Report for Test',
            'email_to': 'xoleg2006x@gmail.com',
            'body_html': html,
        })
        mail.send(raise_exception=True)