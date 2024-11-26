from odoo import models, api
import logging
_logger = logging.getLogger(__name__)

data = []

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def update_account_move_sri_lines(self, invoice_name, sri_lines):        
        try:
            _logger.info(f'SRI LINES { sri_lines }')
            data.clear()
            for line in sri_lines:
                data.append(line)
            
            # Agrega las sri_lines al acount_move
            lines_value = []
            invoice_id = self.env['account.move'].search(
            [('ref', '=', invoice_name)])
            invoice = self.env['account.move'].browse(invoice_id.id)
            if invoice :
                for sri_line in sri_lines:
                    invoice.write({'l10n_ec_sri_payment_ids': [(0, 0, sri_line)]})
                    lines_value.append( (0, 0, sri_line))
                invoice.env.cr.commit()
        except Exception as e:
            # Captura la excepción y registra el error
            _logger.error("Ocurrió un error: %s", str(e))
    
    @api.model
    def _l10n_ec_get_payment_data(self):
        payment_contable = super(PaymentValue, self)._l10n_ec_get_payment_data()
        payment_data = []
        
        _logger.info(f'MOSTRANDO SELF >>> { self.l10n_ec_sri_payment_ids }')
        
        for line in data:
            payment_id = line['l10n_ec_sri_payment_id']
            
            sri_payment = self.env['l10n_ec.sri.payment'].search([
                ("id", "=", payment_id)
            ])

            payment_values = {
                'payment_code': sri_payment.code,
                'payment_total': line['payment_valor'],
                'payment_name': sri_payment.name
            }
            
            payment_data.append(payment_values)  
        
        data.clear()        
        return payment_data if payment_data else payment_contable
