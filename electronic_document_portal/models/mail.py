from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)

class MailTemplate(models.Model):
    _inherit = 'mail.template'

    def generate_email(self, res_ids, fields=None):
        res = super().generate_email(res_ids, fields)
        xml_model = self.env['sri.xml.data']
        multi_mode = True
        if isinstance(res_ids, int):
            multi_mode = False
        if multi_mode:
            aux = res.copy()
            for key in aux.keys():
                r = aux[key]
                if 'model' in r and 'res_id' in r:
                    if r.get('model') == 'account.remision': # Se anade account remision para mostrar xml cuando se envia al correo
                        class_model = self.env[r.get('model')]
                        record = class_model.browse(r.get('res_id'))
                        if record.xml_data_id and record.xml_data_id.state == 'authorized':
                            try:
                                file_name = xml_model.with_context(only_file=True).generate_file_name(record.xml_data_id.id, 'file_authorized')
                                r['attachments'].append((file_name, record.xml_data_id.xml_authorized))
                            except:
                                _logger.warning("Can't get xml file")

                res.update(r)
        return res
    