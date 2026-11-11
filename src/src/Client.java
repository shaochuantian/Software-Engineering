public class Client {
    private String name;
    private String contact;
    private String deliveryAddress;
    private boolean active;

    public Client(String name, String contact, String deliveryAddress, boolean active) {
        this.name = name;
        this.contact = contact;
        this.deliveryAddress = deliveryAddress;
        this.active = active;
    }

    public String getName() { return name; }
    public void setActive(boolean active) { this.active = active; }
    
    @Override
    public String toString() {
        return "Client{name='" + name + "', contact='" + contact + "'}";
    }
}