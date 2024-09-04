from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

nota_actual = ''

class InvoiceUpdate(models.Model):
    _inherit = 'pos.order'
    
    @api.model
    def get_note(self, orders, draft, nota):
        for order in orders:
            # name = order['name']
            
            _logger.info(f'OBTENIENDO SHOP NAME >>> { order }')
            
        _logger.info(f'OBTENIENDO ORDERS >>> { orders }')
        _logger.info(f'OBTENIENDO NOTA >>> { nota }')

        return nota
    
    # @api.model
    # def get_note(self, argumentos):
    #     pay_term_line_ids = self.line_ids.filtered(
    #         lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
    #     )
        
    #     _logger.info(f'PAY TERM >>> { pay_term_line_ids }')
        
    #     receipt_number = argumentos['receipt_number']
    #     nota = argumentos['note']
        
    #     _logger.info(f'NUMBER RECEIPT >>> { receipt_number } || NOTA >>> { nota }')
        
    #     pos_id = self.env['pos.order'].search([('pos_reference', '=', receipt_number)], limit=1)
        
    #     invoice = self.search([('ref', '=', pos_id.name)], limit=1)
        
    #     _logger.info(f'MOSTRANDO INVOICE >>>> { invoice }')
        
    #     _logger.info(f'MOSTRANDO NARRATION >>>> { invoice.narration }')
        
    #     # invoice.write({ 'narration': nota })        
        
    #     _logger.info(f'MOSTRANDO ARGUMENTOS >>> { argumentos }')
    #     # pay_term_line_ids = self.line_ids.filtered(
    #     #     lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
    #     # )
        
    #     # move_id = pay_term_line_ids.move_id.id
        
    #     # _logger.info(f'OBTENIENDO MOVE ID >>> { move_id }')
        
    #     # invoice = self.search([('id', '=', move_id)])
        
    #     # _logger.info(f'OBTENIENDO INVOICE >>> { invoice }')
        
    #     # if invoice:
    #     #     invoice.write({ 'narration': nota })

    #     return argumentos
    
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