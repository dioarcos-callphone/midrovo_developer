# -*- encoding: utf-8 -*-
import re
import simplejson
import json
import logging
from datetime import timedelta
from odoo import tools
from .. import DEFAULT_SEPARATOR_LINE, DEFAULT_SEPARATOR_FIELD, DEFAULT_SEPARATOR_TEXT, DEFAULT_ENCODING
from odoo import models, fields, registry, api
from odoo.tools.translate import _
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime
import base64
import pytz


def simplify_modifiers(modifiers):
    for a in ('invisible', 'readonly', 'required'):
        if a in modifiers and not modifiers[a]:
            del modifiers[a]


def transfer_modifiers_to_node(modifiers, node):
    if modifiers:
        simplify_modifiers(modifiers)
        node.set('modifiers', json.dumps(modifiers))


_logger = logging.getLogger(__name__)


class EcuaUtils(models.Model):
    '''
    Open ERP Model
    '''
    _name = 'ecua.utils'
    _description = 'Utilidades Varias'
    
    @api.model
    def validate_date(self, dateStart, dateEnd):
        """
            VALIDADOR DE FECHAS
        """
        try:
            if dateStart.length > 0 & dateEnd.length>0:
                dateStart = datetime.strptime(dateStart, DF)
                dateEnd = datetime.strptime(dateEnd, DF)
                if not (dateEnd < dateStart):
                    checker = False
                else: 
                    checker = True
            else:
                checker = False     
        except ValueError:
            _logger.debug()
            checker = False
            
        return checker

    @api.model
    def create_report(self, ids, report_service, model=None, name=False):
        files = []
        p = re.compile('[/:()<>|?*]|(\\\)')
        for res_id in ids:
            try:
                report = self.env.ref(report_service)
                report_service = report.report_name
                report_service = report.report_name

                if report.report_type not in ['qweb-html', 'qweb-pdf']:
                    raise UserError(_('Unsupported report type %s found.') % report.report_type)
                result, format = report._render_qweb_pdf(report_service, [res_id])
                result = base64.b64encode(result)
                if not name:
                    report_file = '/tmp/report_'+ str(res_id) + '.' + format
                else:
                    name = p.sub('_', name) 
                    report_file = name + '.' + format
                files += [(report_file, result)]    
            except Exception as e:
                _logger.warning(u'Error creating Report: %s', tools.ustr(e))
                continue        
        return files
    
    @api.model
    def get_data_notification(self, module, xml_id):
        res = {
               'name': '',
               'header': '',
               'emails': [],
               'footer': ''
               }
        model_model = self.env['ir.model.data']
        not_model = self.env['util.notification']
        if not module or not xml_id:
            raise UserError(_('You must set xml_id and module'))
        else:
            model_ids = model_model.search([('module','=',module), ('name','=',xml_id)])
            model = model_ids and model_ids[0] or None
            notification = model and not_model.browse(model.res_id) or None
            if notification:
                for user in notification.user_mails_ids:
                    if user.email_to_notification:
                        res['emails'].append(user.email_to_notification)
                    if user.email:
                        res['emails'].append(user.email)
                    else:
                        _logger.warning(_("User %s doesn't have email configured, you must assign email address to send notifications") % (user.name))
                for group in notification.groups_mails_ids:
                    for user in group.users:
                        if user.email:
                            res['emails'].append(user.email)
                        else:
                            _logger.warning(_("User %s doesn't have email configured, you must assign email address to send notifications") % (user.name))
                res['header'] = notification.header or ''
                res['footer'] = notification.footer or ''
                res['name'] = notification.name or ''
            return res
    
    @api.model
    def send_notification_email(self, xml_id, module, 
                                content='', name_report='', model_report='', ids_report=None, 
                                name_file_report=None, cc_mails=None, attachment_data=None):
        if not ids_report:
            ids_report = []
        if not cc_mails:
            cc_mails = []
        #attachment_data debe ser una lista de tuplas(nombre_adjunto, data_binaria)
        if not attachment_data:
            attachment_data = []
        mail_data = self.get_data_notification(module, xml_id)
        emails = []
        reports = []
        for mail in mail_data.get('emails'):
            emails.append(mail)
        for cc_mail in cc_mails:
            emails.append(cc_mail)
        if model_report:
            model_model = self.env[model_report]
            if ids_report and ids_report[0] == 0:
                reports.append(self.create_report(ids_report, name_report, model_report,  name_file_report)[0])
            else:
                for obj in model_model.browse(ids_report):
                    name = name_file_report and (name_file_report + ' - ') or ''
                    name += obj.display_name
                    reports.append(self.create_report(ids_report, name_report, model_report,  name)[0])
        attachments = reports or []
        if attachment_data:
            for line in attachment_data:
                if not isinstance(line, tuple):
                    raise UserError(_(u'Se espera lista de tuplas de dos elementos: [(nombre_archivo, data_binaria)]'))
                elif len(line) != 2:
                    raise UserError(_(u'Se espera lista de tuplas de dos elementos: [(nombre_archivo, data_binaria)]'))
                attachments.append(line)
        from_adr = tools.config.get('email_from')
        subject = mail_data.get('name')
        to_adr = emails
        header = mail_data.get('header') and (mail_data.get('header') + '\n') or '\n'
        footer = mail_data.get('footer') and (mail_data.get('footer') + '\n') or '\n'
        body = header + content + '\n' + footer + _(u'<br><br> No responder este correo, ha sido creado automÃ¡ticamente por odoo')
        if to_adr:
            mail_id = tools.email_send(from_adr, to_adr, subject, tools.ustr(body), email_bcc=[from_adr], attachments=attachments, subtype='html')
        else:
            _logger.warning(_('Notification "%s" doesn\'t have emails in users or groups assigned to send') % (mail_data.get('name','')))
        return True
    
    #http://stackoverflow.com/a/7029418
    @api.model
    def get_week_of_month(self, date):
        month = date.month
        week = 0
        while date.month == month:
            week += 1
            date -= timedelta(days=7)
        return week
    
    @api.model
    def get_weeks(self, date_start, date_end):
        res = []
        date_end_aux = datetime.strptime(date_end,DF)
        date_aux = datetime.strptime(date_start, DF)
        while True:
            week = self.get_week_of_month(date_aux)
            week_aux = date_aux
            while True:
                if week_aux.isoweekday() == 1:
                    start_week_date = week_aux
                    break
                week_aux -= timedelta(days=1)
            week_aux = date_aux
            while True:
                if week_aux.isoweekday() == 7:
                    end_week_date = week_aux
                    break
                week_aux += timedelta(days=1)
            data = {'name': _(u'Semana %s del %s al %s') % (week, start_week_date.strftime(DF), end_week_date.strftime(DF)),
                    'start_date': start_week_date,
                    'end_date': end_week_date,
                    }
            res.append(data)
            date_aux += timedelta(days=7)
            if date_aux.month != date_end_aux.month:
                if end_week_date.month != date_end_aux.month:
                    res.remove(data)
                break
        return res
    
    @api.model    
    def get_selection_item(self, model, field, value=None):
        """
        Obtener el valor de un campo selection
        @param model: str, nombre del modelo
        @param field: str, nombre del campo selection
        @param value: str, optional, valor del campo selection del cual obtener el string
        @return: str, la representacion del campo selection que se muestra al usuario
        """
        try:
            field_val = value
            if field_val:
                return dict(self.env[model].fields_get(allfields=[field])[field]['selection'])[field_val]
            return ''
        except Exception:
            return ''
        
    def lista_sin_repeticiones(self, lista, elemento):
        
        existe = False
        for el in lista:
            if el == elemento:
                existe = True
                break
        if existe:
            return lista
        else:
            lista.append(elemento)
            return lista

    def replace_character_especial(self, string_to_reeplace, list_characters=[]):
        """
        Reemplaza caracteres por otros caracteres especificados en la lista
        @param string_to_reeplace:  string a la cual reemplazar caracteres
        @param list_characters:  Lista de tuplas con dos elementos(elemento uno el caracter a reemplazar, elemento dos caracter que reemplazara al elemento uno)
        @return: string con los caracteres reemplazados
        """
        if not list_characters:
            list_characters=[(u'á','a'),(u'à','a'),(u'ä','a'),(u'â','a'),(u'Á','A'),(u'À','A'),(u'Ä','A'),(u'Â','A'),
                               (u'é','e'),(u'è','e'),(u'ë','e'),(u'ê','e'),(u'É','E'),(u'È','E'),(u'Ë','E'),(u'Ê','E'),
                               (u'í','i'),(u'ì','i'),(u'ï','i'),(u'î','i'),(u'Í','I'),(u'Ì','I'),(u'Ï','I'),(u'Î','I'),
                               (u'ó','o'),(u'ò','o'),(u'ö','o'),(u'ô','o'),(u'Ó','O'),(u'Ò','O'),(u'Ö','O'),(u'Ô','O'),
                               (u'ú','u'),(u'ù','u'),(u'ü','u'),(u'û','u'),(u'Ú','U'),(u'Ù','U'),(u'Ü','U'),(u'Û','U'),
                               (u'ñ','n'),(u'Ñ','N'),(u'/','-'), (u'&','Y'),(u'º',''), (u'´', '')]
        for character in list_characters:
            string_to_reeplace= string_to_reeplace.replace(character[0],character[1])
        return string_to_reeplace
    
    def unlink_function_field_calculate(self, pool_obj, model, field, context=None):
        """
        Elimina la linea que tiene la informacion de las funciones a llamar en los campos funcionales
        @param pool_obj: objeto osv_pool
        @param model: nombre del modelo del cual eliminar items
        @param field: nombre del campo calculado del cual eliminar funciones 
        @return: True si se elimina con exito
        """
        info_funct = pool_obj._store_function.get(model,[])
        index = 0
        #las funciones que se llaman para recalcular un campo funcional se almacenan en un diccionario _store_function en el objeto osv_pool
        #este diccionario tiene como clave el modelo sobre el que se va a obtener ids para calcular el campo
        #y como valor una tupla del store={'object_name':(function_name,['field_name1', 'field_name2'],priority)}
        # como el ejemplo (object_name, campo_calcular, function_name, ['field_name1', 'field_name2'],priority)
        for line in info_funct:
            if isinstance(line, tuple) and len(line) > 1:
                if line[1] == field:
                    del info_funct[index]
            index += 1
        return True
    
    @api.model
    def _change_time_zone(self, date, from_zone = None, to_zone = None):
        """
        Cambiar la informacion de zona horaria a la fecha
        En caso de no pasar la zona horaria destino, tomar la zona horaria del usuario
        @param date: Object datetime to convert according timezone in format '%Y-%m-%d %H:%M:%S'
        @return: datetime according timezone
        """
        user = self.env.user
        if not from_zone:
            #get timezone from user
            try:
                from_zone = user.tz and pytz.timezone(user.tz) or\
                 self.env.context.get('tz') and pytz.timezone(self.env.context['tz']) or pytz.UTC 
            except pytz.UnknownTimeZoneError:
                pass        #get UTC per Default
        if not to_zone:
            to_zone = pytz.UTC
        #si no hay informacion de zona horaria, establecer la zona horaria
        if not date.tzinfo:
            date = from_zone.localize(date)
        date = date.astimezone(to_zone)
        return date
    
    @api.model
    def show_wizard(self, model, id_xml, name, target='new', nodestroy=True, res_id=None):
        obj_model = self.env['ir.model.data']
        model_datas = obj_model.search([('model','=','ir.ui.view'),('name','=',id_xml)])
        resource_id = model_datas and model_datas[0] and model_datas[0].res_id or None
        action = {
            'name': name,
            'view_type': 'form',
            'view_mode': 'form',
            'nodestroy': nodestroy, 
            'res_model': model,
            'views': [(resource_id,'form')],
            'type': 'ir.actions.act_window',
            'target': target,
            'context': self.env.context,
                }
        if res_id:
            action.update({
                'res_id': res_id,
                })
        return action 
    
    @api.model
    def show_message(self, message, title='Mensaje'):
        message_obj = self.env['wizard.messages']
        wizard_id = message_obj.create({'message': message})
        return self.show_view(name=title, model='wizard.messages', id_xml='ec_tools.wizard_messages_form_view', res_id=wizard_id)
    
    @api.model    
    def show_view(self, name, model, id_xml, res_id=None, view_mode='tree,form', nodestroy=True, target='new'):
        mod_model = self.env['ir.model.data']
        view_model = self.env['ir.ui.view']
        module = ""
        if "." in id_xml:
            module, id_xml = id_xml.split(".", 1)
        res = mod_model.check_object_reference(module, id_xml)
        view_id = res and res[1] or False
        if view_id:
            view = view_model.browse(view_id)
            view_mode = view.type
        ctx = self.env.context.copy()
        ctx.update({'active_model': model})
        res = {'name': name,
                'view_type': 'form',
                'view_mode': view_mode,
                'view_id': view_id,
                'res_model': model,
                'res_id': res_id,
                'nodestroy': nodestroy,
                'target': target,
                'type': 'ir.actions.act_window',
                'context': ctx,
                }
        return res
    
    @api.model
    def show_action(self, id_xml, domain=None):
        if domain is None:
            domain = []
        #pasar el domain a una lista en caso de no serlo
        if not isinstance(domain, list):
            try:
                domain = list(domain)
            except:
                domain = []
        mod_model = self.env['ir.model.data']
        act_model = self.env['ir.actions.act_window']
        module = ""
        if "." in id_xml:
            module, id_xml = id_xml.split(".", 1)
        result = mod_model.check_object_reference(module, id_xml)
        res_id = result and result[1] or False
        result = act_model.browse(res_id).read()[0]
        domain_action = []
        if result['domain']:
            domain_action = eval(result['domain'])
        domain.extend(domain_action)
        result['domain'] = domain
        return result
    
    @api.model
    def print_report(self, report_name, model_name, ids):
        if isinstance(ids, (int)):
            ids = [ids]
        model = self.env[model_name]
        if ids:
            records = model.browse(ids)
        #Si no me pasan nada al reporte puedo asumir que no queria nada mas 
        else:
            #FIXME: Deberia asegurarme que exista al menos un registro, y evitar tambien traer totas los registro
            records = model.search([], limit=1)
        datas = {
                 'ids': ids,
                 'model': model_name,
                }
        return self.env['report'].get_action(records, report_name, data=datas)
    
    @api.model    
    def read_file(self, file, options = None):
        """
        lee un archivo binario
        :options: data for read file, keys(encoding,separator_line,separator_field,separator_text)
        :returns: [[str,str,...], [str,str,...],....]
        """
        if options is None:
            options = {}
        lines_read = []    
        lines_process = []
        errors = []
        separator_line = str(options.get('separator_line', DEFAULT_SEPARATOR_LINE))
        separator_field = str(options.get('field_delimiter', DEFAULT_SEPARATOR_FIELD))
        separator_text = str(options.get('text_delimiter', DEFAULT_SEPARATOR_TEXT))
        encoding = str(options.get('encoding', DEFAULT_ENCODING))
        try:
            lines_file = base64.decodestring(file).split(separator_line)
        except UnicodeDecodeError as er:
            raise UserError(_(u'Error to read file, please choose encoding, Field delimiter and text delimiter right. \n More info %s' % (tools.ustr(er))))
        except Exception as e:
            raise UserError(_(u'Error to read file. \nMore info %s' % (tools.ustr(e))))
        for row in lines_file:
            #leer cada linea, separando cada campo
            try:
                line = row.split(separator_field)
            except UnicodeDecodeError:
                raise UserError(_(u'Error to read file, please choose encoding, Field delimiter and text delimiter right'))
            lines_read.append(line)
        #cada linea codificarla como utf-8, para prevenir problemas de caracteres especiales
        for line in lines_read:
            if line:
                try:
                    lines_process.append(map(lambda x:x.decode(encoding).encode('utf-8').replace(separator_text,''), line))
                except UnicodeDecodeError as e:
                    errors.append(_(u"Error reading file, Encoding %s is incorrect. Line %s, More info %s" % (encoding, line,tools.ustr(e))))
                except Exception as e:
                    errors.append(_(u"Error reading file, Line %s not valid. More info %s" % (line, tools.ustr(e) ))) 
        #FIX: algunos archivos tienen caracteres especiales, quitar esos caracteres
        data_aux = []
        characters = ['\r','\t']
        for line in lines_process:
            new_r = []
            for r in line:
                for c in characters:
                    r = r.replace(c,'')
                new_r.append(r)
            if any(new_r):
                data_aux.append(new_r)
        lines_process = data_aux[:]
        return lines_process, errors
    
    def get_field_value(self, fields_required, object_list, raise_error=False):
        """
        devuelve el valor del(os) campo(s) solicitado(s), buscando en la lista de modelos dados
        si son varios campos requeridos, todos deben estar configurados en el mismo objeto
        si falta un campo, seguir evaluando los demas objetos
        @param field_required: lista de campos solicitado
        @param object_list: lista de objetos browse_record, el orden de la lista, determina la prioridad de busqueda
        @return: dict (k,v), (field, value), diccionario con los valores solicitados
        """

        def get_objects_name():
            object_name = []
            for o in object_list:
                object_name.append(u'%s %s' % (o._name, o._description))
            return " o ".join(object_name)
        
        def build_msj():
            
            res_model_pool = self.env[object_list[0]._name]
            fields_info = res_model_pool.fields_get(fields_required)
            field_name = ""
            for f in fields_info:
                #si es un campo de unidad de medida no mostrarlo en el label
                if fields_info.get(f,{}).get('type','') == 'many2one' and fields_info.get(f,{}).get('relation','') == 'product.uom':
                    continue
                field_name += "%s, " % fields_info.get(f,{}).get('string',f)
            
            msj = _(u"You must be configure Fields: %s In: %s" % (field_name, get_objects_name()))
            return msj
        fields_invalid = []
        res = {}
        #pasar un valor por defecto
        for f in fields_required:
            res[f] = None
        if not fields_required:
            return res
        if not object_list:
            object_list = []
        done_all = False
        #recorrer cada objeto para encontrar los campos requeridos
        for obj in object_list:
            res_model = self.env[obj._name]
            for f in fields_required:
                if not f in res_model._fields:
                    if not f in fields_invalid:
                        fields_invalid.append(f)
                    continue
                #si el campo si pertenece al modelo
                #pero en un modelo anterior no estaba
                #sacarlo de la lista de campos no encontrados
                else:
                    if f in fields_invalid:
                        fields_invalid.remove(f)
                res[f] = obj[f]
                #los campos deben estan configurados todos en el mismo objeto
                #en caso de faltar un campo, seguir buscando en los demas objetos
            done = True
            for f2 in res:
                if not f2 in res_model._fields:
                    if not f2 in fields_invalid:
                        fields_invalid.append(f)
                    done = False
                    continue
                #si el campo si pertenece al modelo
                #pero en un modelo anterior no estaba
                #sacarlo de la lista de campos no encontrados
                else:
                    if f2 in fields_invalid:
                        fields_invalid.remove(f2)
                col_info = res_model._fields[f2]
                #FIX: si es un campo boolean, y esta en False, se debe aceptar como configurado
                if col_info.type == 'boolean':
                    continue
                if col_info.type == 'float':
                    #si es campo float y tiene 0, solo si es el ultimo objeto, darlo como configuracion valida
                    if obj != object_list[-1] and res[f2] == 0.0:
                        #por un campo que no este configurado
                        #pasar al siguiente objeto
                        done = False
                        break
                    if res[f2] < 0.0:
                        #por un campo que no este configurado
                        #pasar al siguiente objeto
                        done = False
                        break        
                elif not res[f2]:
                    #por un campo que no este configurado
                    #pasar al siguiente objeto
                    done = False
                    break
            if done:
                done_all = True
                break
        #si hay campos que no existen en el modelo
        #mostrar error
        if fields_invalid:
            raise UserError(_(u'Fields: %s not found in Objects : %s' % (",".join(fields_invalid), get_objects_name())))
        if not done_all and raise_error:
            raise UserError(build_msj())
        return res
        
    @api.model
    def GetSQLProductStock(self, product_ids, location_ids, lot_ids=None, date_from=None, date_to=None, group_by_location=False, fields_select=None):
        field_data = {
            'qty_available': 'COALESCE(SUM(report.qty_available),0) AS ',
            'price_unit': """CASE WHEN COALESCE(SUM(report.qty_available),0) > 0 THEN COALESCE(SUM(report.valuation),0) / COALESCE(SUM(report.qty_available),0)
                            ELSE 0 END AS """,
            'valuation': 'COALESCE(SUM(report.valuation),0) AS ',
            'virtual_available': 'COALESCE(SUM(report.qty_available),0) + COALESCE(SUM(report.incoming),0) - COALESCE(SUM(report.outgoing),0) AS ',
            'incoming_qty': 'SUM(incoming) AS ',
            'outgoing_qty': 'SUM(outgoing) AS ',
                        
        }
        if not fields_select:
            fields_select = [('qty_available', 'qty_available'),
                            ('price_unit', 'price_unit'),
                            ('valuation', 'valuation'),
                            ('virtual_available', 'virtual_available'),
                            ('incoming_qty', 'incoming_qty'),
                            ('outgoing_qty', 'outgoing_qty'),
                            ]
        if not lot_ids:
            lot_ids = []
        extra_where, extra_where_quant = "", ""
        extra_select = []
        params = {'product_ids': tuple(product_ids),
                  'location_ids': tuple(location_ids),
                  }
        if date_from:
            extra_where += " AND sm.date >= %(date_from)s"
            extra_where_quant += " AND quant.in_date >= %(date_from)s"
            params['date_from'] = date_from
        if date_to:
            extra_where += " AND sm.date < %(date_to)s"
            extra_where_quant += " AND quant.in_date < %(date_to)s"
            params['date_to'] = date_to
        if lot_ids:
            extra_where += " AND sm.restrict_lot_id IN %(lot_ids)s"
            extra_where_quant += " AND quant.lot_id IN %(lot_ids)s"
            params['lot_ids'] = tuple(lot_ids)
        for field, alias in fields_select:
            if field in field_data:
                extra_select.append(field_data[field] + alias)
        if extra_select:
            extra_select =  ",".join(extra_select)
            extra_select = "," + extra_select
        else:
            extra_select = ""
        SQL = """
            SELECT P.id AS product_id
                """ + extra_select + """
            FROM product_product P
                LEFT JOIN 
                    (SELECT 
                        product_id, 
                        SUM(qty) AS qty_available,
                        SUM(valuation) AS valuation,
                        0 AS incoming, 0 AS outgoing
                        FROM 
                            (SELECT 
                                quant.product_id AS product_id,
                                quant.quantity AS qty,
                                (quant.quantity * coalesce((select cost from product_price_history 
                                    where product_id = quant.product_id
                                    order by datetime desc limit 1
                                    ),0)) AS valuation
                            FROM stock_quant AS quant
                            WHERE 
                                quant.product_id IN %(product_ids)s
                                AND quant.location_id IN %(location_ids)s 
                                """+extra_where_quant+"""
                    ) AS product_stock_available 
                    GROUP BY product_id
                    UNION ALL
                        SELECT 
                            prod AS product_id, 
                            0 as qty_available,
                            0 as valuation, 
                            SUM(stock_in_out_data.in) AS incoming,
                            SUM(stock_in_out_data.out) AS outgoing
                        FROM
                            (SELECT 
                                product_id AS prod,
                                SUM(product_qty) AS in,
                                0 as out
                            FROM stock_move sm
                            WHERE 
                                product_id IN %(product_ids)s
                                AND sm.location_id NOT IN %(location_ids)s 
                                AND sm.location_dest_id IN %(location_ids)s
                                AND sm.state IN ('confirmed', 'waiting', 'assigned') """+extra_where+"""
                                GROUP BY product_id
                            UNION
                            SELECT
                                product_id AS prod, 
                                0 AS in, 
                                SUM(product_qty) AS out 
                            FROM stock_move sm
                            WHERE product_id IN %(product_ids)s
                                AND sm.location_id IN %(location_ids)s
                                AND sm.location_dest_id NOT IN %(location_ids)s
                                AND sm.state IN ('confirmed', 'waiting', 'assigned') """+extra_where+"""
                            GROUP BY product_id
                            ) AS stock_in_out_data
                            GROUP BY prod
                ) report ON (P.id = report.product_id)
            WHERE P.id IN %(product_ids)s
            GROUP BY P.id 
            ORDER BY P.id
        """
        return SQL, params
    
    @api.model
    def GetProductStock(self, product_ids, location_ids, lot_ids=None, date_from=None, date_to=None, group_by_location=False):
        SQL, params = self.GetSQLProductStock(product_ids, location_ids, lot_ids, date_from, date_to, group_by_location)
        self.env.cr.execute(SQL, params)
        return self.env.cr.dictfetchall()
    
    @api.model
    def find_node(self, node_root, node_find, node_type="field", node_attribute="name"):
        nodes = node_root.xpath("//%s[@%s='%s']" % (node_type, node_attribute, node_find))
        return nodes 
    
    @api.model
    def set_node_modifiers(self, nodes, node_modifiers):
        for node in nodes:
            #tomar los atributos actuales y solo modificar los nuevos
            modifiers_curr = node.get('modifiers', {})
            try:
                modifiers_curr = simplejson.loads(modifiers_curr)
            except Exception as e:
                modifiers_curr = {}
            modifiers_curr.update(node_modifiers)
            transfer_modifiers_to_node(modifiers_curr, node)
        return nodes
    
    @api.model
    def set_node(self, nodes, attribute, value):
        for node in nodes:
            node.set(attribute, value)
        return nodes
    
    @api.model
    def find_set_node(self, node_root, node_find, node_modifiers, node_type="field", node_attribute="name"):
        nodes = self.find_node(node_root, node_find, node_type, node_attribute)
        return self.set_node_modifiers(nodes, node_modifiers)
    
    @api.model
    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    @api.model
    def _insert_into_mogrify(self, table_name, values):
     
        if values:
     
            fields_name = values[0].keys()
            
            values_insert = map(tuple, [v.values() for v in values])
            SQL = self.env.cr.mogrify("INSERT INTO " + table_name + " (" + ", ".join(fields_name) + ") values " + ','.join(["%s"] * len(values)), values_insert)
            self.env.cr.execute(SQL)
        return True
    
    def _ensure_zero_values(self, dict_data):
        if not dict_data: dict_data = {}
        for key in dict_data.keys():
            if not dict_data.get(key): dict_data[key] = 0.0
        return dict_data
    
    def float_to_str_time(self, value):
        if value:
            if isinstance(value, (float, int)):
                value = float(value)
                value = str(value)
            if len(value) >= 3:
                asplit = value.split('.')
                return '%02d:%02d' % (int(asplit[0]) , int(float('0.' + asplit[1]) *  60))
        return ''

    def get_next_char(self, character):
        list_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
                           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
                           'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
                           'U', 'V', 'W', 'X', 'Y', 'Z']
        current_index = list_characters.index(character)
        if current_index >= len(list_characters):
            return list_characters[0], True
        else:
            return list_characters[current_index + 1], False

    @api.model
    def _clean_str(self, string_to_reeplace, list_characters=None):
        """
        Reemplaza caracteres por otros caracteres especificados en la lista
        @param string_to_reeplace:  string a la cual reemplazar caracteres
        @param list_characters:  Lista de tuplas con dos elementos(elemento uno el caracter a reemplazar, elemento dos caracter que reemplazara al elemento uno)
        @return: string con los caracteres reemplazados
        """
        if not string_to_reeplace:
            return string_to_reeplace
        caracters = ['.',',','-','\a','\b','\f','\n','\r','\t','\v']
        for c in caracters:
            string_to_reeplace = string_to_reeplace.replace(c, '')
        if not list_characters:
            list_characters=[(u'á','a'),(u'à','a'),(u'ä','a'),(u'â','a'),(u'Á','A'),(u'À','A'),(u'Ä','A'),(u'Â','A'),
                               (u'é','e'),(u'è','e'),(u'ë','e'),(u'ê','e'),(u'É','E'),(u'È','E'),(u'Ë','E'),(u'Ê','E'),
                               (u'í','i'),(u'ì','i'),(u'ï','i'),(u'î','i'),(u'Í','I'),(u'Ì','I'),(u'Ï','I'),(u'Î','I'),
                               (u'ó','o'),(u'ò','o'),(u'ö','o'),(u'ô','o'),(u'Ó','O'),(u'Ò','O'),(u'Ö','O'),(u'Ô','O'),
                               (u'ú','u'),(u'ù','u'),(u'ü','u'),(u'û','u'),(u'Ú','U'),(u'Ù','U'),(u'Ü','U'),(u'Û','U'),
                               (u'ñ','n'),(u'Ñ','N'),(u'/','-'), (u'&','Y'),(u'º',''), (u'´', '')]
        for character in list_characters:
            string_to_reeplace = string_to_reeplace.replace(character[0],character[1])
        SPACE = ' '
        #en range el ultimo numero no es inclusivo asi que agregarle uno mas
        #espacio en blanco
        range_ascii = [32]
        #numeros
        range_ascii += range(48, 57+1)
        #letras mayusculas
        range_ascii += range(65,90+1)
        #letras minusculas
        range_ascii += range(97,122+1)
        for c in string_to_reeplace:
            try:
                codigo_ascii = ord(c)
            except TypeError:
                codigo_ascii = False
            if codigo_ascii:
                #si no esta dentro del rang ascii reemplazar por un espacio
                if codigo_ascii not in range_ascii:
                    string_to_reeplace = string_to_reeplace.replace(c,SPACE)
            #si no tengo codigo ascii, posiblemente dio error en la conversion
            else:
                string_to_reeplace = string_to_reeplace.replace(c,SPACE)
        return ''.join(string_to_reeplace.splitlines())
    
    def get_xlsx_formats(self, workbook):
        FORMATS = {
            'bold' : workbook.add_format({'bold': True, 'text_wrap': True}),
            'number' : workbook.add_format({'num_format': '#,##0.00'}),
            'money' : workbook.add_format({'num_format': '$#,##0.00'}),
            'number_bold' : workbook.add_format({'num_format': '#,##0.00', 'bold': True}),
            'money_bold' : workbook.add_format({'num_format': '$#,##0.00', 'bold': True}),
            'date': workbook.add_format({'num_format': 'dd/mm/yyyy'}),
            'datetime': workbook.add_format({'num_format': 'dd/mm/yyyy h:m:s'}),
            'date_bold': workbook.add_format({'num_format': 'dd/mm/yyyy', 'bold': True}),
            'datetime_bold': workbook.add_format({'num_format': 'dd/mm/yyyy h:m:s', 'bold': True}),
            'merge_center': workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': True}),
        }
        return FORMATS

    LETTERS = list(map(chr, range(65, 90)))

    @api.model
    def toDigits(self, n, b):
        """Convert a positive number n to its digit representation in base b."""
        digits = []
        if n == 0:
            digits.append(0)
        while n > 0:
            digits.insert(0, n % b)
            n = n // b
        return digits

    @api.model
    def GetLetterForPosition(self, position):
        numbers = self.toDigits(position, (len(self.LETTERS) - 1))
        pos = [self.LETTERS[n] for n in numbers]
        return ''.join(pos)
    
    @api.model
    def get_xml_for_report(self, record):
        return '%s/%s' % (record._name, record.id)
    
    @api.model
    def get_record_from_report_id(self, xml_id):
        model_name, record_id = xml_id.split('/')
        model = self.env[model_name]
        return id and model.browse(int(record_id)) or model.browse()
