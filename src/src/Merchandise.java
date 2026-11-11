public class Merchandise {
    private String title;
    private double weight;
    private String description;
    private double unitPrice;

    public Merchandise(String title, double weight, String description, double unitPrice) {
        this.title = title;
        this.weight = weight;
        this.description = description;
        this.unitPrice = unitPrice;
    }

    public double getPriceForQuantity(int qty) {
        return this.unitPrice * qty;
    }

    public double getWeight() {
        return this.weight;
    }

    public String getTitle() {
        return title;
    }
}