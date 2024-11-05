from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class AccountMoveLineInherit(models.AbstractModel):
    _inherit = 'account.move.line'
    
    @api.model
    def default_get(self, fields_list):
        res = super(AccountMoveLineInherit, self).default_get(fields_list)
        
        if self.move_id.journal_id and self.account_id:
            analytic_account = self.move_id.journal_id.analytic_id
            
            # Establecer la distribución analítica por defecto si existe la cuenta
            if analytic_account:                
                _logger.info(f'CUENTA ANALITICA >>> { analytic_account }')

                res['analytic_distribution'] = {str(analytic_account.id): 100,}
                
        return res
