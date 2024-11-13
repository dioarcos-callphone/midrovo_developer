from odoo import models, fields, api

class CreditCardInfo(models.Model):
    _name = "credit.card.info"
    
    pos_payment_id = fields.Many2one('pos.payment', string="Factura")
    credit_card_id = fields.Many2one('credit.card', string="Número de Tarjeta")
    recap = fields.Char(string="Recap")
    authorization = fields.Char(string="Autorización")
    reference = fields.Char(string="Referencia")