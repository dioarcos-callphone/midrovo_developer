from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    
    @api.onchange('journal_id')
    def onchange_journal(self):
        """
        Cuando el usuario cambia el diario (journal_id), este método se ejecuta.
        Se puede usar para actualizar las cuentas analíticas en las líneas del asiento.
        """
        if self:
            for line in self.line_ids:
                if self.journal_id.analytic_id:
                    if line.account_id.account_type == 'income' or line.account_id.account_type == 'expense':
                        line.analytic_distribution = { str(self.journal_id.analytic_id.id): 100 }
    
class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"
    
    @api.model
    def create(self, vals):
        if self:
            if self.account_id:
                _logger.info(f'ACCOUNT >>> { self.account_id }')
                if self.account_id.account_type == 'income' or self.account_id.account_type == 'expense':
                    analytic_id = self.move_id.journal_id.analytic_id
                    vals['analytic_distribution'] = { str(analytic_id.id): 100 }
    