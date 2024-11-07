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
        for record in self:            
            # Buscamos la cuenta analítica relacionada con el journal_id
            analytic_account = record.move_id.journal_id.analytic_id

            # Si se encuentra una cuenta analítica, asignamos el valor correspondiente
            if analytic_account:
                
                if record.account_id.account_type == 'income' or record.account_id.account_type == 'expense':
                    record.analytic_distribution = {str(analytic_account.id): 100}
            else:
                # Si no se encuentra ninguna cuenta, se asigna un valor predeterminado o vacío
                record.analytic_distribution = {}
