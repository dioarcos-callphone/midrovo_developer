from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'
    
    price_unit = fields.Float(
        readonly=lambda self: self._check_readonly_price_unit()
    )

    @api.model
    def _check_readonly_price_unit(self):
        # Comprueba si el usuario pertenece al grupo específico
        group_id = self.env.ref('custom_security_rules.group_custom_security_role_user').id
        return not self.env.user.has_group(group_id)

    # @api.depends('price_unit')
    # def _check_price_unit(self):
    #     # Verifica si el usuario pertenece al grupo restringido
    #     if self.env.user.has_group('custom_security_rules.group_custom_security_role_user'):
    #         raise UserError("No tiene permisos para modificar los precios.")