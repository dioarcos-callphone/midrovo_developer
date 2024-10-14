{
    'name': 'Custom Security',
    'version': '1.0',
    'author': 'Mauricio Idrovo',
    'company': 'Callphone S.A.',
    'website': "https://www.callphoneecuador.com",
    'depends': ['base', 'sale', 'contacts', 'sale_management'],
    'data': [
        'security/custom_security_access.xml',
        'security/ir.model.access.csv',
        'data/rules.xml',
        'views/res_partner_form.xml',
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}
