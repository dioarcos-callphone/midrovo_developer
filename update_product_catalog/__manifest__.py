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
    'depends': [ 'amf_product_catalog', 'sale', 'stock' ],
    'data': [
        'report/product_catalog_template.xml',
        'wizard/view/view_wizard_error.xml',
        'wizard/record_wizard_error.xml',
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}
