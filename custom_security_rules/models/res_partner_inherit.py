from odoo import models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        # Obtener el grupo
        group_user = self.env.ref('custom_security_rules.group_custom_security_role_user')
        
        # Obtener el permiso actual del grupo para res.partner
        write_permission = self.env['ir.model.access'].search([
            ('group_id', '=', group_user.id),
            ('model_id.model', '=', 'res.partner')
        ], limit=1)
        
        if write_permission:
            # Habilitar el permiso de escritura temporalmente
            write_permission.perm_write = True

        # Crear el registro
        partner = super(ResPartner, self).create(vals)

        if write_permission:
            # Deshabilitar el permiso de escritura nuevamente
            write_permission.perm_write = False

        return partner
