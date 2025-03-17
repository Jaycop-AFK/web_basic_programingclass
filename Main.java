public class Main {
    public static void main(String[] args) {
        // Create an object of the Car class
        Car myCar = new Car("Toyota", "Red", 120);

        // Access fields and methods
        System.out.println("Brand: " + myCar.brand); // Accessing field
        myCar.drive(); // Calling a method
        myCar.stop();
    }
}
