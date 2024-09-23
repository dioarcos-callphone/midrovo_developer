{
    "name": "Inventory Report Location",
    
    "summary": "Reporte de inventario por Ubicación.",
    "description": """
        Muestra el inventario PDF de acuerdo a la categoria de producto y la localidad.
        "
    """,
    
    "category": "Stock",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': [ 'base', 'stock' ],
    'data': [
        'reports/inventory_template.xml',
        'wizards/stock_quantity_hitory.xml',
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}
