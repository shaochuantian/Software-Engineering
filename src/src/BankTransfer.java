public class BankTransfer extends Transaction {
    private String bankID;
    private String bankName;

    public BankTransfer(double amount, String bankID, String bankName) {
        super(amount);
        this.bankID = bankID;
        this.bankName = bankName;
    }

    @Override
    public String getPaymentDetails() {
        return "BankTransfer [Bank: " + bankName + ", ID: " + bankID + "]";
    }
}