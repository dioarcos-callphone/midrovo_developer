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
        default='_get_default_forma_pago_sri'
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
                    'payment_code': line.l10_ec_sri_payment_id.code,
                    'payment_total': line.payment_valor,
                    'payment_name': line.l10n_ec_sri_payment_id.name
            }
        
            payment_data.append(payment_vals)
        
        _logger.info(f'MOSTRANDO EL PAYMENT DATA 1 >>> { payment_data }')

        return payment_data
    
class InheritAccountMoveSriLines(models.Model):
    _inherit = 'account.move.sri.lines'

    def _get_default_forma_pago(self):
        return self.env['l10n_ec.sri.payment'].search([('code', '=', '16')])
    

    l10n_ec_sri_payment_id = fields.Many2one(
        comodel_name="l10n_ec.sri.payment",
        string="Payment Method (SRI)",
        required=True, 
        ondelete='cascade', 
        index=True
    )
    
    #parameter to One2many, 
    move_id = fields.Many2one(  "account.move", 
                                string="Account_key",
                                required=True,
                                readonly=True,
                                index=True,
                                auto_join=True,
                                ondelete="cascade",
                                check_company=True,
                            )
    
    payment_valor = fields.Float( string="Price value",
                                    compute='_compute_payment_valor', store=True, readonly=False, precompute=True,
                                    digits='Payment value',)
    
    @api.model
    @api.depends("payment_valor","move_id")
    def _compute_payment_valor(self):
        value = 0.00
        for line in self:
            if ( line.move_id[0]):
                invoices = self.env["account.move"].browse([line.move_id[0].id])
                _logger.info(f'MOSTRANDO INVOICES >>> { invoices }')
                value = invoices._get_default_payment_valor()
                line.payment_valor = value