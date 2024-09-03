from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

nota_actual = ''

class InvoiceUpdate(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def get_note(self, argumentos):
        _logger.info(f'MOSTRANDO ARGUMENTOS >>> { argumentos }')
        # pay_term_line_ids = self.line_ids.filtered(
        #     lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
        # )
        
        # move_id = pay_term_line_ids.move_id.id
        
        # _logger.info(f'OBTENIENDO MOVE ID >>> { move_id }')
        
        # invoice = self.search([('id', '=', move_id)])
        
        # _logger.info(f'OBTENIENDO INVOICE >>> { invoice }')
        
        # if invoice:
        #     invoice.write({ 'narration': nota })

        return argumentos
    
    # @api.model
    # def _l10n_ec_get_payment_data(self):
    #     pay_term_line_ids = self.line_ids.filtered(
    #         lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
    #     )
        
    #     move_id = pay_term_line_ids.move_id.id
        
    #     _logger.info(f'OBTENIENDO MOVE ID >>> { move_id }')
        
    #     invoice = self.search([('id', '=', move_id)])
        
    #     _logger.info(f'OBTENIENDO INVOICE >>> { invoice }')
        
    #     if invoice:
    #         invoice.write({ 'narration': nota_actual })
        
    #     return super(InvoiceUpdate, self)._l10n_ec_get_payment_data()