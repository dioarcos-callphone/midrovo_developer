from odoo import models, fields, api

class RegenerateImages(models.TransientModel):
    _name = 'regenerate.images'
    _description = 'Regenerar Caché de Imágenes'

    models_to_update = fields.Selection(
        selection=[('product.template', 'Productos'), ('res.partner', 'Contactos')],
        string='Modelo a actualizar',
        required=True
    )

    @api.model
    def regenerate_images(self):
        model = self.models_to_update
        records = self.env[model].search([])
        for record in records:
            record.write({'image_1920': record.image_1920})
        return {'type': 'ir.actions.client', 'tag': 'reload'}
