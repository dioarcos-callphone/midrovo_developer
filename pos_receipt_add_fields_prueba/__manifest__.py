
{
    'name': "POS Receipt Add Fields Prueba",
    "description": """Agrega nombre del cajero logueado a la factura""",
    "summary": "Agrega elementos al recibo",
    "category": "Point of Sale",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': ['pos_receipt_add_fields', 'point_of_sale', 'sale', 'account'],
    'data': [
        # 'views/report/factura.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_receipt_add_fields_prueba/static/src/js/payment_field.js',
            # 'pos_receipt_add_fields_prueba/static/src/xml/factura.xml',
        ]
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
