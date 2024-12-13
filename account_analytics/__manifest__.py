{
    'name': 'Personalización de Cuentas Analíticas',
    'summary': 'Relación establecida de cuantas analíticas con el punto de emisión',
    'description': """
        - Modulo creado para Odoo Community
        Este modulo permite trabajar con las cuentas analiticas al crear facturas.
    """,
    
    "category": "Account",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone S.A.',
    'website': "https://www.callphoneecuador.com",
    'depends': [ 'account', 'ec_account_edi', 'ec_sri_authorizathions', ],
    'data': [
        'views/sri_printer_point_form.xml',
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}