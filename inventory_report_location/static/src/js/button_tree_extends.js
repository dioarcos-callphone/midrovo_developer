/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
export class SaleListController extends ListController {
    setup() {
       super.setup();
    }
    
    async actionPDF() {
        const result = await this._rpc({
            model: 'product.product',
            method: 'action_pdf',
        });

        if (result) {
            const blob = new Blob([result], { type: 'application/pdf' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'Informe_Inventario.pdf';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    }
}

registry.category("views").add("button_in_tree", {
    ...listView,
    Controller: SaleListController,
    buttonTemplate: "button_sale.ListView.Buttons",
});