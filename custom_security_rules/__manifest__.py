{
    'name': 'Custom Security',
    'version': '1.0',
    'author': 'Mauricio Idrovo',
    'company': 'Callphone S.A.',
    'website': "https://www.callphoneecuador.com",
    'depends': ['base', 'sale', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'security/custom_security_access.xml',
    ],
    'installable': True,
    'application': True,
}
