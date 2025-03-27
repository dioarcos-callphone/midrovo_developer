{
    'name' : 'EC Portal WEB Documentos Electrónicos',
    'version' : '16.0',
    'summary': 'Portal Web de Documentos Electrónicos',
    'description': """
        - Modulo creado para Odoo 16 Community
        - Lista los documentos del cliente en el portal web
        - Documentos disponibles: facturas, notas de crédito, notas de debito, liquidaciones de compras, guías de remisión y retenciones.
        - Opción para descargar facturas en formato PDF y XML.
        - Se mejora el diseño del mensaje de aviso cuando no hay documentos disponibles.
        - Filtrar por punto de emisión para los usuarios internos.
        - Mostrar el estado del documento electronico emitido por el SRI.
    """,
    'category': 'Electronic',
    'author': 'Mauricio Idrovo',
    "company": "Callphone S.A.",
    "website": "https://www.callphoneecuador.com",
    'images' : [],
    'depends' : [
        'ec_account_edi',
        'account',
        'sale',
        'purchase',
        'account_payment',
        'portal',
    ],
    'data': [
        'security/portal_group.xml',
        'security/documents_security.xml',
        'security/ir.model.access.csv',
        'reports/report_invoice_document_extend.xml',
        'templates/email_ec_account_edi_template.xml'
        'templates/portal_template.xml',
        'templates/payment_portal_template.xml',
        'templates/invoice_portal_template.xml',
        'templates/credit_note_portal_template.xml',
        'templates/debit_note_portal_template.xml',
        'templates/liquidation_portal_template.xml',
        'templates/remission_portal_template.xml',
        'templates/retention_portal_template.xml',
        'views/user_extend_view.xml',
        'views/invoice_view.xml',
        
    ],
    'assets': {
        'web.assets_frontend': [
            'electronic_document_portal/static/src/js/ec_account_portal.js',
        ],
    },
    
    'installable': True,
    'license': 'LGPL-3',
}