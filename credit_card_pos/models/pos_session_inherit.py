from odoo import models, fields, api

class PosSessionInherit(models.Model):
    _inherit = 'pos.session'
    
    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        if self.config_id.module_pos_hr:
            credit_card = 'credit.card'
            credit_card_info = 'credit.card.info'
            if credit_card not in result:
                result.append(credit_card)
            if credit_card_info not in result:
                result.append(credit_card_info)
        return result
    
    def _loader_params_credit_card(self):
        return {
            'search_params': { 'fields': ['name', 'tipo', 'banco'] },
        }
        
    def _loader_params_credit_card_info(self):
        return {
            'search_params': { 'fields': ['credit_card_id', 'recap', 'authorization', 'reference'] },
        }
        
    def _get_pos_ui_credit_card(self, params):
        return self.env['credit.card'].search_read(**params['search_params'])
    
    def _get_pos_ui_credit_card_info(self, params):
        return self.env['credit.card.info'].search_read(**params['search_params'])