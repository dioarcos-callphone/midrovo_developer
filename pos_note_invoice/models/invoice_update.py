from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class InvoiceUpdate(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def get_note(self, nota):
        pay_term_line_ids = self.line_ids.filtered(
            lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
        )
        
        move_id = pay_term_line_ids.move_id.id
        
        _logger.info(f'OBTENIENDO MOVE ID >>> { move_id }')
        
        invoice = self.search([('id', '=', move_id)])
        
        _logger.info(f'OBTENIENDO INVOICE >>> { invoice }')
        
        if invoice:
            invoice.write({ 'narration': nota })

        return nota