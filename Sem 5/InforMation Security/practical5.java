import java.io.*;
import java.util.*;

public class practical5 {
    public static String selectedKey;
    public static char sortedKey[];
    public static int sortedKeyPos[];

    public practical5() {
        selectedKey = "megabuck";
        sortedKeyPos = new int[selectedKey.length()];
        sortedKey = selectedKey.toCharArray();
    }

    public practical5(String JOD) {
        selectedKey = JOD;
        sortedKeyPos = new int[selectedKey.length()];
        sortedKey = selectedKey.toCharArray();
    }

    public static void doProcessOnKey() {
        int min, i, j;
        char orginalKey[] = selectedKey.toCharArray();
        char temp;
        for (i = 0; i < selectedKey.length(); i++) {
            min = i;
            for (j = i; j < selectedKey.length(); j++) {
                if (sortedKey[min] > sortedKey[j]) {
                    min = j;
                }
            }
            if (min != i) {
                temp = sortedKey[i];
                sortedKey[i] = sortedKey[min];
                sortedKey[min] = temp;
            }
        }
        for (i = 0; i < selectedKey.length(); i++) {
            for (j = 0; j < selectedKey.length(); j++) {
                if (orginalKey[i] == sortedKey[j])
                    sortedKeyPos[i] = j;
            }
        }
    }

    public static String doEncryption(String plainText) {
        int min, i, j;
        char orginalKey[] = selectedKey.toCharArray();
        char temp;
        doProcessOnKey();
        int row = plainText.length() / selectedKey.length();
        int extrabit = plainText.length() % selectedKey.length();
        int exrow = (extrabit == 0) ? 0 : 1;
        int rowtemp = -1, coltemp = -1;
        int totallen = (row + exrow) * selectedKey.length();
        char pmat[][] = new char[(row + exrow)][(selectedKey.length())];
        char encry[] = new char[totallen];
        int tempcnt = -1;
        row = 0;
        for (i = 0; i < totallen; i++) {
            coltemp++;
            if (i < plainText.length()) {
                if (coltemp == (selectedKey.length())) {
                    row++;
                    coltemp = 0;
                }
                pmat[row][coltemp] = plainText.charAt(i);
            } else {
                pmat[row][coltemp] = '-';
            }
        }
        int len = -1, k;
        for (i = 0; i < selectedKey.length(); i++) {
            for (k = 0; k < selectedKey.length(); k++) {
                if (i == sortedKeyPos[k]) {
                    break;
                }
            }
            for (j = 0; j <= row; j++) {
                len++;
                encry[len] = pmat[j][k];
            }
        }
        String p1 = new String(encry);
        return (new String(p1));
    }

    public static String doDecryption(String s) {
        int min, i, j, k;
        char key[] = selectedKey.toCharArray();
        char encry[] = s.toCharArray();
        char temp;
        doProcessOnKey();
        int row = s.length();
        selectedKey.length();
        char pmat[][] = new char[row][(selectedKey.length())];
        int tempcnt = -1;
        for (i = 0; i < selectedKey.length(); i++) {
            for (k = 0; k < selectedKey.length(); k++) {
                if (i == sortedKeyPos[k]) {
                    break;
                }
            }
            for (j = 0; j < row; j++) {
                tempcnt++;
                pmat[j][k] = encry[tempcnt];
            }
        }
        char p1[] = new char[row * selectedKey.length()];
        k = 0;
        for (i = 0; i < row; i++) {
            for (j = 0; j < selectedKey.length(); j++) {
                if (pmat[i][j] != '*') {
                    p1[k++] = pmat[i][j];
                }
            }
        }
        p1[k++] = '\0';
        return (new String(p1));
    }


    public static void main(String[] args) {
        practical5 tc = new practical5();
        String s = "";
        System.out.println("Enter Plain Text");
        Scanner sc = new Scanner(System.in);
        s = sc.nextLine();
        System.out.println("Cipher Text" + tc.doEncryption(s));
    }
}
