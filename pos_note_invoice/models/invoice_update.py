from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class InvoiceUpdate(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def create(self, vals):
        vals['narration'] = 'ACTUALIZANDO NOTA DE POS'
        
        return super(InvoiceUpdate, self).create(vals)