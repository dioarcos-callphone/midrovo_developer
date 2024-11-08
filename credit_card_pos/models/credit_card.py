from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class CreditCard(models.Model):
    _name = 'credit.card'
    _description = 'CreditCard'

    metodo_pago = fields.Many2one(
        string="Método de Pago",
        comodel_name='pos.payment.method',
    )
    
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

    

