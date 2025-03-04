
{
    'name': "Pos Customer Validated",
    "summary": "Validación de los clientes en el pos y campo NIF actualizado",
    "description": """
        - Módulo diseñado para Odoo 16 Eterprise
        - Se cambia el campo NIF a Número de identificación
        - Se valida que no existan clientes duplicados
        - Se valida que solo exista un cliente
        - Validación de RUC y cédula
        - Se oculta campos (bar code y postal code)
        - Se desactiva el campo vat en el momento que se realizan actualizaciones del cliente
        - Numero de identificacion (CEDULA O RUC) es obligatorio
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
            'pos_customer_validated/static/src/js/vat_disabled.js',
            'pos_customer_validated/static/src/xml/partner_details_edit.xml',
            'pos_customer_validated/static/src/scss/pos.scss',
        ],
    },

    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}

