from odoo import _, fields, models

class StockQuantityHistoryInherit(models.TransientModel):
    _inherit = 'stock.quantity.history'
    
    def action_pdf(self):
        """This function is for printing pdf report"""
        data = {
            'model_id': self.id,
            'product_ids': self.product_ids.ids,
            'location_ids': self.location_ids.ids,
            'category_ids': self.category_ids.ids,
            'company_ids': self.company_ids.ids,
            'age_breakdown_days': self.age_breakdown_days,
        }
        return (
            self.env.ref(
                'inventory_advanced_reports.'
                'report_inventory_age_breakdown_action')
            .report_action(None, data=data))