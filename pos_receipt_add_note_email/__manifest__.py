{
    'name': "POS Receipt Add Note & Email",
    "description": """Agrega nota y el email validado en la factura""",
    "summary": "Agrega nota y email en la factura",
    "category": "Point of Sale",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': ['pos_receipt_add_fields', 'point_of_sale', 'sale', 'account'],
    'data': [
        'views/factura.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}