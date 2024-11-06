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
            _logger.info(f"Journal changed to: {self.journal_id.name}")
            for line in self.line_ids:
                if self.journal_id.analytic_id:
                    _logger.info(f"Setting analytic distribution for line {line.id}")
                    line.analytic_distribution = { str(self.journal_id.analytic_id.id): 100 }
                else:
                    _logger.warning("No analytic account found for the selected journal.")

class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"
    
    @api.depends('move_id.journal_id')    
    def _compute_journal_id(self):
        if self.move_id:
            analytic_account = self.move_id.journal_id.analytic_id
            if analytic_account:
                _logger.info(f"Computing analytic distribution for line {self.id}")
                self.analytic_distribution = { str(analytic_account.id): 100 }  # Distribuir 100% a esa cuenta
            else:
                _logger.warning(f"No analytic account found for journal in move {self.move_id.id}")
