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
    'depends': [ 'account', ],
    'data': [
        'wizard/invoice_details_wizard.xml',
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}