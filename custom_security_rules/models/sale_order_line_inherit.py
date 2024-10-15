from odoo import models, fields, api

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     # Restringir el cambio de 'price_unit' si el usuario no pertenece al grupo
    #     if self.env.user.has_group('custom_security_rules.group_custom_security_role_user'):
    #         self.price_unit = self.price_unit  # Mantener editable para el grupo
    #     else:
    #         self.price_unit = self.price_unit  # Dejar inmutable para otros usuarios

    # @api.model
    # def create(self, vals):
    #     # Restringir el cambio de 'price_unit' en la creación
    #     if not self.env.user.has_group('custom_security_rules.group_custom_security_role_user'):
    #         if 'price_unit' in vals:
    #             del vals['price_unit']  # Quitar el campo para usuarios sin acceso
    #     return super(SaleOrderLineInherit, self).create(vals)

    # def write(self, vals):
    #     # Restringir el cambio de 'price_unit' en la edición
    #     if not self.env.user.has_group('custom_security_rules.group_custom_security_role_user'):
    #         if 'price_unit' in vals:
    #             del vals['price_unit']  # Quitar el campo para usuarios sin acceso
    #     return super(SaleOrderLineInherit, self).write(vals)
