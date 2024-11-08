from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

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

