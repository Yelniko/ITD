from .model import *
from google.oauth2 import service_account
from googleapiclient.discovery import build

def employee_migration(env):
    service = connect_table(env)
    
    spreadsheet_id_em = get_config(env, 'spreadsheet_employees_id')
    spreadsheet_id_db = get_config(env, 'spreadsheet_birthdays_id')
    spreadsheet_id_tw = get_config(env, 'spreadsheet_working_hours_id')
    sheet_name_em = get_config(env, 'spreadsheet_employees_sheet')
    sheet_name_db = get_config(env, 'spreadsheet_birthdays_sheet')
    sheet_name_tw = get_config(env, 'spreadsheet_working_hours_sheet')

    data_em = service.values().get(spreadsheetId=spreadsheet_id_em, range=sheet_name_em).execute()
    data_db = service.values().get(spreadsheetId=spreadsheet_id_db, range=sheet_name_db).execute()
    data_tw = service.values().get(spreadsheetId=spreadsheet_id_tw, range=sheet_name_tw).execute()
    rows_em = data_em.get('values', [])
    rows_db = data_db.get('values', [])
    rows_tw = data_tw.get('values', [])

    em = []
    tw = {}
    db = {}

    for i in range(1, len(rows_tw)):
        if len(rows_tw[i]) == 2:
            rows_tw[i].append('00:00')
            rows_tw[i].append('00:00')
        tw[rows_tw[i][0]] = [rows_tw[i][2], rows_tw[i][3]]

    for i in range(1, len(rows_em)):
        for _ in range(len(rows_em[0])-len(rows_em[i])):
            rows_em[i].append('')
        lis = {}
        for j in range(len(rows_em[0])):
            lis[rows_em[0][j]] = rows_em[i][j]
        em.append(lis)

    for i in rows_db[1:]:
        db[i[0]] = i[1]

    for row in em:
        print(row['Email'], end=' - ')
        if row['Email'] in tw:
            row['Time'] = tw[row['Email']]
        else:
            row['Time'] = ['00:00', '00:00']

        vals = {
            "name":       row['Full name'],
            "work_email": row['Email'],
            "work_phone": row['Phone number'],

            "development_area_id":         many2many_ids(env, "development.area",     row['Development area']),
            "key_development_area_id":     many2many_ids(env,"development.area",     row['Key area']),
            "programming_language_id":     many2many_ids(env,"programming.language", row['Programming languages']),
            "key_programming_language_id": many2many_ids(env,"programming.language", row['Key languages']),
            "key_framework":               many2many_ids(env,"key.framework",        row['Key frameworks']),

            "start_work_time": time_to_float(row['Time'][0]),
            "end_work_time":   time_to_float(row['Time'][1]),

            "birthday": convert_date(db.get(row['Full name'], ''))
        }

        existing = env['hr.employee'].search([('name', '=', row['Full name'])], limit=1)

        if existing:
            existing.write(vals)
            print('Updated employee')
        else:
            env['hr.employee'].create(vals)
            print('Created employee')