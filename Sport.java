// Define a class named Car
public class Car {
    // Fields (state of the car)
    String brand;
    String color;
    int speed;

    // Constructor (used to initialize objects)
    public Car(String brand, String color, int speed) {
        this.brand = brand;
        this.color = color;
        this.speed = speed;
    }

    // Method (behavior of the car)
    public void drive() {
        System.out.println(brand + " is driving at " + speed + " km/h.");
    }

    public void stop() {
        System.out.println(brand + " has stopped.");
    }
}
