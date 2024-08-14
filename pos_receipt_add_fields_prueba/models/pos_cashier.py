from odoo import models, fields, api
import logging 

_logger = logging.getLogger(__name__)

class PosCashier(models.Model):
    _inherit = 'pos.order'
    
    @api.model
    def get_invoice_field(self, id):
        pos_id = self.search([('pos_reference', '=', id)])
        
        cashier_name = pos_id.cashier
        
        res.invoice_user_id.name = cashier_name
        
        res = super(PosCashier, self).get_invoice_field(id)
        
        _logger.info(f'NAME CASHIER >>> {cashier_name}')
        
        res.update({
            'cashier_name': cashier_name,
        })

        return res
    
# class InheritAccountMove(models.Model):
#     _inherit = 'account.move'
    
#     def _l10n_ec_get_invoice_additional_info(self):
#         additional_info = super(InheritAccountMove, self)._l10n_ec_get_invoice_additional_info()

#         cashier = self.env['pos.oder'].get_invoice_field(id)

#         additional_info.update({
#             "Vendedor": self.invoice_user_id.name or '',
#         })
#         return additional_info