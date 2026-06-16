from .model import *

def report_migration(env):
    service = connect_table(env)

    status_map_report = get_config_json(env, 'status_map_report')
    spreadsheet_id_rp = get_config(env, 'spreadsheet_reports_id')

    existing_sheets = get_sheet_names(service, spreadsheet_id_rp)
    existing_sheets_set = set(existing_sheets)

    employees = env['hr.employee'].search_read([], ['id', 'name', 'work_email'])

    for employee in employees:
        email = employee['work_email']
        if not email:
            continue

        if email not in existing_sheets_set:
            print(f'Not found reports {email}')
            continue

        data = service.values().get(spreadsheetId=spreadsheet_id_rp, range=email).execute()
        rows = data.get('values', [])
        if not rows:
            print(f'Not found reports {email}')
            continue

        print(f'Found reports {email}')
        headers = rows[0]
        for row in rows[1:]:
            if not row:
                continue

            if not len(row) == 6:
                continue

            d = dict(zip(headers, row))
            project_id = get_or_create(env, 'project.list', d.get('Project Name', ''))
            if not project_id:
                continue

            datatime = d['Date'].split()

            vals = {
                'date': f'{convert_date(datatime[0])} {datatime[1]}',
                'name_developer': employee['id'],
                'name_project': project_id,
                'task': d['Taks(S)'],
                'logged': time_to_float(d['logged time']),
                'status': status_map_report.get(d['Status'], 'not_info')
            }

            env['project.report'].create(vals)