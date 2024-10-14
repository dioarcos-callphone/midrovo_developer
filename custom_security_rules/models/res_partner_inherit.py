from odoo import models, fields, api
from odoo.exceptions import UserError

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'
    
    # def action_create(self, vals):
    #     return super(ResPartnerInherit, self).create(vals)
    
    # def write(self, vals):
    #     # Verificar si el usuario pertenece al grupo 'group_no_edit_delete'
    #     if self.env.user.has_group('custom_security_rules.group_no_edit_delete'):
    #         raise UserError("No tienes permiso para actualizar este registro.")
        
    #     # Si no pertenece al grupo, permite la escritura
    #     return super(ResPartnerInherit, self).write(vals)