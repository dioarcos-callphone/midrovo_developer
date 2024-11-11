from odoo import models, api

class InvoiceUpdate(models.Model):
    _inherit = "pos.order"
    
    @api.model
    def update_invoice_payments_widget(self, results):
        return ''