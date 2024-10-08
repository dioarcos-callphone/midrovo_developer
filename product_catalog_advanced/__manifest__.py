{
    "name": "Product Catalog Advanced",
    
    "summary": "Optimizacion y Personalizacion Nueva del Catalogo de Productos.",
    "description": """
        Quita los espacios en blanco
    """,
    
    "category": "Product Template",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': [ 'base', 'sale_management', 'stock', 'web' ],
    'data': [
        "reports/report_product_catalog.xml",
        "reports/product_catalog_template.xml",
        "views/view_product_catalog.xml",
        "views/assets.xml"
    ],
    
    'assets': {
        'web.assets_backend': [
            'product_catalog_advanced/static/src/css/style.css'
        ]
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}
