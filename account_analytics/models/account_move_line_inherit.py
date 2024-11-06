from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'
    
    # analytic_distribution = fields.Json(
    #     default_get = lambda self: {
    #         str(self.env['account.analytic.account'].search([('name', '=', self.journal_id.analytic_id)], limit=1).id): 100
    #     },
    #     inverse="_inverse_analytic_distribution",
    # )
    
    @api.model
    def default_get(self, fields_list):
        res = super(AccountMoveLineInherit, self).default_get(fields_list)
        # Definir la cuenta analítica por defecto (ID de la cuenta analítica)
        # default_analytic_account_id = self.env['account.analytic.account'].search([('name', '=', 'Proyecto XYZ')], limit=1)
        
        if self.journal_id:
            analytic_account = self.journal_id.analytic_id
            _logger.info(f'MOSTRAR CUENTA ANALITICA >>> { analytic_account }')
            analytic_account_id = self.env['account.analytic.account'].search([('name', '=', analytic_account.name)], limit=1)
            
        # Establecer la distribución analítica por defecto si existe la cuenta
        # if default_analytic_account_id:
            self.analytic_distribution = {str(analytic_account_id.id): 100}  # Distribuir 100% a esa cuenta
            # _logger.info(f"BUSQUEDA >>> { res['analytic_distribution'] }")
        return res