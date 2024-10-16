{
    'name': 'Custom Security',
    'version': '1.0',
    'author': 'Mauricio Idrovo',
    'company': 'Callphone S.A.',
    'website': "https://www.callphoneecuador.com",
    'depends': ['base', 'sale', 'contacts', 'sale_management'],
    'data': [
        'security/groups/security_groups_data.xml',
        'security/rules/security_rules_data.xml',
        'security/ir.model.access.csv',
        'views/sale_order_form.xml'
    ],
    
    'assets': {
        'web.assets_backend': [
            'custom_security_rules/static/js/custom_security_res_partner',
            'custom_security_rules/static/xml/show_save_buttons_partner',
        ]
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}
