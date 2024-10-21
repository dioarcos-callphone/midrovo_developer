# -*- encoding: utf-8 -*-

from odoo import models, api, fields


class UtilNotification(models.Model):

    _name = 'util.notification'
    _description = u'Notificaciones por mail'
    
    name = fields.Char(u'Nombre', size=256, required=True, )
    header = fields.Html(u'Cabecera', )
    footer = fields.Html(u'Pie de Página', )
    user_mails_ids = fields.Many2many('res.users', 'ecua_utils_notification_users_rel', 'report_id', 'user_id', 
        u'Usuarios/Envío de Correos', )
    groups_mails_ids = fields.Many2many('res.groups', 'ecua_utils_notification_group_rel', 'report_id', 'group_id', 
        u'Grupos/Envío de Correos', )
    

class UtilNotificationTask(models.Model):

    _name = 'util.notification.task'
    _description = u'Notificaciones agrupadas'
    _rec_name = 'notification_id'
    
    notification_id = fields.Many2one('util.notification', u'Notificación', required=False, index=True, )
    message = fields.Html(u'Mensaje', )
    state = fields.Selection([
        ('pending', u'Pendiente'),
        ('error', u'Error al enviar'),
        ('done', u'Enviado'),
        ],    string=u'Estado', index=True, readonly=True, default='pending', )
    
    @api.model
    def get_messages(self, task_ids, group_by_notification=True):
        """
        Devuelve el mensaje de cada notificacion
        @param group_by_notification: bool, 
                True si los mensajes se envian agrupados, un mail por cada notificacion
                False si se debe enviar un mail por cada mensaje
        """
        messages_per_notificaction = {}
        k = False
        for task in self.browse(task_ids):
            if task.state != 'pending':
                continue
            k = False
            if group_by_notification:
                k = task.notification_id and task.notification_id.id or False
            messages_per_notificaction.setdefault(k, []).append(task.message)
        for notification_id in messages_per_notificaction.keys():
            message_list = messages_per_notificaction[notification_id]
            # TODO: configurar el caracter para nueva linea(\n o <br>) 
            messages_per_notificaction[notification_id] = "<br>".join(message_list)
        return messages_per_notificaction
