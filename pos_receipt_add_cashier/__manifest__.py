
{
    'name': "POS Receipt Add Cashier",
    "description": """Agrega nombre del cajero logueado a la factura""",
    "summary": "Agrega nombre del cajero",
    "category": "Point of Sale",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': ['pos_receipt_add_fields', 'point_of_sale', 'sale', 'account'],
    'data': [
        # 'views/factura.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_receipt_add_cashier/static/src/js/payment_field.js',
        ]
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
