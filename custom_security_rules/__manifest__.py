{
    'name': 'Custom Security',
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
        'web.asset.backend': [
            'custom_security_rules/static/src/js/custom_security_res_partner.js',
            'custom_security_rules/static/src/xml/show_save_buttons_partner.xml',
        ]
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}
