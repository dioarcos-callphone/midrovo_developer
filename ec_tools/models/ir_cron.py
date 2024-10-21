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


class IrCron(models.Model):
    _inherit = 'ir.cron'

    @classmethod
    def _process_jobs(cls, db_name):
        if tools.config.get('no_cron'):
            return True
        return super(IrCron, cls)._process_jobs(db_name)
