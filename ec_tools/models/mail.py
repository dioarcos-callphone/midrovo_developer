# -*- coding: utf-8 -*-
#############################################################################
#                                                                           #
#Copyright (C) HackSystem, Inc - All Rights Reserved                        #
#Unauthorized copying of this file, via any medium is strictly prohibited   #
#Proprietary and confidential                                               #
#Written by Ing. Harry Alvarez <halvarezg@hacksystem.es>, 2019              #
#                                                                           #
#############################################################################
from odoo import models, fields, registry, api
from odoo import tools
import logging

_logger = logging.getLogger(__name__)


class MailMail(models.Model):
    _inherit = 'mail.mail'

    def send(self, auto_commit=False, raise_exception=False):
        if tools.config.get('no_sendmail') or self.env.context.get('no_sendmail',False):
            return True
        return super(MailMail, self).send(auto_commit, raise_exception)


    def process_email_queue(self, ids=None):
        if tools.config.get('no_sendmail') or self.env.context.get('no_sendmail',False):
            return True
        return super(MailMail, self).process_email_queue(ids)


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def _get_default_from(self):
        if tools.config.get('no_sendmail') or self.env.context.get('no_sendmail',False):
            return False
        else:
            return super(MailMessage, self)._get_default_from()


class PublisherWarrantyContract(models.AbstractModel):
    _inherit = "publisher_warranty.contract"

    def update_notification(self, cron_mode=True):
        if tools.config.get('send_odoo_contract', False):
            return super(PublisherWarrantyContract, self).update_notification(cron_mode)
        return True

    @api.model
    def _get_sys_logs(self):
        if tools.config.get('send_odoo_contract', False):
            return super(PublisherWarrantyContract, self)._get_sys_logs()
        return True

    @api.model
    def _get_message(self):
        if tools.config.get('send_odoo_contract', False):
            return super(PublisherWarrantyContract, self)._get_message()
        return False