public class WeChatPay extends Transaction {
    private String number;

    public WeChatPay(double amount, String number) {
        super(amount);
        this.number = number;
    }

    @Override
    public String getPaymentDetails() {
        return "WeChatPay [Account: " + number + "]";
    }
}