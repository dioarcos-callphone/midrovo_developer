
{
    'name': "POS Receipt Add Fields",
    "description": """Agrega elementos al recibo: 
                        # de factura y 
                        # codigo de acceso (sri)""",
    "summary": "Agrega elementos al recibo",
    "category": "Point of Sale",
    "version": "16.0.1.0.0",
    'author': 'Diego Arcos',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': ['point_of_sale', 'sale', 'account'],
    'data': [
        #'views/res_config_settings.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_receipt_add_fields/static/src/xml/OrderReceiptFields.xml',
            #'pos_receipt_add_fields/static/src/js/pos_order_receipt_fields.js',
            'pos_receipt_add_fields/static/src/js/payment_field.js',
        ]
    },
    'images': ['static/description/icon.png', ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
