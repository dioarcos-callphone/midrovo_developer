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
            move_lines = self.env['account.move.line'].browse(self.line_ids)
            _logger.info(f'MOVE LINES >>> { move_lines }')
            for line in move_lines:
                if self.journal_id.analytic_id:
                    if line.account_id.account_type == 'income' or line.account_id.account_type == 'expense':
                        line.analytic_distribution = { str(self.journal_id.analytic_id.id): 100 }
    

# class AccountMoveLineInherit(models.Model):
#     _inherit = "account.move.line"
    
    