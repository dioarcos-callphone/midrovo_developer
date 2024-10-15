from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    price_unit_compute = fields.Float(
        compute='_compute_price_unit_compute',
        store=False
    )

    def _compute_price_unit_compute(self):
        for line in self:
            line.price_unit = line.price_unit

    
    # @api.constrains('price_unit')
    # def _check_price_unit(self):
    #     # Verifica si el usuario pertenece al grupo restringido
    #     if self.env.user.has_group('custom_security_rules.group_custom_security_role_user'):
    #         raise UserError("No tiene permisos para modificar los precios.")