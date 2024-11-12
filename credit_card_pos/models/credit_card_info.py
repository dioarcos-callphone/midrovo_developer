from odoo import models, fields, api

class CreditCardInfo(models.Model):
    _name = "credit.card.info"
    
    account_move_id = fields.Many2one('account.move', string="Factura")
    card_number = fields.Char(string="Número de Tarjeta")
    recap = fields.Char(string="Recap")
    authorization = fields.Char(string="Autorización")
    reference = fields.Char(string="Referencia")