from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

data = []
query = 'SELECT code, name FROM l10n_ec_sri_payment WHERE id = %s'

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    def _get_default_forma_pago(self):
        pass
    
    def _get_default_forma_pago_sri(self):
        pass
    
    # l10n_ec_sri_payment_ids = fields.Many2one('account.move.sri.lines', 'move_id',)
    
    @api.model
    def update_account_move_sri_lines(self, invoice_name, sri_lines):        
        try:
            data.clear()
            for line in sri_lines:
                data.append(line)
            
            # Agrega las sri_lines al acount_move
            lines_value = []
            invoice_id = self.env['account.move'].search(
            [('ref', '=', invoice_name)])
            _logger.info(f'MOSTRANDO EL INVOICE >>> { invoice_id }')
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
    def _l10n_ec_get_payment_data_inherit(self):
        cr = self.env.cr
        payment_data = []
        
        for line in data:
            payment_id = line['l10n_ec_sri_payment_id']
            _logger.info(f'ID DEL PAYMENT SRI >>> { payment_id }')
            cr.execute(query,(payment_id,))
            result = cr.fetchone()
            
            _logger.info(f'OBTENIENDO EL RESULT >>> { result }')
            payment_values = {
                'payment_code': result[0],
                'payment_total': line['payment_valor'],
                'payment_name': result[1]
            }
            
            payment_data.append(payment_values)
        
        _logger.info(f'SE OBTIENE EL PAYMENT DATA >>> { payment_data }')  
        
        data.clear()
        
        payment_contable = super(PaymentValue, self)._l10_ec_gt_payment_data()
        
        _logger.info(f'SE OBTIENE EL PAYMENT CONTABLE >>> { payment_contable }')
        
        # return payment_data
        return payment_data