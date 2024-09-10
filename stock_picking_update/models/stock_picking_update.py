from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
                    raise ValidationError(f'El producto { product_id.name } ya fue seleccionado.')
            
            self.select_validate.append(product_id)
        
        
                
        