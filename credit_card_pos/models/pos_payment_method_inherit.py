from odoo import api, fields, models

class PosPaymentMethodInherit(models.Model):
    _inherit = 'pos.payment.method'

    apply_card = fields.Boolean(
        string='Aplica Tarjeta de Crédito ?',
        default='false'
    )
