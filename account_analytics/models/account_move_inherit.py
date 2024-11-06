from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    
    @api.onchange('journal_id')
    def onchange_journal(self):
        return {
            
            'value': { 'analytic_distribution': { str(self.journal_id.analytic_id.id): 100 } }
            
        }
        # if self:
        #     for line in self.line_ids:
        #         if self.journal_id.analytic_id:
        #             if line.account_id.account_type == 'income' or line.account_id.account_type == 'expense':
        #                 line.analytic_distribution = { str(self.journal_id.analytic_id.id): 100 }
    
class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"
    
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        
        if self.move_id.journal_id:
            journal_id = self.move_id.journal_id
            if journal_id.analytic_id:
                if self.move_id.onchange_journal():
                    analytic_id = journal_id.analytic_id
                    self.analytic_distribution = { str(analytic_id.id): 100 }

        return defaults
    