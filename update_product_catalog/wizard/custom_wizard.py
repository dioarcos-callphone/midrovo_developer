from odoo import models, fields, api

class MyErrorWizard(models.TransientModel):
    _name = 'custom.error.wizard'
    _description = 'Wizard de Mensaje de Error'

    message = fields.Text(string="Mensaje de Error", readonly=True)

    def action_close(self):
        """ Método para cerrar el wizard """
        return {'type': 'ir.actions.act_window_close'}