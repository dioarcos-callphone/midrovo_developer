odoo.define("credit_card_pos.CreditCardModal", (require) => {
    const PosComponent = require("point_of_sale.PosComponent");
    const Registries = rquire("point_of_sale.Registries");
    
    class CreditCardModal extends PosComponent {
        // Selecciona una tarjeta de crédito y cierra el modal
        selectCard(card) {
            this.trigger('close-popup', { card });
        }
    }
    
    CreditCardModal.template = "CreditCardModal";
    Registries.Component.add(CreditCardModal);
})
