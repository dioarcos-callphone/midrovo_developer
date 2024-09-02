from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class InvoiceUpdate(models.Model):
    _inherit = 'account.move'
    
    def note_update(self, note):
        
        _logger.info(f'OBTENIENDO NOTE >>> { note }')
        
        return 'ACTUALIZADO'
        