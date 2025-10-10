import java.util.*;

class Address{
    String city;
    int pincode;
    void displayAdd(){
        System.out.println("City: "+ city);
        System.out.println("Pincode: "+ pincode);
    }
}
class Biodata extends Address{
    String name;
    String quali;
    String dob;
    void displayBio(){
        System.out.println("Name: "+ name);
        System.out.println("Qualitifcation: "+ quali);
        System.out.println("Date of Birth: "+ dob);
        displayAdd();
    }
}
class P11a{
    public static void main(String[] args) {
        Biodata b = new Biodata();
        b.city = "Surat";
        b.pincode = 394210;
        b.name = "Tejash";
        b.quali = "Diploma C.E.";
        b.dob = "13";
        b.displayBio();
    }
}




class Vehicle{
    int id,speed;
}
class Bike extends Vehicle{
    void display(){
        System.out.println("Id: "+id);
        System.out.println("Speed: "+speed);
    }
    void insert(int i,int s){
        super.id = i;
        super.speed = s;
        display();
    }
}
class P11b{
    public static void main(String[] args) {
        Bike b= new Bike();
        b.insert(25,250);
    }
}