from odoo import models, api
import logging
_logger = logging.getLogger(__name__)

sri_lines = []

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def update_account_move_sri_lines(self, invoice_name, sri_lines):
        try:
            # Buscar la factura por referencia
            invoice = self.env['account.move'].search([('ref', '=', invoice_name)], limit=1)
            
            if invoice:
                # Agregar las líneas SRI
                invoice.write({'l10n_ec_sri_payment_ids': [(0, 0, line) for line in sri_lines]})

        except Exception as e:
            # Capturar y registrar errores
            _logger.error("Ocurrió un error en update_account_move_sri_lines: %s", str(e))
            return False


    
    @api.model
    def _l10n_ec_get_payment_data(self):
        payment_contable = super(PaymentValue, self)._l10n_ec_get_payment_data()
        payment_data = []
        
        if self:
            sri_payments = self.l10n_ec_sri_payment_ids
            if sri_payments:
                for sri_payment in sri_payments:
                    payment_values = {
                        'payment_code': sri_payment.l10n_ec_sri_payment_id.code,
                        'payment_total': sri_payment.payment_valor,
                        'payment_name': sri_payment.l10n_ec_sri_payment_id.name
                    }
            
                    payment_data.append(payment_values)
                    
        
          
        # if sri_lines:
        #     for sri_line in sri_lines:
        #         l10n_ec_sri_payment = self.env['l10n_ec.sri.payment'].search([('id','=', sri_line.l10n_ec_sri_payment_id)])
                
        #         if l10n_ec_sri_payment:
        #             payment_values = {
        #                 'payment_code': l10n_ec_sri_payment.code,
        #                 'payment_total': sri_line.payment_valor,
        #                 'payment_name': l10n_ec_sri_payment.name
        #             }
            
        #             payment_data.append(payment_values)
        
        return payment_data if payment_data else payment_contable
