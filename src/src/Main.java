public class Main {
    public static void main(String[] args) {
        System.out.println("Initializing Shopping System Test...\n");

        // 1. Create a Client
        Client client1 = new Client("Yang Zheng", "13800138000", "Computer Science Dept, Room j1306", true);

        // 2. Create some Merchandise
        Merchandise book1 = new Merchandise("Software Engineering", 0.5, "UML Modeling Textbook", 59.9);
        Merchandise laptop = new Merchandise("ThinkPad T14", 1.5, "Developer Laptop", 6500.0);

        // 3. Create a Purchase (Order) for the Client
        Purchase order1 = new Purchase(client1);

        // 4. Create PurchaseItems (Order Details) and add to Purchase
        PurchaseItem item1 = new PurchaseItem(book1, 2); // 2 books
        PurchaseItem item2 = new PurchaseItem(laptop, 1); // 1 laptop
        
        order1.addItem(item1);
        order1.addItem(item2);

        // 5. Calculate total to pay
        double totalToPay = order1.calculateTotalOrderPrice();

        // 6. Process Payment (Transaction) - using AliPay as an example
        Transaction payment = new AliPay(totalToPay, "alipay_user_999");
        
        // Alternative payment examples:
        // Transaction payment = new CreditCard(totalToPay, "4392123456789012", "Visa", "12/28");
        // Transaction payment = new CashPayment(totalToPay, 7000.0);

        order1.setTransaction(payment);

        // 7. Print verification
        order1.printOrderSummary();
    }
}