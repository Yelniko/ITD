import pytz
from odoo import models, fields
from datetime import datetime, timedelta

class DailyReport(models.Model):
    _name = 'daily.report.generator'

    def _build_report_html(self, employee):
        projects = self.env['project.development'].search([('name_developer', '=', employee.id)])

        html = """
            <html>
            <head></head>
            <body style="margin: 0; padding: 0;">
            <div style="font-family: Roboto, Arial, Helvetica, sans-serif; font-size: 13px; color: #333333;">
            <div style="color: #4472c4; font-weight: bold; font-size: 15px; margin-bottom: 20px;">
                Status: 0 – in process, 0 – done.
            </div>
            """

        for project in projects:
            if not project.status == 'available':
                continue

            html += f"""
                <h2 style="color: #4472c4; margin-top: 20px; margin-bottom: 10px; font-size: 20px;">
                Project: {project.name_project.name}
                </h2>
                <table width="100%" cellpadding="6" cellspacing="0" style="border-collapse: collapse; border: none; margin-bottom: 30px;">
                    <tr style="background-color: #4472c4; color: #ffffff; text-align: left;">
                        <th style="border: 1px solid #ffffff; font-weight: bold;">Task</th>
                        <th style="border: 1px solid #ffffff; font-weight: bold; width: 15%;">Time (hh:mm)</th>
                        <th style="border: 1px solid #ffffff; font-weight: bold; width: 10%;">Status</th>
                    </tr>
                """

            for i in range(4):
                bg_color = "#e9edf4" if i % 2 == 0 else "#ffffff"
                html += (f'<tr style="background-color: {bg_color};">'
                         f'<td style="border: 1px solid #ffffff; font-weight: bold;"> </td>'
                         f'<td style="border: 1px solid #ffffff; font-weight: bold;"> </td>'
                         f'<td style="border: 1px solid #ffffff; font-weight: bold;"> </td>'
                         f'</tr>')

            html += '</table>'

        html += '</body></html>'

        return html

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