public class CashPayment extends Transaction {
    private double cashTendered;

    public CashPayment(double amount, double cashTendered) {
        super(amount);
        this.cashTendered = cashTendered;
    }

    @Override
    public String getPaymentDetails() {
        return "CashPayment [Tendered: ¥" + cashTendered + ", Change: ¥" + (cashTendered - amount) + "]";
    }
}