from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line')
    def _compute_price_unit_readonly(self):
        group_id = self.env.ref('custom_security_rules.group_custom_security_role_user').id
        for record in self:
            record.price_unit_readonly = not self.env.user.has_group(group_id)

    price_unit_readonly = fields.Boolean(compute='_compute_price_unit_readonly', store=False)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_unit = fields.Float(
        readonly=lambda self: self.price_unit_readonly
    )
