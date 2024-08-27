
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
    'depends': ['point_of_sale','res_partner'],
    'data': [
        'views/partner_details_edit.xml'
    ],

    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
