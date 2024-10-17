from odoo import models, fields, api
from odoo.exceptions import AccessError

class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'
    
    @api.model
    def unlink(self):
        # Verificar si el usuario pertenece al grupo restringido
        if self.env.user.has_group('custom_security_rules.group_custom_security_role_user_2'):
            raise AccessError("No tienes permiso para eliminar este registro.")
        
        # Lógica personalizada antes de eliminar, si es necesario
        return super(StockPickingInherit, self).unlink()