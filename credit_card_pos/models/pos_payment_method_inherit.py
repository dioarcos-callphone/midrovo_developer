from odoo import api, fields, models

class PosPaymentMethodInherit(models.Model):
    _inherit = 'pos.payment.method'

    apply_card = fields.Boolean(
        string='Tarjetas de Crédito ?',
        default=False
    )
    
    @api.model
    def is_card(self, name_method):
        pos_payment_method = self.search([('name', '=', name_method)], limit=1)
        
        if pos_payment_method:
            if pos_payment_method.apply_card:
                return True
        
        return False       
