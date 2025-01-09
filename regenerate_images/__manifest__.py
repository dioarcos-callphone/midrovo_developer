{
    'name': 'Regenerate Images',
    'version': '16.0.1.0.0',
    'summary': 'Regeneración de caché de imágenes para productos y contactos.',
    'description': """
        Este módulo permite regenerar la caché de imágenes para productos y contactos en Odoo 16.
        Características:
        - Regeneración de imágenes desde un asistente.
        - Compatible con Odoo 16 Community.
    """,
    'category': 'Tools',
    'author': 'Mauricio Idrovo',
    'company': 'Callphone S.A.',
    'website': 'https://www.callphoneecuador.com',
    'images': [],  # Puedes añadir la ruta de una imagen si tienes un logotipo o una captura de pantalla.
    'depends': [
        'base',  # Dependencia mínima necesaria para los modelos base.
    ],
    'data': [
        'views/regenerate_image_view.xml',  # Asegúrate de que el nombre del archivo sea correcto.
    ],
    'installable': True,
    'application': False,  # Cambia a True si este módulo es una aplicación principal.
    'license': 'LGPL-3',
}
