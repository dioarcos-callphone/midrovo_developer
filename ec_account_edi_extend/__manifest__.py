{
    'name' : 'Ec Extend Account Edi',
    'version' : '16.0',
    'summary': 'Facturacion Electronica',
    'description': """
        - Modulo creado para Odoo 16 Community
        - Actualizacion del portal de usuario
        - Muestra iconos para descargar facturas pdf y xml
        - Se agrega lista para documentos de notas de credito.
    """,
    'category': 'Accounting',
    'author': 'Mauricio Idrovo',
    "company": "Callphone S.A.",
    "website": "https://www.callphoneecuador.com",
    'images' : [],
    'depends' : [
        'ec_account_edi',
        'account',
        'sale',
        'purchase',
        'account_payment',
        'portal',
        
    ],
    'data': [
        'views/account_portal_template_inh.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'ec_account_edi_extend/static/src/js/ec_account_portal.js',
        ],
    },
    
    'installable': True,
    'license': 'LGPL-3',
}