from odoo import models, fields

class MyErrorWizard(models.TransientModel):
    _name = 'wizard.product.template'
    _description = 'Wizard de Mensaje de Error'

    message = fields.Text(string="Mensaje de Error", readonly=True)

    def action_close(self):
        """Método para cerrar el wizard"""
        return {'type': 'ir.actions.act_window_close'}
