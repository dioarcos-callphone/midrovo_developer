{
    'name': 'Custom Security',
    
    "summary": "Restriccion de modificacion para el sale order line y res partner",
    "description": """
        - No permite actualizar precios unitarios de la orden de venta
        - Restringe confirmacion de factura y despacho, no permite eliminar el stock picking
        - Restringe actualizacion en el modulo de contactos (res_partner)
        - Los grupos definidos son group_custom_security_role_user (No actualizar contactos)
        group_custom_security_role_user_2 (No confirmar facturas ni despachos)
        
    """,
    
    'version': '1.0',
    'author': 'Mauricio Idrovo',
    'company': 'Callphone S.A.',
    'website': "https://www.callphoneecuador.com",
    'depends': ['base', 'sale', 'contacts', 'sale_management', 'stock'],
    'data': [
        'security/groups/security_groups_data.xml',
        'security/rules/security_rules_data.xml',
        'security/ir.model.access.csv',
        'views/sale_order_form.xml',
        'views/stock_picking_form.xml',
        # 'views/res_partner_form.xml'
        
    ],
    
    # 'assets': {
    #     'web.assets_backend': [
    #         'custom_security_rules/static/src/xml/form_status_indicator.xml',         
    #     ]
    # },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}
