from odoo import models, fields, api

class PosSessionInherit(models.Model):
    _inherit = 'pos.session'
    
    def _loader_params_credit_card():
        return {
            'search_params': { 'fields': ['name', 'tipo', 'banco'] },
        }
        
    def _loader_params_credit_card_info():
        return {
            'search_params': { 'fields': ['credit_card_id', 'recap', 'authorization', 'reference'] },
        }
        
    def _get_pos_ui_credit_card(self, params):
        return self.env['credit.card'].search_read(**params)
    
    def _get_pos_ui_credit_card_info(self, params):
        return self.env['credit.card.info'].search_read(**params)