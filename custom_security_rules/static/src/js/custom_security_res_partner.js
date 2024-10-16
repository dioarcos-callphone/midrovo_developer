odoo.define('custom_security_rules.custom_security_res_partner', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var rpc = require('web.rpc');

    FormController.include({
        _onButtonNew: function (event) {
            // Llamamos al método original para la creación de un nuevo registro
            this._super.apply(this, arguments);

            var self = this;

            // Habilitar permisos de escritura al hacer clic en "Nuevo"
            rpc.query({
                model: 'res.users',
                method: 'toggle_write_permission',
                args: [true],  // Habilitar permisos de escritura
            }).then(function () {
                self.$buttons.find('.o_form_button_save').show();
                self.$buttons.find('.o_form_button_cancel').show();
            });
        },

        // Sobreescribir el método para el guardado
        _onSave: function (event) {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                // Después de guardar, deshabilitar nuevamente los permisos de escritura
                rpc.query({
                    model: 'res.users',
                    method: 'toggle_write_permission',
                    args: [false],  // Deshabilitar permisos de escritura
                });
            });
        },

        // Sobreescribir el método para el descarte
        _onDiscard: function (event) {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                // Después de descartar, deshabilitar nuevamente los permisos de escritura
                rpc.query({
                    model: 'res.users',
                    method: 'toggle_write_permission',
                    args: [false],  // Deshabilitar permisos de escritura
                });
            });
        },
    });
});
