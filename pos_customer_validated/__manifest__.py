
{
    'name': "Pos Customer Validated",
    "summary": "Validación de los clientes en el pos y campo NIF actualizado",
    "description": """
        - Se cambia el campo NIF a Número de identificación
        - Se valida que no existan clientes duplicados
        - Se valida que solo exista un cliente
        - Validación de RUC y cédula
    """,
    "category": "Point of Sale",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': ['point_of_sale','contacts', "l10n_ec", "l10n_latam_invoice_document", "l10n_latam_base",],
    'data': [],
    
    'assets': {
        'point_of_sale.assets': [
            'pos_customer_validated/static/src/js/customer_validation.js',
            'pos_customer_validated/static/src/xml/partner_details_edit.xml',
            'pos_customer_validated/static/src/scss/pos.scss',
        ],
    },

    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
