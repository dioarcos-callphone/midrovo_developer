odoo.define('pos_customer_validated.models', function(require) {
    'use strict';

    var models = require('point_of_sale.models');

    models.load_fields('res.partner');
})