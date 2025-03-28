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
                if isinstance(r, dict) and 'model' in r and 'res_id' in r:  # Aseguramos que r es un diccionario
                    if r.get('model') in ['account.move', 'account.withhold', 'account.remision']:  # Se agrega account.remision
                        class_model = self.env[r.get('model')]
                        record = class_model.browse(r.get('res_id'))
                        if record.xml_data_id and record.xml_data_id.state == 'authorized':
                            try:
                                file_name = xml_model.with_context(only_file=True).generate_file_name(record.xml_data_id.id, 'file_authorized')
                                r.setdefault('attachments', []).append((file_name, record.xml_data_id.xml_authorized))  # Usa setdefault para evitar KeyError
                            except Exception as e:
                                _logger.warning("Can't get xml file: %s", e)
                if isinstance(r, dict):  # Solo actualizamos si r sigue siendo un diccionario válido
                    res[key] = r
        return res
