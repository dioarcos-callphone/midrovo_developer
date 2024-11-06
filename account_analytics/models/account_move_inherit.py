from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    
    @api.onchange('journal_id')
    def onchange_journal(self):
        if self:
            for line in self.line_ids:
                if self.journal_id.analytic_id:
                    if line.account_id.account_type == 'income' or line.account_id.account_type == 'expense':
                        line.analytic_distribution = { str(self.journal_id.analytic_id.id): 100 }
    
class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"
    
    analytic_distribution = fields.Json(
        compute='_compute_analytic_distribution',  # Función que calculará el valor
        inverse='_inverse_analytic_distribution',  # Función para manejar el cambio de valor
        store=True,  # Indicamos que el campo se guarda en la base de datos
    )

    # Función que calcula el valor del campo computado
    def _compute_analytic_distribution(self):
        for record in self:
            _logger.info(f'MOSTRANDO MOVE ID >>> { self.move_id.journal_id }')
            # Aquí puedes poner tu lógica para calcular el valor
            analytic = self.env['account.analytic.account'].search([('id', '=', 1)], limit=1)
            record.analytic_distribution = { str(analytic.id): 100 }

    
    # def default_get(self, fields_list):
    #     defaults = super().default_get(fields_list)
        
    #     if self.move_id.journal_id:
    #         journal_id = self.move_id.journal_id
    #         if journal_id.analytic_id:
    #             if self.move_id.onchange_journal():
    #                 analytic_id = journal_id.analytic_id
    #                 self.analytic_distribution = { str(analytic_id.id): 100 }

    #     return defaults
    