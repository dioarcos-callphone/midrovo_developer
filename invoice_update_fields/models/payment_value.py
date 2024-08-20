from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class PaymentValue(models.Model):
    _inherit = 'account.move'
     
    @api.model
    def _l10n_ec_get_payment_data(self):
        payment_data_2 = []
        payment_data = super(PaymentValue, self)._l10n_ec_get_payment_data()
        
        payment_data.clear()
        
        pay_term_line_ids = self.line_ids.filtered(
            lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
        )
        
        pay_term_line_ids_2 = self.l10n_ec_sri_payment_ids.filtered(
            lambda line: line.payment_valor > 0
        )
                
        for line in pay_term_line_ids:
            payment_vals = {
                    'payment_code': self.l10n_ec_sri_payment_id.code,
                    'payment_total': abs(line.balance),
            }
        
            payment_data.append(payment_vals)
            
        for line in pay_term_line_ids_2:
            payment_vals = {
                'payment_code': line.l10n_ec_sri_payment_id.code,
                'payment_total': line.payment_valor,
                'payment_name':line.l10n_ec_sri_payment_id.name,
            }
            
            payment_data_2.append(payment_vals)
        
        _logger.info(f'MOSTRANDO EL PAYMENT DATA 1 >>> { payment_data }')
        
        _logger.info(f'MOSTRANDO EL PAYMENT DATA 2 >>> { payment_data_2 }')

        return payment_data