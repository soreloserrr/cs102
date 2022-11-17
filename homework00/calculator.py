import math
import typing as tp


def check_number(num):
    try:
        num = float(num)
        return num
    except ValueError:
        print("Введен некорректный символ")
        return "wrong"


def check_int(number: float) -> tp.Union[None, int]:
    if int(number) == number:
        return int(number)
    return None


def math_degree(num1: float, num2: float) -> tp.Union[str, float]:
    numbers = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    num1, num2 = int(num1), int(num2)
    while num1 > 0:
        res = numbers[num1 % num2] + res
        num1 = num1 // num2
    return res if res != "" else 0


def match_case_calc2(num1: float, num2: float, command: str) -> tp.Union[float, str]:
    match command:
        case "+":
            return num1 + num2
        case "degree":
            return math_degree(num1, num2)
        case "-":
            return num1 - num2
        case "/":
            if num2 == 0:
                return "На ноль делить нельзя!"
            return num1 / num2
        case "//":
            if num2 == 0:
                return "На ноль делить нельзя!"
            return num1 // num2
        case "%":
            if num2 == 0:
                return "На ноль делить нельзя!"
            return num1 % num2
        case "*":
            return num1 * num2
        case "**":
            return num1**num2
        case _:
            return f"Неизвестный оператор: {command!r}."


def match_case_calc1(num1: float, command: str) -> tp.Union[float, str]:
    match command:
        case "cos":
            return math.cos(num1)
        case "sin":
            return math.sin(num1)
        case "tan":
            return math.tan(num1)
        case "log10":
            if num1 <= 0:
                return "Число должно быть больше нуля!"
            return math.log10(num1)
        case "ln":
            if num1 <= 0:
                return "Число должно быть больше нуля!"
            return math.log(num1)
        case _:
            return f"Неизвестный оператор: {command!r}."


if __name__ == "__main__":
    while True:
        COMMAND = input("Введите оперцию: ")
        if COMMAND.isdigit() and int(COMMAND) == 0:
            break
        if COMMAND == "sin" or COMMAND == "cos" or COMMAND == "tan" or COMMAND == "log10" or COMMAND == "ln":
            NUM_1 = input("Введите число: ")
            while check_number(NUM_1) == "wrong":
                NUM_1 = input("Введите число: ")
            print(match_case_calc1(check_number(NUM_1), COMMAND))
        else:
            NUM_1 = input("Введите число: ")
            while check_number(NUM_1) == "wrong":
                NUM_1 = input("Введите число: ")
            NUM_2 = input("Введите еще одно число: ")
            while check_number(NUM_2) == "wrong":
                NUM_2 = input("Введите число: ")
            print(match_case_calc2(check_number(NUM_1), check_number(NUM_2), COMMAND))
