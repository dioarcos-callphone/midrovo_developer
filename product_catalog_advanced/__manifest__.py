{
    "name": "Product Catalog Advanced",
    
    "summary": "Optimizacion y Personalizacion Nueva del Catalogo de Productos.",
    "description": """
        - Modulo creado para Odoo 16 Community
        Quita los espacios en blanco
    """,
    
    "category": "Product Template",
    "version": "16.0.1.0.0",
    "author": "Mauricio Idrovo",
    "company": "Callphone SA",
    "website": "https://www.callphoneecuador.com",
    "depends": [
        "sale_management",
        "stock"
    ],
    "data": [
        "reports/report_product_catalog.xml",
        "reports/product_catalog_template.xml",
        "views/view_product_catalog.xml"
    ],
    
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False
}
