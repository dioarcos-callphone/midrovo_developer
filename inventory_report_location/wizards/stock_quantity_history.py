from odoo import fields, models
from odoo.tools.safe_eval import safe_eval

import logging
_logger = logging.getLogger(__name__)


class StockQuantityHistoryInherit(models.TransientModel):
    _inherit = 'stock.quantity.history'
    
    category_ids = fields.Many2many('product.category', string='Categorías',)
    location_ids = fields.Many2many('stock.location', string='Ubicaciones', domain=[('usage','in',['internal','transit'])],)
    
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
        action = super().open_at_date()
        context = action["context"]
        context = safe_eval(context) if isinstance(context, str) else context

        # Filtro por ubicación
        if self.location_ids:
            context["location"] = self.location_ids.ids  # Filtrar por varias ubicaciones
            context["compute_child"] = self.include_child_locations
            if context.get("company_owned", False):
                context.pop("company_owned")
            # Modificar el display_name para mostrar todas las ubicaciones seleccionadas
            location_names = ", ".join(self.location_ids.mapped("complete_name"))
            action["display_name"] = f"{location_names} - {action['display_name']}"

        # Filtro por categorías
        if self.category_ids:
            context["category"] = self.category_ids.ids  # Filtrar por varias categorías
            # Modificar el display_name para incluir categorías
            category_names = ", ".join(self.category_ids.mapped("name"))
            action["display_name"] = f"{category_names} - {action['display_name']}"

        action["context"] = context
        contexto = action["context"]
        _logger.info(f'MOSTRANDO CONTEXTO >>> { contexto }')
        return action
