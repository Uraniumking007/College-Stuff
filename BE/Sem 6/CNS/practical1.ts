import { stdin as input, stdout as output } from "process"
import * as readLine from "readline/promises"

interface EncrpytParameters {
    plainText: string
    key: number
}

interface DecryptParameters {
    encrpytedText: string
    key: number
}

interface FunctionsParameters {
    input: number
    type: "E" | "D"
}

function encryptForSmallLetters({ input, type }: FunctionsParameters) {
    if (input > 122) {
        input = input - 26
    }

    return input

}

function caesarEncrypt({ plainText, key }: EncrpytParameters) {
    const inputArr = plainText.split("")
    inputArr.forEach((element, index) => {
        let code = element.charCodeAt(0) + key
        inputArr[index] = String.fromCharCode(encryptForSmallLetters({ input: code, type: "E" }))
    });
    return inputArr.join("")
}

function caesarDecrypt({ encrpytedText, key }: DecryptParameters) {
    const inputArr = encrpytedText.split("")
    inputArr.forEach((element, index) => {
        let code = element.charCodeAt(0) - key
        console.log(code);

        if (code < 97) {
            code = code + 26
        }
        inputArr[index] = String.fromCharCode(code)
    });
    return inputArr.join("")
}

const encrpytedString = caesarEncrypt({ plainText: "tasty", key: 5 })
console.log(encrpytedString);
const decryptedText = caesarDecrypt({ encrpytedText: encrpytedString, key: 5 })
console.log(decryptedText);
