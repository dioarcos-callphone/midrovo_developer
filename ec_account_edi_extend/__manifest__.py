{
    'name' : 'Ec Extend Account Edi',
    'version' : '16.0',
    'summary': 'Facturacion Electronica',
    'description': """
        - Modulo creado para Odoo 16 Community
        - Lista los documentos del cliente en el portal
        - Documentos disponibles: facturas, notas de crédito, retenciones, guías de remisión y liquidación de compras.
        - Opción para descargar facturas en formato PDF y XML.
        - Se mejora el diseño del mensaje de aviso cuando no hay documentos disponibles.
        - Filtrar por punto de emisión para los usuarios internos. (requerimiento del 20/12/2024)
    """,
    'category': 'Accounting',
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
        'security/documents_security.xml',
        'security/ir.model.access.csv',
        'views/portal_inherited_templates.xml',
        'views/portal_custom_templates.xml',
        'views/user_extend_view.xml',
        'reports/report_invoice_document_extend.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'ec_account_edi_extend/static/src/js/ec_account_portal.js',
            # 'ec_account_edi_extend/static/src/js/download_with_spinner.js',
        ],
        
        'web.assets_backend': [
            'ec_account_edi_extend/static/src/css/spinner.css',
            'ec_account_edi_extend/static/src/js/download_with_spinner.js',
        ]
    },
    
    'installable': True,
    'license': 'LGPL-3',
}