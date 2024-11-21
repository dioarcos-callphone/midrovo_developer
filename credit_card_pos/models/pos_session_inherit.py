from odoo import models, fields, api

class PosSessionInherit(models.Model):
    _inherit = 'pos.session'
    
    def _loader_params_pos_credit_card():
        return {
            'search_params': { 'fields': ['credit_card_info_id'] },
        }