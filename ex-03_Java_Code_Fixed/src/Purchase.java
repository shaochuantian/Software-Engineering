import java.util.Date;
import java.util.List;
import java.util.ArrayList;

public class Purchase {
    private Date createDate;
    private OrderStatus status;
    
    // Associations
    private Client client;
    private List<PurchaseItem> items;
    private Transaction transaction;

    public Purchase(Client client) {
        this.client = client;
        this.createDate = new Date();
        this.status = OrderStatus.CREATE;
        this.items = new ArrayList<>();
    }

    public void addItem(PurchaseItem item) {
        this.items.add(item);
    }

    public void setTransaction(Transaction transaction) {
        this.transaction = transaction;
        this.status = OrderStatus.PAID; // Update status upon payment
    }

    public double calculateTotalOrderPrice() {
        double total = 0;
        for (PurchaseItem item : items) {
            total += item.calculateSubTotal();
        }
        return total;
    }

    public void printOrderSummary() {
        System.out.println("====== ORDER SUMMARY ======");
        System.out.println("Client: " + client.getName());
        System.out.println("Date: " + createDate);
        System.out.println("Status: " + status);
        System.out.println("Items:");
        for (PurchaseItem item : items) {
            System.out.println("  - " + item.toString());
        }
        System.out.println("Total Amount: ¥" + calculateTotalOrderPrice());
        if (transaction != null) {
            System.out.println("Payment: " + transaction.getPaymentDetails());
        }
        System.out.println("===========================");
    }
}