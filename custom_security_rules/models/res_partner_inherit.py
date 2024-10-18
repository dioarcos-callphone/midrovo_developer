from odoo import models, api, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # @api.model
    # def create(self, vals):
    #     # Obtener el grupo
    #     group_user = self.env.ref('custom_security_rules.group_custom_security_role_user')
    #     _logger.info('ENTRA EN EL CREATE')
    #     # Verificar si el grupo se obtiene correctamente
    #     if not group_user:
    #         raise ValueError(_("El grupo no se encontró: 'group_custom_security_role_user'"))

    #     # Buscar el permiso de acceso en ir.model.access
    #     write_permission = self.env['ir.model.access'].sudo().search([
    #         ('group_id', '=', group_user.id),
    #         ('model_id.model', '=', 'res.partner')
    #     ], limit=1)

    #     if write_permission:
    #         _logger.info('ENTRA AQUI')
    #         # Habilitar el permiso de escritura temporalmente
    #         write_permission.perm_write = True

    #     # Crear el registro de partner
    #     partner = super(ResPartner, self).create(vals)

    #     if write_permission:
    #         # Deshabilitar el permiso de escritura nuevamente
    #         write_permission.perm_write = False

    #     return partner

    @api.model
    def create(self, vals):
        # Permitir creación sin restricciones
        return super(ResPartner, self).create(vals)

    def write(self, vals):
        # Comprobar si el usuario pertenece al grupo que solo debe crear contactos
        if self.env.user.has_group('custom_security_rules.group_custom_security_role_user'):
            # Realizar un search para verificar si el ID existe en la base de datos
            existing_partners = self.search([('id', 'in', self.ids)])
            if existing_partners:
                _logger.info(f'ESTADO >>> { self.state }')
                # Si hay registros existentes, prohibir la actualización
                raise UserError(_('No tiene permisos para actualizar contactos.'))
        
        # Si no pertenece al grupo o si no está actualizando un registro existente, proceder con la escritura
        return super(ResPartner, self).write(vals)