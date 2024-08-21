from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    def _get_default_forma_pago_sri(self):
        return self.env['l10n_ec.sri.payment'].search([('code', '=', '16')])
    
    l10n_ec_sri_payment_id = fields.Many2one(
        comodel_name="l10n_ec.sri.payment",
        string="Payment Method (SRI)",
        # default=_get_default_forma_pago_sri,        
    )
    
    @api.model
    def _l10n_ec_get_payment_data(self):
        payment_data = []
        
        # pay_term_line_ids = self.line_ids.filtered(
        #     lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
        # )
        
        pay_term_line_ids = self.l10n_ec_sri_payment_ids.filtered(
            lambda line: line.payment_valor > 0
        )
        
        # move_id = pay_term_line_ids.move_id
        # name = pay_term_line_ids.name
        # ref = pay_term_line_ids.ref
        
        # _logger.info(f'PAYMENT TERM 1 >>> { move_id.id } || { name } || { ref }')
        
        _logger.info(f'PAYMENT TERM 1 >>> { pay_term_line_ids }')
                
        for line in pay_term_line_ids:
            payment_vals = {
                    'payment_code': 16,
                    'payment_total': line.payment_valor,
            }
        
            payment_data.append(payment_vals)
        
        _logger.info(f'MOSTRANDO EL PAYMENT DATA 1 >>> { payment_data }')

        return payment_data