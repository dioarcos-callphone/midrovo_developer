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
    @api.depends('move_id.journal_id')
    def _compute_analytic_distribution(self):
        if self:
            journal_id = self.move_id.journal_id
            _logger.info(f'MOSTRANDO JOURNAL >>> { journal_id }')        
            
            analytic_account = journal_id.analytic_id
            _logger.info(f'ENTRA EN EL FOR >>> { analytic_account }')
            # Si se encuentra una cuenta analítica, asignamos el valor correspondiente
            if analytic_account:
                _logger.info('ENTRA AL PRIMER IF')
                if self.account_id.account_type == 'income' or self.account_id.account_type == 'expense':
                    _logger.info('ENTRA AL SEGUNDO IF')
                    self.analytic_distribution = {str(analytic_account.id): 100}
            else:
                # Si no se encuentra ninguna cuenta, se asigna un valor predeterminado o vacío
                self.analytic_distribution = {}
