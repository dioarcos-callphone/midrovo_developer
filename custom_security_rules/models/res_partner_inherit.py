from odoo import models, api, _
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        # Obtener el grupo
        group_user = self.env.ref('custom_security_rules.group_custom_security_role_user')

        # Verificar si el grupo se obtiene correctamente
        if not group_user:
            raise ValueError(_("El grupo no se encontró: 'group_custom_security_role_user'"))

        # Buscar el permiso de acceso en ir.model.access
        write_permission = self.env['ir.model.access'].sudo().search([
            ('group_id', '=', group_user.id),
            ('model_id.model', '=', 'res.partner')
        ], limit=1)

        if write_permission:
            # Habilitar el permiso de escritura temporalmente
            write_permission.perm_write = True

        # Crear el registro de partner
        partner = super(ResPartner, self).create(vals)

        if write_permission:
            # Deshabilitar el permiso de escritura nuevamente
            write_permission.perm_write = False

        return partner

    # def write(self, vals):
    #     # Solo bloquear si el registro ya existe
    #     if self and self.ids:  # Si el registro ya tiene un ID, es una actualización
    #         if self.env.user.has_group('custom_security_rules.group_custom_security_role_user'):
    #             raise UserError("You are not allowed to update records.")
    #     return super(ResPartner, self).write(vals)