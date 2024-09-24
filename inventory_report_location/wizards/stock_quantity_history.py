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
        
        
    # def open_at_date(self):
    #     action = super(StockQuantityHistoryInherit, self).open_at_date()
        
    #     domain = action.get('domain', [])
        
    #     # Agregar filtros por categoría
    #     if self.category_ids:
    #         _logger.info(f'MOSTRANDO CATEGORIES IDS >>> {self.category_ids}')
    #         category_ids = self.category_ids.ids
    #         domain = expression.AND([domain, [('categ_id', 'in', category_ids)]])  # Cambio aquí: categ_id en lugar de categ_id.id
        
    #     # Agregar filtros por ubicación
    #     if self.location_ids:
    #         _logger.info(f'MOSTRANDO LOCATION IDS >>> {self.location_ids}')
    #         location_ids = self.location_ids.ids
    #         _logger.info(f'LOCATION IDS >>> {location_ids}')
            
    #         # Buscar los productos en las ubicaciones
    #         quants = self.env['stock.quant'].search([('location_id', 'in', location_ids)])
    #         product_ids = quants.mapped('product_id')  # Obtenemos los IDs de los productos
    #         _logger.info(f'PRODUCT IDS >>> {product_ids.ids}')
            
    #         # Filtrar por productos en las ubicaciones seleccionadas
    #         domain = expression.AND([domain, [('id', 'in', product_ids.ids)]])
        
    #     # Actualizar el dominio en la acción
    #     action['domain'] = domain
        
    #     _logger.info(f"Final domain: {action['domain']}")
        
    #     return action
    
    # def open_at_date(self):
    #     action = super(StockQuantityHistoryInherit, self).open_at_date()
        
    #     domain = action.get('domain', [])
        
    #     # Agregar filtros por categoría
    #     if self.category_ids:
    #         _logger.info(f'MOSTRANDO CATEGORIES IDS >>> {self.category_ids}')
    #         category_ids = self.category_ids.ids
    #         domain = expression.AND([domain, [('categ_id', 'in', category_ids)]])
        
    #     # Agregar filtros por ubicación
    #     if self.location_ids:
    #         _logger.info(f'MOSTRANDO LOCATION IDS >>> {self.location_ids}')
    #         location_ids = self.location_ids.ids
    #         _logger.info(f'LOCATION IDS >>> {location_ids}')
            
    #         # Buscar los productos y sus cantidades por ubicación
    #         quants = self.env['stock.quant'].search([
    #             ('location_id', 'in', location_ids)
    #         ])
            
    #         # Crear un diccionario para almacenar la cantidad por producto por ubicación
    #         product_quantities = {}
            
    #         for quant in quants:
    #             product_id = quant.product_id.id
    #             if product_id not in product_quantities:
    #                 product_quantities[product_id] = 0.0
    #             product_quantities[product_id] += quant.quantity
            
    #         # Obtener los IDs de productos
    #         product_ids = list(product_quantities.keys())
            
    #         _logger.info(f'PRODUCT IDS >>> {product_ids}')
            
    #         # Filtrar solo por productos en las ubicaciones seleccionadas
    #         domain = expression.AND([domain, [('id', 'in', product_ids)]])
        
    #     # Actualizar el dominio en la acción
    #     action['domain'] = domain
        
    #     _logger.info(f"Final domain: {action['domain']}")
        
    #     return action
    
    # def open_at_date(self):
    #     active_model = self.env.context.get('active_model')
        
    #     # Si estamos en el modelo 'stock.valuation.layer', aplicar el filtro específico
    #     if active_model == 'stock.valuation.layer':
    #         action = self.env["ir.actions.actions"]._for_xml_id("stock_account.stock_valuation_layer_action")
    #         action['domain'] = [('create_date', '<=', self.inventory_datetime), ('product_id.type', '=', 'product')]
    #         action['display_name'] = format_datetime(self.env, self.inventory_datetime)
    #         return action

    #     # Continuar con la lógica heredada de StockQuantityHistoryInherit
    #     action = super(StockQuantityHistoryInherit, self).open_at_date()
        
    #     domain = action.get('domain', [])
        
    #     # Agregar filtros por categoría
    #     if self.category_ids:
    #         _logger.info(f'MOSTRANDO CATEGORIES IDS >>> {self.category_ids}')
    #         category_ids = self.category_ids.ids
    #         domain = expression.AND([domain, [('categ_id', 'in', category_ids)]])
        
    #     # Agregar filtros por ubicación
    #     if self.location_ids:
    #         _logger.info(f'MOSTRANDO LOCATION IDS >>> {self.location_ids}')
    #         location_ids = self.location_ids.ids
    #         _logger.info(f'LOCATION IDS >>> {location_ids}')
            
    #         # Buscar los productos y sus cantidades por ubicación
    #         quants = self.env['stock.quant'].search([('location_id', 'in', location_ids)])
            
    #         # Crear un diccionario para almacenar la cantidad por producto por ubicación
    #         product_quantities = {}
            
    #         for quant in quants:
    #             product_id = quant.product_id.id
    #             if product_id not in product_quantities:
    #                 product_quantities[product_id] = 0.0
    #             product_quantities[product_id] += quant.quantity
            
    #         # Obtener los IDs de productos
    #         product_ids = list(product_quantities.keys())
            
    #         _logger.info(f'PRODUCT IDS >>> {product_ids}')
            
    #         # Filtrar solo por productos en las ubicaciones seleccionadas
    #         domain = expression.AND([domain, [('id', 'in', product_ids)]])
        
    #     # Actualizar el dominio en la acción
    #     action['domain'] = domain
        
    #     _logger.info(f"Final domain: {action['domain']}")
        
    #     return action
    
    
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
        return action