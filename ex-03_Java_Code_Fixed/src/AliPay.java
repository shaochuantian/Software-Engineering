public class AliPay extends Transaction {
    private String number;

    public AliPay(double amount, String number) {
        super(amount);
        this.number = number;
    }

    @Override
    public String getPaymentDetails() {
        return "AliPay [Account: " + number + "]";
    }
}