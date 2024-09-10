from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class StockPickingUpdate(models.Model):
    _inherit = "stock.move"
    
    select_validate = []
    
    @api.depends('product_id', 'move_ids_without_package')
    def _onchange_(self):
        product_id = self.product_id
        
        if(product_id):
            products = self.move_ids_without_package
            
            _logger.info(f'MOSTRANDO PRODUCTOS SELECCIONADOS >>> { products }')
                
            # for select in self.select_validate:
            #     if select.id == product_id.id:
            #         raise ValidationError(f'El producto { product_id.name } ya ha sido seleccionado.')
            
            # self.select_validate.append(product_id)
        
        
                
        