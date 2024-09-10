from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class StockPickingUpdate(models.Model):
    _inherit = "stock.move"
    
    select_validate = []
    
    @api.onchange('product_id')
    def _onchange_(self):
        product_id = self.product_id
        
        if(product_id):    
            for select in self.select_validate:
                if select.id == product_id.id:
                    _logger.info(f'YA FUE SELECCIONADO EL PRODUCTO >>> { product_id }')
            
            self.select_validate.append(product_id)
        
        
                
        