from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def _get_default_forma_pago_sri(self):
        pass
    
    l10n_ec_sri_payment_id = fields.Many2one(
        comodel_name="l10n_ec.sri.payment",
        string="Payment Method (SRI)",
    )
    
    # line_ids = fields.One2many(
    #     'account.move.sri.line',
    #     'move_id',
    # )
     
    # @api.model
    # def _l10n_ec_get_payment_data(self):
    #     payment_data = []
    #     # payment_data = super(PaymentValue, self)._l10n_ec_get_payment_data()
        
    #     # payment_data.clear()
        
    #     # pay_term_line_ids = self.line_ids.filtered(
    #     #     lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
    #     # )
        
    #     pay_term_line_ids = self.l10n_ec_sri_payment_ids
        
        
    #     # pay_term_line_ids_2 = self.l10n_ec_sri_payment_ids
        
    #     _logger.info(f'PAYMENT TERM 1 >>> { pay_term_line_ids }')
    #     # _logger.info(f'PAYMENT TERM 2 >>> { pay_term_line_ids_2 }')
                
    #     for line in pay_term_line_ids:
    #         payment_vals = {
    #                 'payment_code': 16,
    #                 'payment_total': 15,
    #                 'payment_name': 'Debito',
    #         }
        
    #         payment_data.append(payment_vals)
        
    #     _logger.info(f'MOSTRANDO EL PAYMENT DATA 1 >>> { payment_data }')

    #     return payment_data
    
    @api.model
    def _l10n_ec_get_payment_data(self):
        """ Get payment data for the XML.  """
        payment_data = []
        pay_term_line_ids = self.line_ids.filtered(
            lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
        )
        for line in pay_term_line_ids:
            payment_vals = {
                'payment_code': 16,
                'payment_total': 20,
                'payment_name': 'Debito',
            }
            if self.invoice_payment_term_id and line.date_maturity:
                payment_vals.update({
                    'payment_term': max(((line.date_maturity - self.invoice_date).days), 0),
                    'time_unit': "dias",
                })
            payment_data.append(payment_vals)
        if self.compensa>0:
            payment_vals = {
                    'payment_code': '15',
                    'payment_total': self.compensa,
                    'payment_name': 'Compensación de Deudas',
                }
            payment_vals.update({
                        'payment_term': 1,
                        'time_unit': "dias",
                    })
            payment_data.append(payment_vals)
        return payment_data