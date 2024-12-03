{
    'name': '',
    'summary': '',
    'description': """

    """,
    
    "category": "Account Move",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone S.A.',
    'website': "https://www.callphoneecuador.com",
    'depends': [ 'account', 'point_of_sale', 'invoice_details_view' ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/account_due_wizard.xml',
        'report/account_due_report.xml',
        'report/account_due_template.xml',
    ],
    
    'assets': {
        'web.assets_backend': [
            # 'invoice_details_view/static/src/js/action_manager.js',
            'account_due/static/src/css/style.css'
        ]
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}