public class PurchaseItem {
    private int quantity;
    private Merchandise merchandise;

    public PurchaseItem(Merchandise merchandise, int quantity) {
        this.merchandise = merchandise;
        this.quantity = quantity;
    }

    public double calculateSubTotal() {
        return merchandise.getPriceForQuantity(quantity);
    }

    public double calculateWeight() {
        return merchandise.getWeight() * quantity;
    }

    @Override
    public String toString() {
        return merchandise.getTitle() + " x" + quantity + " (Subtotal: ¥" + calculateSubTotal() + ")";
    }
}