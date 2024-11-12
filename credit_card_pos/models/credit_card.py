from odoo import models, fields, api

class CreditCard(models.Model):
    _name = 'credit.card'
    _description = 'CreditCard'
    
    name = fields.Char(
        string='Nombre',
        required=True,
    )
    
    tipo = fields.Char(
        string="Tipo",
        required=True,
    )
    
    banco = fields.Many2one(
        comodel_name='res.bank',
        string="Banco",
    )    
    
    @api.model
    def get_cards(self):
        model_cards = self.search_read([],['id', 'name'], order='name asc')

        return model_cards
