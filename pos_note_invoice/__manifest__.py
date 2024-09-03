{
    "name": "Pos Note Invoice",
    
    "summary": "Visualización general del comentario o nota de la factura",
    "description": """
        Se añade nota general para que pueda ser visualizada en la factura
    """,
    
    "category": "Point of Sale",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': ['point_of_sale', 'account', 'sale', 'invoice_update_fields', 'account_move_sri'],
    'data': [],
    
    "assets": {
        "point_of_sale.assets": [
            'pos_note_invoice/static/src/js/order_line_note_button.js',
            'pos_note_invoice/static/src/js/payment_fields.js',
            'pos_note_invoice/static/src/js/note_service.js',
            # 'pos_note_invoice/static/src/js/pos_order_note.js',
            'pos_note_invoice/static/src/xml/order_line_note_button.xml',
        ],
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
