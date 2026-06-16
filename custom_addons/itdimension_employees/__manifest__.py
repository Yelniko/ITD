{
    'name': 'IT-Dimension Employee Custom',
    'version': '1.0',
    'author': '',
    'category': 'Custom/HR',

    'depends': [ 'hr' ],

    'data':
        {
            'security/ir.model.access.csv',
            'views/development_area_views.xml',
            'views/programming_language_views.xml',
            'views/framework_views.xml',
            'views/employee_views.xml'
        },
}