from odoo import models, api
import logging
_logger = logging.getLogger(__name__)

sri_payment_lines = []

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def update_account_move_sri_lines(self, invoice_name, sri_lines):
        try:
            sri_payment_lines.clear()
            # Buscar la factura por referencia
            invoice = self.env['account.move'].search([('ref', '=', invoice_name)], limit=1)
            
            if sri_lines:
                for sri_line in sri_lines:
                    sri_payment_lines.append(sri_line)                
            
            if invoice:
                for line in sri_lines:
                    sri_payment = self.env['l10n_ec.sri.payment'].search([('id', '=', line['l10n_ec_sri_payment_id'])])
                    self.env['account.move.sri.lines'].create({
                        'l10n_ec_sri_payment_id': sri_payment.id,
                        'move_id': invoice.id,
                        'payment_valor': line['payment_valor']
                    })

        except Exception as e:
            # Capturar y registrar errores
            _logger.error("Ocurrió un error en update_account_move_sri_lines: %s", str(e))
            return False
    
    @api.model
    def _l10n_ec_get_payment_data(self):
        contable_payments = super(PaymentValue, self)._l10n_ec_get_payment_data()
        payment_data = []
        
        if sri_payment_lines:
            for sri_payment_line in sri_payment_lines:
                sri_payment = self.env['l10n_ec.sri.payment'].search([
                    ('id','=', sri_payment_line.get('l10n_ec_sri_payment_id'))
                ])
                
                if sri_payment:
                    payment_values = {
                        'payment_code': sri_payment.code,
                        'payment_total': sri_payment_line.get('payment_valor'),
                        'payment_name': sri_payment.name
                    }
            
                    payment_data.append(payment_values)
        
        return payment_data if payment_data else contable_payments
