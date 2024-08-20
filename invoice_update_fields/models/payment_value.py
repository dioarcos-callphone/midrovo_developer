from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def _l10n_ec_get_payment_data(self):
        payment_data = super(PaymentValue, self)._l10n_ec_get_payment_data()
        
        # payment_total = payment_data['payment_total']
        _logger.info(f'MOSTRANDO EL PAYMENTO TOTAL >>> { payment_data }')
        
        # for payment in payment_data:
        #     payment_total = payment['payment_total']
        #     _logger.info(f'MOSTRANDO EL PAYMENTO TOTAL >>> { payment_total }')

        return payment_data