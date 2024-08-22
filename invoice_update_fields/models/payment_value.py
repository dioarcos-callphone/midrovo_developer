from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def _l10n_ec_get_payment_data(self):
        payment_data = super(PaymentValue, self)._l10n_ec_get_payment_data()
        
        payment_data.clear()
        
        result = self.env['account.move.sri.lines'].search([], order='id desc', limit=1)
        
        sri_lines = result
        
        result.write(sri_lines)
        
        _logger.info(f'MOSTRANDO RESULTADO SRI LINES >>> { result }')
        
        for element in result:
            _logger.info(f'ACCOUNT MOVE ID >>> { element.move_id }')
        
        

        return payment_data
