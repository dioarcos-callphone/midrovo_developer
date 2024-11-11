odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const { useState } = require("react"); // Usamos React para manejar el estado del modal

    // Componente del Modal para mostrar las tarjetas
    const CreditCardModal = (props) => {
        const { isVisible, closeModal } = props;
        return isVisible ? (
            <div className="credit-card-modal">
                <div className="modal-content">
                    <h3>Selecciona una tarjeta de crédito</h3>
                    {/* Aquí puedes poner la lista de tarjetas de crédito */}
                    <ul>
                        <li>Tarjeta Visa</li>
                        <li>Tarjeta MasterCard</li>
                        <li>Tarjeta American Express</li>
                    </ul>
                    <button onClick={closeModal}>Cerrar</button>
                </div>
            </div>
        ) : null;
    };

    // Heredamos la clase PaymentScreen
    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            // Extiende la función setup si quieres añadir lógica adicional
            setup() {
                super.setup();  // Llamar al método padre
                this.state = useState({ isModalVisible: false });
            }

             // Método para abrir el modal
             openModal() {
                this.state.isModalVisible = true;
            }

            // Método para cerrar el modal
            closeModal() {
                this.state.isModalVisible = false;
            }

            // Sobrescribimos el método addNewPaymentLine
            async addNewPaymentLine({ detail: paymentMethod }) {
                const method_name = paymentMethod.name
                const result_rpc = await this.rpc({
                    model: "pos.payment.method",
                    method: "is_card",
                    args: [ method_name ]
                })

                if(result_rpc) {
                    this.openModal();
                }

                // Retornamos el método original de PaymentScreen utilizando super
                return super.addNewPaymentLine({ detail: paymentMethod });
            }

        };

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);

})
