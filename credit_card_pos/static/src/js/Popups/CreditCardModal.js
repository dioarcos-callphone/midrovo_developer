import PosComponent from "@point_of_sale/js/PosComponent";
import Registries from "@point_of_sale/js/Registries";

class CreditCardModal extends PosComponent {
    // Selecciona una tarjeta de crédito y cierra el modal
    selectCard(card) {
        this.trigger('close-popup', { card });
    }
}

CreditCardModal.template = "CreditCardModal";
Registries.Component.add(CreditCardModal);
export default CreditCardModal;
