{
    'name': 'Invoice Details View',
    'summary': 'Modulo que filtra desde un wizard y genera informe de los detalles de facturas',
    'description': """
        Este modulo realiza los siguientes detalles:
        - El wizard filtra por rango de fecha, diario contable, comercial, sales person
        - La vista tree del account move line muestra los detalles de la factura
        - Cuando genere el informe seleccione los registros y de click en PDF
    """,
    
    "category": "Account Move",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone S.A.',
    'website': "https://www.callphoneecuador.com",
    'depends': [ 'account', 'point_of_sale' ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/invoice_details_wizard.xml',
        'report/invoice_details_report.xml',
        'report/invoice_details_template.xml',
    ],
    
    'assets': {
        'web.assets_backend': [
            'invoice_details_view/static/src/css/style.css']
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}