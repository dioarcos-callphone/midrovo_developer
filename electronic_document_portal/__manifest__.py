{
    'name' : 'EC Portal WEB Documentos Electrónicos',
    'version' : '16.0',
    'summary': 'Portal Web de Documentos Electrónicos',
    'description': """
        - Modulo creado para Odoo 16 Community
        - Lista los documentos del cliente en el portal web
        - Documentos disponibles:
            - Facturas,
            - Notas de crédito,
            - Notas de débito,
            - Liquidaciones de compras
            - Guías de remisión
            - Retenciones
        - Descarga de documentos en formato PDF y XML.
        - Mejoras en el diseño del portal.
        - Configuración de punto de emision a usuarios internos.
        - Visualización de estados del SRI y de EMAIL.
        - Grupos de acceso:
            - Eliminar documentos ya publicados (usuario interno)
            - No eliminar documentos (usuario interno)
            - Enviar e imprimir documentos (usuario interno)
        - Mejora de las vistas form de los documentos.
        - Enviar e imprimir con los documentos estándar del modulo ec_account_edi.
        - Visualización de mensajes informativos del SRI y mejora de la pestaña Documentos electrónicos de los notebook FORM.
        - Replicación de métodos para enviar e imprimir y estado de enviado a email en account.remision y account.withhold.
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
        'data/templates/email_ec_account_edi_template.xml',
        'templates/sri_state_template.xml',
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
        'views/remission_view.xml',
        'views/withhold_view.xml',
        'wizard/account_remission_send.xml',
        'wizard/account_withhold_send.xml',
        
    ],
    'assets': {
        'web.assets_frontend': [
            'electronic_document_portal/static/src/js/ec_account_portal.js',
        ],
    },
    
    'installable': True,
    'license': 'LGPL-3',
}