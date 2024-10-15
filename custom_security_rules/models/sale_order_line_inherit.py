from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'  # Cambiar a 'sale.order.line' si es necesario

    can_edit_price = fields.Boolean(compute='_compute_can_edit_price', store=True)

    @api.depends('user_id')  # Cambia esto a 'order_id.user_id' si estás en 'sale.order.line'
    def _compute_can_edit_price(self):
        for order in self:
            # Aquí utilizas el método para verificar si el usuario pertenece al grupo
            order.can_edit_price = order.user_has_groups('custom_security_rules.group_custom_security_role_user')
