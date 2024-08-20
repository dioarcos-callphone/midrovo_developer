from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    # @api.model
    # def get_invoice_field(self, id):
    #     pos_id = self.search([('pos_reference', '=', id)])
    #     invoice_id = self.env['account.move'].search(
    #         [('ref', '=', pos_id.name)])
        
    #     result = invoice_id._l10n_ec_get_payment_data()    
        
    #     _logger.info(f'MOSTRANDO PAYMENT DATA >>> { result }')
        
    #     return super(PaymentValue, self).get_invoice_field(id)
    
    @api.model
    def _l10n_ec_get_payment_data(self):
        payment_data = super(PaymentValue, self)._l10n_ec_get_payment_data()
        
        payment_data.clear()
        
        pay_term_line_ids = self.line_ids.filtered(
            lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
        )
        
        _logger.info(f'MOSTRANDO EL PAYMENT TERM LINE >>> { pay_term_line_ids }')
        
        for line in pay_term_line_ids:
            payment_vals = {
                    'payment_code': line.l10n_ec_sri_payment_id.code,
                    'payment_total': line.payment_valor,
                    'payment_name': line.l10n_ec_sri_payment_id.name,
            }
        
            payment_data.append(payment_vals)
        
        # for payment in payment_data:
        #     payment_total = payment['payment_total']
        #     _logger.info(f'MOSTRANDO EL PAYMENTO TOTAL >>> { payment_total }')
        
        _logger.info(f'MOSTRANDO EL PAYMENT TOTAL >>> { payment_data }')

        return payment_data