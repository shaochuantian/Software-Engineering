public class CreditCard extends Transaction {
    private String number;
    private String type;
    private String expireDate;

    public CreditCard(double amount, String number, String type, String expireDate) {
        super(amount);
        this.number = number;
        this.type = type;
        this.expireDate = expireDate;
    }

    @Override
    public String getPaymentDetails() {
        return "CreditCard [" + type + "] ending in " + number.substring(Math.max(0, number.length() - 4));
    }
}