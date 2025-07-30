# -*- coding: utf-8 -*-

import logging
import requests 
import json
from odoo import models, fields, api
from odoo.tools import config

_logger = logging.getLogger(__name__)
config['limit_time_real'] = 1000000
from datetime import datetime
from itertools import groupby


class balance_portfolio(models.Model):
    _name = 'balance.portfolio'
    _description = 'balance_portfolio'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    client_id = fields.Many2one('res.partner', string='Cliente', required=True)
    client_vat = fields.Char(related='client_id.vat', string='Cédula del Cliente')
    client_detail_ids = fields.One2many('balance.portfolio.lines', 'client_id', string='Detalles de Pagos')
    sales_man =   fields.Char( string='Vendedor')
    status = fields.Selection([("A", "Activo"),("I", "Inactivo"),("P", "Pendiente")],
        string="Estado",
        copy=False,
        default="I",
        index=True,
        readonly=False, 
        tracking=True,
    )  

    current_date = fields.Date(
        string='Fecha Actual',
        compute='_compute_current_date',
        store=True
    )

    def _compute_current_date(self):
        for record in self:
            record.current_date = fields.Date.today()

    total_amount = fields.Float(string='Total', compute='_compute_total_amount')
    #balance_amount = fields.Float(string='Saldo', compute='_compute_balance_amount')
    
    @api.depends('client_detail_ids.total')
    def _compute_total_amount(self):
        for balance in self:
            total = sum(float(line.total) for line in balance.client_detail_ids)
            balance.total_amount = total

    @api.onchange('client_detail_ids')
    def _onchange_client_detail_ids(self):
        if not self.client_detail_ids:
            self.status = 'I'
        else:
            self.status = 'A'

    @api.onchange('total_amount')
    def _compute_balance_state(self):
        for balance in self:
            total = balance.total_amount
            _logger.info("API CHANGE AMOUNT %s", total)
            if total == 0:
                balance.write({'status': 'I'})  # Cambiar el estado a 'Innactivo a nivel de modelo' si el total es 0
            else:
                balance.write({'status': 'A'})  

    @api.model
    def date_format( self, date_id):
        fecha_str = date_id
        fecha_str = fecha_str.replace('.', '-') 
        _logger.info("FECHAS STRING %s", fecha_str)
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
        return fecha_obj

    @api.model
    def mark_all_inactive(self):
        cabeceras = self.search([])
        cabeceras.write({'status': 'I'})


    def crete_balance_portfolio_api(self):
        """ Crea saldo de cartera """
        lines_value = []
        count = 1
        detalles_creados = 1
        data = 0
        partern_id = self.client_id
        company_id = self.company_id
        api_url = ''
        #LLamo al api 
        api_data = self.env['api.administrator'].sudo().search(
                        [ ( 'name', '=', 'api_balance_detail_report' ),('type','=','get'),('company_id','=', company_id.id)], limit=1)
        try:
            if (api_data.id) :
                old_str = "$num_cedula"
                new_str = self.client_id.vat 
                api_url = api_data.url + api_data.end_point.strip()
                api_url_new = api_url.replace(old_str, new_str)
                headers = {
                        'Accept': 'application/json',
                        'version': '1',
                        'framework': 'PRUEBAS',
                        'userid': api_data.user_id.strip(),
                        'password': api_data.password.strip(),
                        'deviceid': '000000000000000',
                        'sessionid': '0'
                    }
                response = requests.get(api_url_new, headers= headers)
                parsed_data = response.json()
                if  parsed_data.get('success') == True :
                    count = 0
                    partners_request = parsed_data.get("data")
                    if partners_request :
                        # Elimina las líneas del balnace que no están en la lista de line_ids
                        for line in self.client_detail_ids:
                            if line.id_register not in partners_request:
                                line.unlink()                        
                        for line_list in partners_request:
                            balance_portfolio_line = []
                            balance_portfolio_line = {
                                        'client_id': self.id,
                                        'type': line_list["tipo"],
                                        'id_register': line_list["registro"],
                                        'record_date': self.date_format(line_list["fecha_emision"]),
                                        'end_date': self.date_format(line_list["fecha_vencimiento"]),
                                        'days': line_list["dias"],
                                        'total': line_list["total"],
                                        'balance': line_list["saldo"],
                                        'quota':line_list["cupo"],
                                        'term': line_list["plazo"],
                                    }
                            

                            balance_portfolio_line_new = self.env['balance.portfolio.lines'].create(balance_portfolio_line)
                            _logger.info("DEATTALES CREADOS %s", balance_portfolio_line_new.record_date)
        except Exception as e:
            _logger.error("Error al hacer la solicitud a la API: %s", str(e))
            data = {'datos': False, 'count': 0 ,'st_data':str(e)}
            return data

    @api.model
    def _crete_balance_portfolio_all( self, company_id):
        """ Crea saldo de cartera """
        try:
            data = 0
            api_url = ''
            api_data = self.env['api.administrator'].sudo().search(
                        [ ( 'name', '=', 'api_balance_detail_report_all' ),('type','=','get'),('company_id','=',company_id)], limit=1)
            
            if (api_data.id) :
                api_url = api_data.url + api_data.end_point.strip()
                _logger.info("DEATTALES CREADOS %s", api_url  )
                payload = {}
                files={}
                headers = {
                    'Accept': 'application/json',
                    'version': '1',
                    'framework': 'PRUEBAS',
                    'userid': api_data.user_id.strip(),
                    'password': api_data.password.strip(),
                    'deviceid': '000000000000000',
                    'sessionid': '0'
                }
                response = requests.get(api_url, headers= headers)
                parsed_data = response.json()
                ##si el api trae resultados
                if  parsed_data.get('success') == True :
                    self.mark_all_inactive()
                    count = 0
                    #balance_lines_request = parsed_data.get("data")
                    request = parsed_data.get("data")
                    if request :

                        request.sort(key=lambda x: x["ruc"])
                        request_data = {ruc: list(group) for ruc, group in groupby(request, key=lambda x: x["ruc"])}

                        for ruc, detail in request_data.items():
                            res_balance_portfolio = self.search([('client_vat', '=', ruc)],limit=1)
                            if res_balance_portfolio :
                                # Elimina las líneas del balnace que no están en la lista de line_ids_to_keep.
                                for line in res_balance_portfolio.client_detail_ids:
                                    if line.id_register not in detail:
                                        line.unlink() 
                                #res_balance_portfolio.client_detail_ids.unlink() # tambien funciona
                                _logger.info("balance portfolio %s", res_balance_portfolio)
                                for details in detail:
                                    lines_exist = res_balance_portfolio.client_detail_ids.filtered(lambda x: x.id_register == details['registro'])
                                    balance_portfolio_line = []
                                    balance_portfolio_line = { 
                                        'type': details['tipo'],
                                        'id_register': details['registro'],
                                        'record_date': self.date_format(details['fecha_emision']),
                                        'end_date': self.date_format(details['fecha_vencimiento']),
                                        'days': details['dias'],
                                        'total': details['total'],
                                        'balance': details['saldo'],
                                        'quota':details['cupo'],
                                        'term': details['plazo'],
                                    }
                                    if not lines_exist:
                                        agree_client = {'client_id': res_balance_portfolio.id}
                                        balance_portfolio_line.update(agree_client)
                                        balance_portfolio_line_new = self.env['balance.portfolio.lines'].create(balance_portfolio_line)
                                        _logger.info("DEATTALES CREADOS %s", balance_portfolio_line_new)
                                    else:
                                        lines_exist.write(balance_portfolio_line)
                                        #tambien funciona 
                                        # new_balance.write({'client_detail_ids': [(1, new_balance.id, balance_portfolio_line)] })
                                        _logger.info("DETALLES ACTUALIZADO ")
                                    res_balance_portfolio._compute_balance_state()
                    else :
                        _logger.error("Error 404 no existe data: %s", 0)            
        except Exception as e:
            _logger.error("Error al hacer la solicitud a la API: %s", str(e))
            data = {'datos': False, 'count': 0 ,'st_data':str(e)}
            return data


    @api.model
    def crete_balance_portfolio_head( self, partern_id, company_id):
        """ Crear cabeceras """
        res_balance_portfolio = self.search([('client_id', '=', partern_id)],limit=1)
        if not res_balance_portfolio:
            balance_vals = {'client_id': partern_id}
            new_balance = self.create(balance_vals)
            _logger.info("API BALANCE PORTFOLIO NUEVO Cliente  %s", new_balance)
        else:
            new_balance = res_balance_portfolio
            _logger.info("API BALANCE PORTFOLIO Cliente Actualizado  %s", new_balance)

        _logger.info("API CREATE USER %s", new_balance.client_id.name)

    @api.model
    def _balance_portfolio_partner_api(self, company_id = 1):
        ''' Call from cron or direct '''
        try:
            data = 0
            api_url = ''
            api_data = self.env['api.administrator'].sudo().search(
                        [ ( 'name', '=', 'balance_partner_update' ),('type','=','post'),('company_id','=',company_id)], limit=1)
            _logger.info("API INFO ARREGLO %s", api_data)
            #si existe el end point
            if (api_data.id) :
                api_url = api_data.url + api_data.end_point.strip()
                payload = {}
                files={}
                headers = {
                    'Accept': 'application/json',
                    'version': '1',
                    'framework': 'PRUEBAS',
                    'userid': api_data.user_id.strip(),
                    'password': api_data.password.strip(),
                    'deviceid': '000000000000000',
                    'sessionid': '0'
                }
                response = requests.post(api_url, headers= headers)
                parsed_data = response.json()
                ##si el api trae resultados
                if  parsed_data.get('success') == True :
                    count = 0
                    partners_request = parsed_data.get("data")
                    
                    if partners_request :
                        #se crea a los clientes
                        for elements in partners_request :
                            seller_code = elements.get('vendedor').strip()
                            res_users_id = self.env['res.users'].sudo().search(
                                        [("balance_code","=", seller_code)], limit=1)
                            #if res_users_id :
                            partner_ruc = elements.get('ruc').strip()
                            res_partner = self.env['res.partner'].sudo().search([('vat', '=', partner_ruc)],limit=1)
                            dict_q = {}
                            dict_q['name'] = elements.get('nombre').strip()
                            dict_q['vat'] = elements.get('ruc').strip()
                            if res_users_id :
                                dict_q['user_id'] = res_users_id.id
                            #_logger.info("API INFO ARREGLO %s", dict_q)
                            # no existe el cliente se lo crea
                            if not res_partner:
                                newclient = self.env['res.partner'].sudo().create(dict_q)
                                partern_id = newclient.id
                                _logger.info("API INFO CREATE USER %s", partern_id)
                                
                            else:
                                partern_id = res_partner.id
                                res_partner.write(dict_q)
                                res_partner.env.cr.commit()
                                _logger.info("API INFO UPDATE USER %s", res_partner.id)
                            # se crea el saldo de cartera toma mucho tiempo y mata al servidor
                            if partern_id :
                                self.crete_balance_portfolio_head(partern_id, company_id)
                                
        except Exception as e:
            _logger.error("Error al hacer la solicitud a la API: %s", str(e))
            data = {'datos': False, 'count': 0 ,'st_data':str(e)}
            return data


