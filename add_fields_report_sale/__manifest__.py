{
    "name": "Add Fields Report Sale",
    
    "summary": "Columna Adicional en el Reporte de Cotizaciones",
    "description": """

        (Odoo 16 Enterprise)
        Este modulo personaliza el reporte de cotizaciones, añadiendo una columna de las imágenes del producto.
    
    """,
    
    "category": "Sale Report",
    "version": "16.0.1.0.0",
    "author": "Mauricio Idrovo",
    "company": "Callphone S.A.",
    "website": "https://www.callphoneecuador.com",
    
    "depends": [ "sale", "base", ],
    "data": [
        "report/sale_report_template.xml",
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
    
}