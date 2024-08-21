from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    def _get_default_forma_pago_sri(self):
        pass
        # return self.env['l10n_ec.sri.payment'].search([('code', '=', '16')])
    
    l10n_ec_sri_payment_id = fields.Many2one(
        comodel_name="l10n_ec.sri.payment",
        string="Payment Method (SRI)",
        # default=_get_default_forma_pago_sri,
    )
    
    # l10n_ec_sri_payment_id = fields.Many2one(
    #     comodel_name="l10n_ec.sri.payment",
    #     string="Payment Method (SRI)",
    #     required=True, 
    #     ondelete='cascade', 
    #     index=True
    # )
    
    # line_ids = fields.One2many(
    #     'account.move.sri.line',
    #     'move_id',
    # )
     
    @api.model
    def _l10n_ec_get_payment_data(self):
        payment_data = []
        
        pay_term_line_ids = self.line_ids.filtered(
            lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
        )
        
        _logger.info(f'PAYMENT TERM 1 >>> { pay_term_line_ids }')
                
        for line in pay_term_line_ids:
            payment_vals = {
                    'payment_code': 16,
                    'payment_total': abs(line.balance),
            }
        
            payment_data.append(payment_vals)
        
        _logger.info(f'MOSTRANDO EL PAYMENT DATA 1 >>> { payment_data }')

        return payment_data