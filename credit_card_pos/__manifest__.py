{
    "name": "POS Credit Card",
    
    "summary": "Tarjetas de Crédito para el Punto de Venta",
    "description": """
        - Mantenedor de tarjetas de crédito
        - Check que activa las tarjetas de crédito en los métodos de pago
        - Si el método de pago tiene activo el check se muestra la lista de las tarjetas de crédito disponibles
        - Permite ingresar el RECAP, Autorización y la referencia de la tarjeta
        - La información de la tarjeta de crédito se almacena en los metodos de pago para posterior informes que se quieran realizar
        - Se debe ingresar la información de la tarjeta de crédito antes de colocar el monto del metodo de pago
        - En la lista de los metodos de pago que contienen el check de las tarjetas, se visualiza el nombre de la tarjeta seleccionada
    """,
    
    "category": "POS",
    "version": "16.0.1.0.0",
    "author": "Mauricio Idrovo",
    "company": "Callphone S.A.",
    "website": "https://www.callphoneecuador.com",
    
    "depends": ["point_of_sale", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/credit_card_view.xml",
        "views/pos_payment_method_form.xml",
    ],
    
    "assets": {
        "point_of_sale.assets": [
            "credit_card_pos/static/src/css/style.css",
            "credit_card_pos/static/src/xml/**/*.xml",
            "credit_card_pos/static/src/js/**/*.js",            
        ],
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True,
}