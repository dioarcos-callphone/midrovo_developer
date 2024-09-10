from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class SockPickingUpdate(models.Model):
    _inherit = "stock.picking"
    
    @api.onchange('product_id')
    def _onchange_(self):
        product_id = self.product_id
        _logger.info(f'MOSTRANDO PRODUCT >>> { product_id }')