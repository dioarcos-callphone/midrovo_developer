{
    "name": "POS Credit Card",
    
    "summary": "",
    "description": """
    
    """,
    
    "category": "POS",
    "version": "16.0.1.0.0",
    "author": "Mauricio Idrovo",
    "company": "Callphone S.A.",
    "website": "https://www.callphoneecuador.com",
    
    "depends": ["point_of_sale"],
    "data": [
    
    ],
    
    "assets": {
        "point_of_sale.assets": [
            "credit_card_pos/static/src/js/Screens/PaymentScreen/CustomPaymentScreen.js",
            # "credit_card_pos/static/src/xml/Popups/CreditCardListPopup.xml",
        ],
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}