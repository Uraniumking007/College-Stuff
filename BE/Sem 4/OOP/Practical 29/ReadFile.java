import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class ReadFile {
    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Please provide a text file as command line argument");
            System.exit(1);
        }

        try {
            File file = new File(args[0]);
            Scanner scanner = new Scanner(file);

            TreeSet<String> uniqueWords = new TreeSet<>(Collections.reverseOrder());

            while (scanner.hasNext()) {
                String word = scanner.next().toLowerCase().trim();
                word = word.replaceAll("[^a-zA-Z]", "");
                if (!word.isEmpty()) {
                    uniqueWords.add(word);
                }
            }

            System.out.println("Non-duplicate words in descending order:");
            for (String word : uniqueWords) {
                System.out.println(word);
            }

            scanner.close();

        } catch (FileNotFoundException e) {
            System.out.println("Error: File not found - " + args[0]);
        }
    }
}
