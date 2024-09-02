from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class InvoiceUpdate(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def write(self, vals):
        vals['narration'] = 'ACTUALIANDO NOTA EN POS'
        
        return super(InvoiceUpdate, self).write(vals)