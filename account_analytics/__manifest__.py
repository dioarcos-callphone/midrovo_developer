{
    'name': 'Personalización de Cuentas Analíticas',
    'summary': 'Relación establecida de cuantas analíticas con el diario contable',
    'description': """
        Este modulo permite trabajar con las cuentas analiticas al crear facturas.
    """,
    
    "category": "Account",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone S.A.',
    'website': "https://www.callphoneecuador.com",
    'depends': [ 'account', ],
    'data': [
        'views/journal_form_inherit.xml',
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}