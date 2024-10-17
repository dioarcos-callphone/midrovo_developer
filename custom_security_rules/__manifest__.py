{
    'name': 'Custom Security',
    
    "summary": "Restriccion de modificacion para el sale order line y res partner",
    "description": """
        No permite actualizar precios unitarios de la orden de venta y tambien restringe actualizacion
        en el modulo de contactos (res_partner)
    """,
    
    'version': '1.0',
    'author': 'Mauricio Idrovo',
    'company': 'Callphone S.A.',
    'website': "https://www.callphoneecuador.com",
    'depends': ['base', 'sale', 'contacts', 'sale_management',],
    'data': [
        'security/groups/security_groups_data.xml',
        'security/rules/security_rules_data.xml',
        'security/ir.model.access.csv',
        'views/sale_order_form.xml'
    ],
    
    'assets': {
        'web.assets_backend': [
            'custom_security_rules/static/src/js/custom_security_res_partner.js',         
        ]
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}
