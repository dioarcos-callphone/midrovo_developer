from odoo import api, fields, models

class PosPaymentMethodInherit(models.Model):
    _inherit = 'pos.payment.method'

    apply_card = fields.Boolean(
        string='Aplica Tarjetas de Crédito ?',
        default=False
    )
