{
    'name': 'Custom Sale Order and Partner Security',
    'version': '1.0',
    'category': 'Sales',
    'author': 'Mauricio Idrovo',
    'company': 'Callphone S.A.',
    'website': "https://www.callphoneecuador.com",
    'depends': ['sale', 'contacts'],
    'data': [
        'data/groups.xml',
        'security/ir.model.access.csv',
        'security/sale_order_rules.xml',
        'security/res_partner_rules.xml',
        
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}
