from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('price_unit')
    def _check_price_unit(self):
        for record in self:
            # Compara el valor original con el actual
            if record.price_unit != record._origin.price_unit:
                # Verifica si el usuario pertenece al grupo restringido
                if self.env.user.has_group('custom_security_rules.group_custom_security_role_user'):
                    raise UserError("No tiene permisos para modificar los precios.")