{
    'name': 'Withhold Config',
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
    'category': 'settings',
    'depends': [
        'l10n_ec_edi'
    ],

    'installable': True,
    'auto_install': True,
    'application': False,

}