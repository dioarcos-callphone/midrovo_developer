from odoo import models, fields, api

class PosCashier(models.Model):
    _inherit = 'pos.order'
    
    @api.model
    def get_invoice_field(self, id):
        pos_id = self.search([('pos_reference', '=', id)])
        
        cashier_name = pos_id.cashier
        
        res = super(PosCashier, self).get_invoice_field(id)
        
        res.update({
            'cashier_name': cashier_name,
        })

        return res