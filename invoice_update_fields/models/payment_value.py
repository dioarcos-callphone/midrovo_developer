from odoo import models, api
import logging
_logger = logging.getLogger(__name__)

sri_lines = []

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def update_account_move_sri_lines(self, invoice_name, sri_lines):
        sri_lines.clear()
        for line in sri_lines:
            sri_lines.append(line)
        
        super(PaymentValue, self).update_account_move_sri_lines(self, invoice_name, sri_lines)

    
    @api.model
    def _l10n_ec_get_payment_data(self):
        payment_contable = super(PaymentValue, self)._l10n_ec_get_payment_data()
        payment_data = [] 
            
        if sri_lines:
            for sri_line in sri_lines:
                l10n_ec_sri_payment = self.env['l10n_ec.sri.payment'].search([('id','=', sri_line.l10n_ec_sri_payment_id)])
                
                if l10n_ec_sri_payment:
                    payment_values = {
                        'payment_code': l10n_ec_sri_payment.code,
                        'payment_total': sri_line.payment_valor,
                        'payment_name': l10n_ec_sri_payment.name
                    }
            
                    payment_data.append(payment_values)
                    
        sri_lines.clear()
        
        return payment_data if payment_data else payment_contable
