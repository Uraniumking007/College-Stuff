// Pratical 13-A
interface PrintData {
    void printInt();

    void printFloat();

    void printChar();
}

class PrintInt {
    void printInt() {
        System.out.println("int");
    }
}

class PrintFloat {
    void printFloat() {
        System.out.println("Float");
    }
}

class PrintChar {
    void printChar() {
        System.out.println("char");
    }
}

class Main {
    public static void main(String[] args) {
        PrintInt pi = new PrintInt();
        PrintFloat pf = new PrintFloat();
        PrintChar pc = new PrintChar();
        pi.printInt();
        pf.printFloat();
        pc.printChar();
    }
}

// Practical 13-B

class p13b {
    interface animal {
        void food();
    }

    class Dog {
        public void food() {
            System.out.println("Dog eats food");
        }
    }

    class Lion {
        public void food() {
            System.out.println("Lion eats food");
        }
    }
}
