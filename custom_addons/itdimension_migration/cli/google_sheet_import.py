import argparse
import odoo
from odoo.cli import Command
from odoo.addons.itdimension_migration.cli.employee import employee_migration
from odoo.addons.itdimension_migration.cli.project import project_migration
from odoo.addons.itdimension_migration.cli.report import report_migration

class google_sheet_import(Command):
    def run(self, args):
        parser = argparse.ArgumentParser(
            prog='odoo-bin google-sheet-import',
            description='Import data from google sheet',
        )
        parser.add_argument('-d', '--database', required=True, help='Database name')
        parser.add_argument('--task', choices=['employee', 'projects', 'reports', 'all'], default='all')
        parsed = parser.parse_args(args)

        registry = odoo.modules.registry.Registry.new(parsed.database)
        with registry.cursor() as cr:
            env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
            if parsed.task in ('employee', 'all'):
                print("===Migration employee===")
                employee_migration(env)

            if parsed.task in ('projects', 'all'):
                print("===Migration projects===")
                project_migration(env)

            if parsed.task in ('reports', 'all'):
                print("===Migration reports===")
                report_migration(env)

            cr.commit()

        print("Done!")