from odoo import models, fields, api
import logging 

_logger = logging.getLogger(__name__)

class PosCashier(models.Model):
    _inherit = 'pos.order'
    
    @api.model
    def get_invoice_field(self, id):
        pos_id = self.search([('pos_reference', '=', id)])
        
        cashier_name = pos_id.cashier
        
        res = super(PosCashier, self).get_invoice_field(id)
        
        # pos_id.account_move._l10n_ec_get_invoice_additional_info()['Vendedor'] = cashier_name
        # additional_info = pos_id.account_move._l10n_ec_get_invoice_additional_info()
        
        # _logger.info(f'INFORMACION ADICIONAL >>> { additional_info }')
        
        res.update({
            'cashier_name': cashier_name,
        })

        return res