from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class StockPickingUpdate(models.Model):
    _inherit = "stock.move"
    
    @api.onchange('product_id')
    def onchange_field(self):
        product_id = self.product_id
        move_ids = self.move_ids_without_package
        _logger.info(f'OBTENIENDO MOVE LINES >>> { move_ids }')
        _logger.info(f'OBTENIENDO PRODUCT ID >>> { product_id }')
        
        
    # select_validate = []
    
    # @api.onchange('product_id')
    # def _onchange_(self):
    #     product_id = self.product_id
        
    #     if(product_id):
    #         _logger.info(f'MOSTRANDO PRODUCTOS SELECCIONADOS >>> { product_id }')
    #         for select in self.select_validate:
    #             if select.id == product_id.id:
    #                 raise ValidationError(f'El producto { product_id.name } ya ha sido seleccionado.')
            
    #         self.select_validate.append(product_id)
            
    # def action_confirm(self):
    #     super(StockPickingUpdate, self).action_confirm()

    #     # Acceder a las líneas que se han añadido en el campo move_line_ids
    #     for line in self.move_line_ids:
    #         _logger.info(f"Línea añadida: { line.product_id.name }")
        
    
        
        
                
        