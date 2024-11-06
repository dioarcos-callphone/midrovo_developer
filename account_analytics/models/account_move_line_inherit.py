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
        if self.move_id:
            analytic_account = self.move_id.journal_id.analytic_id
            self.analytic_distribution = {str(analytic_account.id): 100}  # Distribuir 100% a esa cuenta
        
        return super(AccountMoveLineInherit, self).default_get(fields_list)
    
    @api.onchange('move_id')
    def onchange_move_id(self):
        analytic_account = self.journal_id.analytic_id
        self.move_analytic_distributionid = {str(analytic_account.id): 100}
    