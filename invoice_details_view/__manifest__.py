{
    'name': 'Invoice Details View',
    'summary': 'Modulo que filtra desde un wizard y genera informe de los detalles de facturas',
    'description': """
        - Módulo diseñado para Odoo 16 Eterprise
        Este modulo realiza los siguientes detalles:
        - El wizard filtra por rango de fecha, diario contable, comercial, sales person
        - Contiene opciones para traer el informe segun el costo
        - Cuando genere el informe seleccione los registros y de click en PDF o EXCEL
        - Muestra el tipo si es factura o nota de credito
        - Los usuarios que pertenecen al grupo group_invoice_details_view_user no tienen permitido ver el costo, total costo y rentabilidad.
        - Genera informe de facturas y notas de credito resumido y detallado
        - Muestra metodos de pago
        - Se actualiza el modulo, ahora los reportes de detalle de factura generados en excel muestran la hora de la factura, categoria, estilo, SKU del producto, porcentaje de descuento, total neto y datos del cliente.
    """,
    
    "category": "Account Move",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone S.A.',
    'website': "https://www.callphoneecuador.com",
    'depends': [ 'account', 'point_of_sale', 'base', 'web' ],
    'data': [
        'security/groups/security_group_data.xml',
        'security/ir.model.access.csv',
        'wizard/invoice_details_wizard.xml',
        'report/invoice_details_report.xml',
        'report/invoice_details_template.xml',
    ],
    
    'assets': {
        'web.assets_backend': [
            'invoice_details_view/static/src/js/action_manager.js',
            'invoice_details_view/static/src/css/style.css'
        ]
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}