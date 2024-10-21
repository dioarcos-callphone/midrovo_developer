# -*- encoding: utf-8 -*-

from odoo import models, fields, api, netsvc, _


class WizardMessages(models.TransientModel):

    _name = 'wizard.messages'
    _description = 'Utilidad para Presentar Mensajes'

    message = fields.Text(string=u'Mensaje', required=False, readonly=True, states={}, help=u"")
    
    def action_done(self):
        
        return {'type': 'ir.actions.act_window_close'}
