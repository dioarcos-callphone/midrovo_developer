from odoo import models, api, _

import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        # Obtener el grupo
        _logger.info('ENTRA AQUI')
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
            _logger.info('ACTIVAMOS')
            _logger.info('ENTRA AQUI CUANDO EL GRUPO ES group_custom_security_role_user')
            # Habilitar el permiso de escritura temporalmente
            write_permission.perm_write = True

        # Crear el registro de partner
        partner = super(ResPartner, self).create(vals)

        if write_permission:
            _logger.info('DESACTIVAMOS')
            # Deshabilitar el permiso de escritura nuevamente
            write_permission.perm_write = False

        return partner
