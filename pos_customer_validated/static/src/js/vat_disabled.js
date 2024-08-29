odoo.define('pos_customer_validated.vat_disabled', (require) => {
    "use strict";

    const rpc = require('web.rpc')
    const PartnerDetailsEdit = require('point_of_sale.PartnerDetailsEdit')
    const Registries = require('point_of_sale.Registries');

    const PartnerDetailsEditExtend = PartnerDetailsEdit => class extends PartnerDetailsEdit {
        setup() {
            super.setup()
            const partner = this.props.partner;
            const vat = partner.vat;

            if(vat) {
                console.log(vat)
                this._disableVatInput();
            }
        }

        _disableVatInput() {
            setTimeout(() => {
                const inputVat = document.querySelector("input[name='vat']");
                if (inputVat) {
                    inputVat.disabled = true;
                }
            }, 0);
        }

    }

    Registries.Component.extend(PartnerDetailsEdit, PartnerDetailsEditExtend);

    return PartnerDetailsEdit;

});