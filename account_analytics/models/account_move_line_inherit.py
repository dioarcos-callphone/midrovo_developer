from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'
    
    @api.model
    def default_get(self, fields_list):
        res = super(AccountMoveLineInherit, self).default_get(fields_list)
        # Definir la cuenta analítica por defecto (ID de la cuenta analítica)
        default_analytic_account_id = self.env['account.analytic.account'].search([('name', '=', 'Proyecto XYZ')], limit=1)
        
        # Establecer la distribución analítica por defecto si existe la cuenta
        if default_analytic_account_id:
            res['analytic_distribution'] = {str(default_analytic_account_id.id): 100}  # Distribuir 100% a esa cuenta
        return res