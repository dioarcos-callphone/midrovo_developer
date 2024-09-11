{
    "name": "Update Product Catalog",
    
    "summary": "Actualiación en el diseño del catalogo de productos.",
    "description": """
        - Actualización del diseño del catalogo de productos.
        - Muestra productos por variantes y no variantes.
        - Este modulo se centra más a los productos cuyas variantes son de tipo color y talla
        - Solo acepta atributos "color" y "tallas"
    """,
    
    "category": "Sales",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': [ 'amf_product_catalog', 'sale', ],
    'data': [
        'report/product_catalog_template.xml', 
    ],
    
    'assets': {
        'web.report_assets_common': [
            'update_product_catalog/static/src/css/style_catalog.css',
        ],
        # 'web.report_assets_pdf': [
        #     'update_product_catalog/static/src/css/style_catalog_pdf.css',
        # ],
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}
