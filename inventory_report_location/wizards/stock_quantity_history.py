from odoo import fields, models
from odoo.osv import expression
from odoo.tools.misc import format_datetime

import logging
_logger = logging.getLogger(__name__)



class StockQuantityHistoryInherit(models.TransientModel):
    _inherit = 'stock.quantity.history'
    
    category_ids = fields.Many2many('product.category', string='Categorías',)
    location_ids = fields.Many2many('stock.location', string='Ubicaciones', domain=[('usage','=','internal')],)
    
    def action_pdf(self):        
        """This function is for printing pdf report"""
        data = {
            'model_id': self.id,
            'location_id': self.location_ids.ids,
            'category_ids': self.category_ids.ids,
            'date': self.inventory_datetime
        }
        return (
            self.env.ref('inventory_report_location.report_stock_quantity_history')
            .report_action(None, data=data))
        
        
    def open_at_date(self):
        action = super(StockQuantityHistoryInherit, self).open_at_date()
        
        domain = action.get('domain', [])
        
        # Agregar filtros por categoría
        if self.category_ids:
            _logger.info(f'MOSTRANDO CATEGORIES IDS >>> { self.category_ids }')
            category_ids = self.category_ids.ids
            domain = expression.AND([domain, [('categ_id.id', 'in', category_ids)]])

        # Agregar filtros por ubicación
        if self.location_ids:
            _logger.info(f'MOSTRANDO LOCATION IDS >>> { self.location_ids }')
            location_ids = self.location_ids.ids
            domain = expression.AND([domain, [('location_id.id', 'in', location_ids)]])

        # Actualizar el dominio en la acción
        action['domain'] = domain
        
        return action