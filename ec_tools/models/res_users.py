# -*- encoding: utf-8 -*-

from odoo import models, fields, api, netsvc, _


class ResUsers(models.Model):

    _inherit = 'res.users'

    email_to_notification = fields.Char(string=u'Email para Notificaciones', index=True, 
                                        required=False, readonly=False, states={}, help=u"")
    #Se reemplaza el campo original para usar el campo de la notificacion de emails
    email = fields.Char(string=u'Email', index=True, 
                        required=False, readonly=False, states={}, help=u"")  
    
    def write(self, vals):
        if 'email_to_notification' in vals:
            vals['email'] = vals.get('email_to_notification')
        return super().write(vals)
    
    @api.model
    def create(self, vals):
        if 'email_to_notification' in vals:
            vals['email'] = vals.get('email_to_notification')
        return super().create(vals)
