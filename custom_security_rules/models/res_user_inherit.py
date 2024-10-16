from odoo import models, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def toggle_write_permission(self, enable):
        group = self.env.ref('custom_security_rules.group_custom_security_role_user')
        if enable:
            group.write({'write_access': True})  # Habilitar permiso de escritura
        else:
            group.write({'write_access': False})  # Deshabilitar permiso de escritura
        return True
