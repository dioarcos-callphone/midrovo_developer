{
    "name": "Plantilla de Reportes de Facturas",
    "summary": "Diseño mejorado de los reportes de factura",
    "description": """
        - Modulo desarrollado para Odoo 16 Enterprise
        - Actualización del template de los reportes de factura
        - Mejorar la vista del archivo PDF
        - Dependencias requeridas: account.move
    """,
    
    "category": "Invoice Report",
    "version": "16.0.1.0.0",
    "author": "Mauricio Idrovo",
    'company': 'Callphone S.A.',
    'website': "https://www.callphoneecuador.com",
    'depends': [ 'account', 'point_of_sale', ],
    'data': [
        "views/paper_format_account_invoice.xml",
        "views/report_invoice_document.xml",
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': True,
}