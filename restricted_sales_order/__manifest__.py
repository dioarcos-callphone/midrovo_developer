{
    'name': 'Restricted Sales Order',
    'version': '16.0.1.0.0',
    'description': '''
        Modulo desarrollado para Odoo 16 Enterprise
        Especificaciones:
            - Oculta el boton de cancelar
    ''',
    'summary': 'Restricción del pedido de venta',
    'author': 'Mauricio Idrovo',
    'website': 'https://www.callphoneecuador.com',
    'license': 'LGPL-3',
    'category': 'sale',
    'depends': [
        'sale'
    ],
    'data': [
        # 'views/sale_order_view.xml',
    ],
    'auto_install': True,
    'installable': True,
    'application': False,
}