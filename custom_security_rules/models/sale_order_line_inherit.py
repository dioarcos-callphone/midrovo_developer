from odoo import models, fields, api

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order'

    can_edit_price = fields.Boolean(compute='_compute_can_edit_price')

    @api.depends('user_id')
    def _compute_can_edit_price(self):
        for order in self:
            user = self.env.user
            group = self.env.ref('custom_security_rules.group_custom_security_role_user')
            order.can_edit_price = group in user.groups_id