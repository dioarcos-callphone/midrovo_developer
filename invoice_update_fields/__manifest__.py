
{
    'name': "Invoice Update Fields",
    "summary": "Visualizacion del Cashier o Usuario Odoo, email del cliente, nota de vendedor, métodos de pago",
    "description": """
        - Módulo diseñado para Odoo 16 Eterprise
        Este modulo añade funcionalidad para las facturas generadas en los modulos POS y Contabilidad,
        mostrando el respectivo vendedor que se loguea en ambos, tambien muestra el email del cliente
        y la nota que realiza el vendedor, oculta los términos y condiciones, se actualizan los métodos de pago.
    """,
    "category": "Point of Sale",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': ['pos_receipt_add_fields', 'pos_payment_sri', 'point_of_sale', 'sale', 'l10n_ec_edi', 'l10n_ec', 'account_move_sri', 'account'],
    'data': [
        'views/invoice_update.xml'
    ],

    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
