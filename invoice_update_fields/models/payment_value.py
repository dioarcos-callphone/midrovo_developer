from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def _l10n_ec_get_payment_data(self):
        payment_data = super(PaymentValue, self)._l10n_ec_get_payment_data()

        for payment in payment_data:
            payment_name = payment['payment_name']
            payment_total = payment['payment_total']
            _logger.info(f'PAYMENT NAME >>> { payment_name }')
            _logger.info(f'PAYMENT TOTAL >>> { payment_total }')

        return payment_data