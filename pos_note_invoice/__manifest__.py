{
    "name": "Pos Note Invoice",
    
    "summary": "Visualización general del comentario o nota de la factura",
    "description": """
        - Módulo diseñado para Odoo 16 Eterprise
        - Se añade nota general para que pueda ser visualizada en la factura
        - Actualización del narration en el POS
        - La nota que se ingresa debe tener un mínimo de 500 caracteres.
    """,
    
    "category": "Point of Sale",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': [ 'point_of_sale', 'account', ],
    'data': [],
    
    "assets": {
        "point_of_sale.assets": [
            'pos_note_invoice/static/src/js/order_line_note_button.js',
            'pos_note_invoice/static/src/js/pos_global_state.js',
            'pos_note_invoice/static/src/js/note_service.js',
            'pos_note_invoice/static/src/xml/order_line_note_button.xml',
        ],
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
