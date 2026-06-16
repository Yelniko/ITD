from google.oauth2 import service_account
from googleapiclient.discovery import build
import json


def get_config(env, key, default=None):
    return env['ir.config_parameter'].sudo().get_param(f'migration.{key}', default)

def get_config_json(env, key, default=None):
    value = env['ir.config_parameter'].sudo().get_param(f'migration.{key}')
    if not value:
        return default
    return json.loads(value)

def connect_table(env):
    creds_path = get_config(env, 'service_account_file')
    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=[get_config(env, 'scopes')])
    return build("sheets", "v4", credentials=creds).spreadsheets()

def get_sheet_names(service, spreadsheet_id):
    spreadsheet = service.get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet.get('sheets')
    return [s['properties']['title'] for s in sheets]

def get_or_create(env, model_name, name):
    if not name.strip():
        return None
    record = env[model_name].search([('name', '=', name.strip())], limit=1)
    if record:
        return record.id
    return env[model_name].create({'name': name.strip()}).id

def many2many_ids(env, model, cell_value):
    if not cell_value:
        return [(6, 0, [])]
    names = [n.strip() for n in cell_value.split(',') if n.strip()]
    ids = [get_or_create(env, model, name) for name in names]
    ids = [i for i in ids if i]
    return [(6, 0, ids)]

def convert_date(date_str):
    if not date_str.strip():
        return False
    d, m, y = date_str.split('.')
    return f'{y}-{m}-{d}'

def time_to_float(time_str):
    if not time_str.strip():
        return 0.0
    try:
        hours, minutes = time_str.split(':')
        return int(hours) + int(minutes) / 60
    except Exception:
        return 0.0