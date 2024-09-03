from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class InvoiceUpdate(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def get_note(self, nota):
        _logger.info(f'OTENIENDO NOTA EN EL BACK >>> { nota }')
        return note