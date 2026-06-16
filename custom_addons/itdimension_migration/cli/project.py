from .model import *

def project_migration(env):
    status_map = get_config_json(env, 'status_map')
    service = connect_table(env)

    spreadsheet_id = get_config(env, 'projects_id')
    sheet_name = get_config(env, 'spreadsheet_projects_sheet')

    data = service.values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
    rows = data.get('values', [])

    header = rows[1]

    for row in rows[2:]:

        project_name = row[0]
        if not project_name:
            continue

        project_id = get_or_create(env, 'project.list', project_name)

        for col_in in range(2, len(header)):
            email = header[col_in].strip()
            cell = row[col_in].strip() if col_in < len(row) else ''
            if not cell:
                continue

            status = status_map.get(cell)
            if not status:
                print(f'NOT Status {cell}')
                continue

            employee = env['hr.employee'].search([('work_email', '=', email)], limit=1)
            if not employee:
                print(f'Not found employee {email}')
                continue

            existing = env['project.development'].search([
                ('name_project', '=', project_id),
                ('name_developer', '=', employee.id)
            ])

            vals = {
                'name_project': project_id,
                'name_developer': employee.id,
                'status': status
            }

            if existing:
                existing.write(vals)
            else:
                env['project.development'].create(vals)