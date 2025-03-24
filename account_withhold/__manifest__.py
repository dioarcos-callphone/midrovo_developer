{
    'name': 'Account Withhold Util',
    'version': '1.0',
    'description': '''
        - Modulo desarrollado para Odoo 16 EE
        - Soluciona el problema con totals.subtotals_order cuando se realiza retenciones de facturas de clientes
    ''',
    'summary': 'Retenciones de Facturas de Clientes',
    'author': 'Mauricio Idrovo',
    'company': 'Callphone S.A.',
    'website': 'https://www.callphoneecuador.com',
    'license': 'LGPL-3',
    'category': 'account',
    'depends': [
        'account'
    ],
    # 'data': [
    #     ''
    # ],
    # 'demo': [
    #     ''
    # ],
    'installable': True,
    'auto_install': True,
    'application': False,
    # 'assets': {
    #     'web.assets_backend': [
    #         'account_withhold/static/src/components/**/*',
    #     ],
    # }
}