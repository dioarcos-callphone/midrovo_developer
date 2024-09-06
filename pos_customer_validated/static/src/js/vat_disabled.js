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
                this._disableVatInput();
            }
        }

        _disableVatInput() {
            setTimeout(() => {
                const inputVat = document.querySelector("input[name='vat']");
                if (inputVat) {
                    console.log('ENTRA AL VAT DEL PARTNER')
                    inputVat.disabled = true;
                }
            }, 0);
        }

        saveChanges() {
            const processedChanges = {};
            for (const [key, value] of Object.entries(this.changes)) {
                if (this.intFields.includes(key)) {
                    processedChanges[key] = parseInt(value) || false;
                } else {
                    processedChanges[key] = value;
                }
            }
            if (
                processedChanges.state_id &&
                this.env.pos.states.find((state) => state.id === processedChanges.state_id)
                    .country_id[0] !== processedChanges.country_id
            ) {
                processedChanges.state_id = false;
            }
    
            if ((!this.props.partner.vat && !processedChanges.vat) || processedChanges.vat === "") {
                return this.showPopup("ErrorPopup", {
                    title: this.env._t("Se requiere número de identificación"),
                });
            }
            
            return super.saveChanges()
        }

    }

    Registries.Component.extend(PartnerDetailsEdit, PartnerDetailsEditExtend);

    return PartnerDetailsEdit;

});

