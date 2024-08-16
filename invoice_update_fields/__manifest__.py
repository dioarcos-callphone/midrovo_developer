
{
    'name': "Invoice Update Fields",
    "summary": "Visualizacion del Cashier o Usuario Odoo, email del cliente y nota de vendedor",
    "description": """
        Este modulo añade funcionalidad para las facturas generadas en los modulos POS y Contabilidad,
        mostrando el respectivo vendedor que se loguea en ambos, tambien muestra el email del cliente
        y la nota que realiza el vendedor, oculta los términos y condiciones.
    """,
    "category": "Point of Sale",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': ['pos_receipt_add_fields', 'point_of_sale', 'sale', 'account'],
    'data': [
        'views/invoice_update.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
