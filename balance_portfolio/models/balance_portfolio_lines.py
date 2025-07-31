# -*- coding: utf-8 -*-

import logging
import requests 
import json
from odoo import models, fields, api
from odoo.tools import config
_logger = logging.getLogger(__name__)
config['limit_time_real'] = 1000000
from datetime import datetime

class balance_portfolio_lines(models.Model):
    _name = 'balance.portfolio.lines'
    _description = 'balance_portfolio_lines'
    _order = 'days_order desc'


    #parameter to One2many, 
    client_id = fields.Many2one( "balance.portfolio", 
                                string="head_key",
                                required=True,
                                readonly=True,
                                index=True,
                                auto_join=True,
                                ondelete="cascade",
                                check_company=True,
                            )
    
    type = fields.Char( string = 'Tipo')
    id_register = fields.Char( string = 'Registro')
    date = fields.Datetime(string='Fecha',default=fields.Datetime.now,)
    record_date = fields.Date(string='Fecha de emision')  
    end_date = fields.Date(string='Fecha de vencimiento')  
    days = fields.Char( string = 'Dias')

    days_order = fields.Integer(string='Días', compute='_compute_days_order', store=True)

    total = fields.Char(string = 'Total')  
    balance = fields.Char(string = 'Saldo')  
    quota = fields.Char(string = 'Cupo')  
    term = fields.Char(string = 'Plazo')  
    status = fields.Selection(
        selection=[
            ("A", "Activo"),
            ("I", "Inactivo"),
            ("P", "Pendiente"),
        ],
        string="Estado",
        copy=False,
        default="A",
        index=True,
        readonly=True,
        tracking=True,
    )
    description = fields.Text(string='Observaciones')   

    @api.depends('days')
    def _compute_days_order(self):
        for record in self:
            record.days_order = int(record.days)

