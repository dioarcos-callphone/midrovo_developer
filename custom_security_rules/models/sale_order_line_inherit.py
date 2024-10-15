from odoo import models, fields, api

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    can_edit_price = fields.Boolean(compute='_compute_can_edit_price', store=True)

    @api.depends('order_id.user_id')
    def _compute_can_edit_price(self):
        for line in self:
            # Por ejemplo, puedes basarlo en el usuario que crea la orden o en otras reglas de negocio
            line.can_edit_price = line.order_id.user_has_groups('custom_security_rules.group_custom_security_role_user')