from odoo import fields, models

import logging
_logger = logging.getLogger(__name__)



class StockQuantityHistoryInherit(models.TransientModel):
    _inherit = 'stock.quantity.history'
    
    location_id = fields.Many2many(
        "stock.location", string="Ubicacion",
        domain=[('usage','=','internal')],
        help="Seleccione las ubicaciones para generar el informe")
    
    def action_pdf(self):
        _logger.info(f'MOSTRANDO DESDE EL WIZARD >>> { self.id }')
        
        """This function is for printing pdf report"""
        data = {
            'model_id': self.id,
            'product_ids': 'self.product_ids.ids',
            'location_ids': self.location_ids.ids,
            'category_ids': 'self.category_ids.ids',
            'company_ids': 'self.company_ids.ids',
            'age_breakdown_days': 'self.age_breakdown_days',
        }
        return (
            self.env.ref('inventory_report_location.report_stock_quantity_history')
            .report_action(None, data=data))