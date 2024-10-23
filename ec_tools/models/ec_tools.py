# -*- coding: utf-8 -*-#
#############################################################################
#                                                                           #
#Copyright (C) HackSystem, Inc - All Rights Reserved                        #
#Unauthorized copying of this file, via any medium is strictly prohibited   #
#Proprietary and confidential                                               #
#Written by Harry Alvarez <halvarez@cenecuador.edu.ec>, 2022                #
#                                                                           #
#############################################################################
from odoo import api, fields, models, tools, _
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import datetime
import math
import pytz

class EcTools(models.TransientModel):
    _name = 'ec.tools'
    _description = 'Utilidades Varias'

    def get_date_now(self):
        user_tz = pytz.timezone('America/Guayaquil')
        now = pytz.utc.localize(datetime.now()).astimezone(user_tz)
        now = now.date()
        return now

    @api.model
    def normal_round(self, n:float, decimals:int=0):
        expoN = n * 10 ** decimals
        if abs(expoN) - abs(math.floor(expoN)) < 0.5:
            return math.floor(expoN) / 10**decimals
        return math.ceil(expoN) / 10**decimals