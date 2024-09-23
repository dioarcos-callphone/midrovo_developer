from odoo import fields, models

import logging
_logger = logging.getLogger(__name__)



class StockQuantityHistoryInherit(models.TransientModel):
    _inherit = 'stock.quantity.history'
    
    category_ids = fields.Many2many('product.category', string='Categorías', domain=[('usage','=','internal')],)
    location_ids = fields.Many2many('stock.location', string='Ubicaciones')
    
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
    #     tree_view_id = self.env.ref('stock.view_stock_product_tree').id
    #     form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
    #     domain = [('type', '=', 'product')]
    #     product_id = self.env.context.get('product_id', False)
    #     product_tmpl_id = self.env.context.get('product_tmpl_id', False)
    #     if product_id:
    #         domain = expression.AND([domain, [('id', '=', product_id)]])
    #     elif product_tmpl_id:
    #         domain = expression.AND([domain, [('product_tmpl_id', '=', product_tmpl_id)]])
    #     # We pass `to_date` in the context so that `qty_available` will be computed across
    #     # moves until date.
    #     action = {
    #         'type': 'ir.actions.act_window',
    #         'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
    #         'view_mode': 'tree,form',
    #         'name': _('Products'),
    #         'res_model': 'product.product',
    #         'domain': domain,
    #         'context': dict(self.env.context, to_date=self.inventory_datetime),
    #         'display_name': format_datetime(self.env, self.inventory_datetime)
    #     }
    #     return action