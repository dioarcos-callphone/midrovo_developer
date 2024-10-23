# -*- encoding: utf-8 -*-

import base64
from .. import DEFAULT_SEPARATOR_LINE, DEFAULT_SEPARATOR_FIELD, DEFAULT_SEPARATOR_TEXT, DEFAULT_ENCODING

class CsvFile(object):
    """
    Clase base para generar archivos csv
    """
    
    @classmethod
    def Make_file(self, lines, options = None):
        def encode(s):
            return s
        if options is None:
            options = {}
        separator_field = options.get('separator_field', DEFAULT_SEPARATOR_FIELD)
        separator_text = options.get('separator_text', DEFAULT_SEPARATOR_TEXT)
        separator_line = options.get('separator_line', DEFAULT_SEPARATOR_LINE)
        mask = separator_text + "%s" + separator_text
        cols = []
        for row in lines:
            new_row = []
            for col in row:
                new_row.append(mask % encode(col))
            cols.append(separator_field.join(new_row))
        return base64.encodestring(separator_line.join(cols))
        
    