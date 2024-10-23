# -*- coding: utf-8 -*-
from odoo import models, fields, registry, api
from odoo import tools
import logging
_logger = logging.getLogger(__name__)


class FetchmailServer(models.Model):

    _inherit = 'fetchmail.server'

    def fetch_mail(self):
        if tools.config.get('no_fetchmail'):
            return True
        return super(FetchmailServer, self).fetch_mail()
