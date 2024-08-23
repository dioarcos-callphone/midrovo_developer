from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import time

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    def _get_default_forma_pago(self):
        pass
    
    @api.model
    def _l10n_ec_get_payment_data(self):        
        pay_term_line_ids = self.line_ids.filtered(
            lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
        )
        
        move_id = pay_term_line_ids.move_id.id
        
        # time.sleep(5) 
        result = self.env['account.move.sri.lines'].search([('move_id','=', move_id)], limit=1)
        
        _logger.info(f'OBTENIENDO SRI LINES >>> { result }')
        _logger.info(f'OBTENIENDO MOVE LINE >>> { pay_term_line_ids }') 

        return super(PaymentValue, self)._l10n_ec_get_payment_data()

# class PosOrder(models.Model):
#     _inherit = 'pos.order'

#     sale_barcode = fields.Char()

#     @api.model
#     def get_invoice_field(self, id):
#         payment_data = []
#         pos_id = self.search([('pos_reference', '=', id)])
#         invoice_id = self.env['account.move'].search(
#             [('ref', '=', pos_id.name)])
        
#         result = self.env['account.move.sri.lines'].search([('move_id','=',invoice_id.id)])
#         _logger.info(f'OBTENIENDO RESULT >>> { result }')
        
#         for line in result:
#             payment_vals = {
#                 'payment_code': line.l10n_ec_sri_payment_id.code,
#                 'payment_total': line.payment_valor,
#                 'payment_name':line.l10n_ec_sri_payment_id.name,
#             }
            
#             self.env['account.move.sri.lines'].write({
#                 'l10n_ec_sri_payment_id': line.l10n_ec_sri_payment_id.code,
#                 'payment_valor': line.payment_valor,
#             })
            
#             payment_data.append(payment_vals)

#         return {
#             'invoice_id': invoice_id.id,
#             'invoice_name': invoice_id.name,
#             'invoice_number': invoice_id.l10n_latam_document_number,
#             'xml_key': invoice_id.l10n_ec_authorization_number,
#             'payment_data': payment_data
#         }
        
    # def _l10n_ec_get_payment_data(self, pos_reference):
    #     payment =  self.get_invoice_field(pos_reference.pos_reference)
    #     payment_data = []
    #     pos_id = self.search([('pos_reference', '=', pos_reference.pos_reference)])
    #     invoice_id = self.env['account.move'].search(
    #         [('ref', '=', pos_id.name)])
        
    #     payment = payment['payment_data']
    #     _logger.info(f'OBTENIENDO DEL INVOICE >>> { payment }')        
        
    #     result = self.env['account.move.sri.lines'].search([('move_id','=',invoice_id.id)])
        
    #     _logger.info(f'OBTENIENDO RESULT >>> { result }')
        
    #     for line in result:
    #         payment_vals = {
    #             'payment_code': line.l10n_ec_sri_payment_id.code,
    #             'payment_total': line.payment_valor,
    #             'payment_name':line.l10n_ec_sri_payment_id.name,
    #         }
            
    #         payment_data.append(payment_vals)
            
    #     return payment_data
            
        
        
        
        
