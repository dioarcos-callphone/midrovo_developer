from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'
    
    @api.depends('price_unit')  # Añade otros campos relevantes si es necesario
    def _compute_price_unit_readonly(self):
        group_id = self.env.ref('custom_security_rules.group_custom_security_role_user').id
        for record in self:
            record.price_unit_readonly = not self.env.user.has_group(group_id)

    price_unit_readonly = fields.Boolean(compute='_compute_price_unit_readonly', store=False)