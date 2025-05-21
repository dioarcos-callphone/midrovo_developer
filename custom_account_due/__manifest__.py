{
    'name': 'Custom Account Due',
    'version': '16.0.1.0.0',
    'description': '''
        Modulo desarrollado en Odoo 16 Enterprise
        Especificaciones:
            - Presenta reporte de saldo por vencer
    ''',
    'summary': 'Reporte de saldo por vencer',
    'author': 'Mauricio Idrovo',
    'website': 'http://www.callphoneecuador.com',
    'license': 'LGPL-3',
    'category': 'account',
    'depends': [
        'account_due'
    ],
    'data': [
        'wizard/account_due_wizard.xml'
    ],
    # 'demo': [
    #     ''
    # ],
    'installable': True,
    'auto_install': True,
    'application': False,
    # 'assets': {
        
    # }
}