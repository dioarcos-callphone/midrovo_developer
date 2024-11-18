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
        "security/ir.model.access.csv",
        "views/credit_card_view.xml",
        "views/pos_payment_method_form.xml",
    ],
    
    "assets": {
        "point_of_sale.assets": [
            "credit_card_pos/static/src/css/style.css",
            "credit_card_pos/static/src/js/Screens/PaymentScreen/CustomPaymentScreen.js",
            "credit_card_pos/static/src/js/Popup/RecapAuthPopup.js",
            # "credit_card_pos/static/src/js/Misc/NumberBufferExtend.js",
            "credit_card_pos/static/src/xml/Popup/RecapAuthPopup.xml",
            "credit_card_pos/static/src/js/PosGlobalStateExtend.js",
            "credit_card_pos/static/src/xml/PaymentScreen/PaymentScreenPaymentLinesInherit.xml",
        ],
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}