from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class PaymentValue(models.Model):
    _inherit = 'account.move'
    
    def _get_default_forma_pago(self):
        pass
    
    @api.model
    def _l10n_ec_get_payment_data(self):
        payment_data = super(PaymentValue, self)._l10n_ec_get_payment_data()
        
        payment_data.clear()
        
        result = self.env['account.move.sri.lines'].search([], order='id desc', limit=1)
        
        _logger.info(f'MOSTRANDO RESULTADO SRI LINES >>> { result }')
        
        for element in result:
            _logger.info(f'ACCOUNT MOVE ID >>> { element.move_id }')
        
        

        return payment_data


class AccountMoveSriLines(models.Model):
    _inherit = 'account.move.sri.lines'

    def _get_default_forma_pago(self):
        pass
    

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
    
    @api.depends("payment_valor","move_id")
    def _compute_payment_valor(self):
        value = 20.00
        for line in self:
            if ( line.move_id[0]):
                invoices = self.env["account.move"].browse([line.move_id[0].id])
                value = invoices._get_default_payment_valor()
                value = 20.00
                line.payment_valor = value