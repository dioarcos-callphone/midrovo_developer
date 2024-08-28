
{
    'name': "Pos Customer Validated",
    "summary": "Validación de los clientes en el pos y campo NIF actualizado",
    "description": """
        - Se cambia el campo NIF a Número de identificación
        - Se valida que no existan clientes duplicados
        - Se valida que solo exista un cliente
    """,
    "category": "Point of Sale",
    "version": "16.0.1.0.0",
    'author': 'Mauricio Idrovo',
    'company': 'Callphone sa',
    'website': "https://www.callphoneecuador.com",
    'depends': ['point_of_sale','contacts'],
    'data': [
        # 'views/partner_details_edit.xml'
    ],
    
    'qweb': [
        'static/src/xml/partner_details_edit.xml'
    ],
    
    'assets': {
        # 'point_of_sale.assets': [
        #     'pos_customer_validated/static/src/models.js'  
        # ],
        'web.assets_qweb': [
            'pos_customer_validated/static/src/xml/partner_details_edit.xml',
        ],
    },


    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
