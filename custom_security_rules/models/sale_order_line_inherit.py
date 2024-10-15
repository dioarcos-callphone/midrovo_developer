from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('price_unit')
    def _check_price_unit(self):
        # Verifica si el usuario pertenece al grupo restringido
        if self.env.user.has_group('custom_security_rules.group_custom_security_role_user'):
            raise UserError("No tiene permisos para modificar los precios.")