#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Malvage OS - Продвинутый калькулятор

import math
import sys
from colorama import init, Fore, Style

init(autoreset=True)

class AdvancedCalculator:
    def __init__(self):
        self.history = []
        self.show_welcome()

    def show_welcome(self):
        print(f"{Fore.CYAN}\n=== Malvage OS Calculator {Fore.YELLOW}v1.0{Fore.CYAN} ===")
        print(f"{Fore.GREEN}Доступные операции:")
        print(f"{Fore.YELLOW}+{Style.RESET_ALL} - сложение  {Fore.YELLOW}-{Style.RESET_ALL} - вычитание")
        print(f"{Fore.YELLOW}*{Style.RESET_ALL} - умножение {Fore.YELLOW}/{Style.RESET_ALL} - деление")
        print(f"{Fore.YELLOW}^ {Style.RESET_ALL}- степень    {Fore.YELLOW}% {Style.RESET_ALL}- остаток")
        print(f"{Fore.YELLOW}sqrt{Style.RESET_ALL} - корень  {Fore.YELLOW}sin/cos/tan{Style.RESET_ALL} - тригонометрия")
        print(f"{Fore.YELLOW}log{Style.RESET_ALL} - логарифм {Fore.YELLOW}pi{Style.RESET_ALL} - число π")
        print(f"{Fore.YELLOW}hist{Style.RESET_ALL} - история {Fore.YELLOW}exit{Style.RESET_ALL} - выход\n")

    def run(self):
        while True:
            try:
                expr = input(f"{Fore.BLUE}calc>{Style.RESET_ALL} ").strip().lower()
                
                if expr == "exit":
                    break
                elif expr == "hist":
                    self.show_history()
                    continue
                elif expr == "help":
                    self.show_welcome()
                    continue
                elif not expr:
                    continue
                
                result = self.evaluate_expression(expr)
                if result is not None:
                    self.history.append(f"{expr} = {result}")
                    print(f"{Fore.GREEN}Результат: {Fore.YELLOW}{result}{Style.RESET_ALL}")
                    
            except (KeyboardInterrupt, EOFError):
                print(f"\n{Fore.RED}Завершение работы калькулятора...{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")

    def evaluate_expression(self, expr):
        try:
            # Заменяем специальные константы и функции
            expr = expr.replace("pi", str(math.pi))
            expr = expr.replace("^", "**")
            
            # Обрабатываем специальные функции
            if "sqrt(" in expr:
                expr = expr.replace("sqrt(", "math.sqrt(")
            if "sin(" in expr:
                expr = expr.replace("sin(", "math.sin(")
            if "cos(" in expr:
                expr = expr.replace("cos(", "math.cos(")
            if "tan(" in expr:
                expr = expr.replace("tan(", "math.tan(")
            if "log(" in expr:
                expr = expr.replace("log(", "math.log10(")
            if "ln(" in expr:
                expr = expr.replace("ln(", "math.log(")
                
            # Вычисляем выражение
            result = eval(expr, {"__builtins__": None}, {"math": math})
            return round(result, 10) if isinstance(result, float) else result
            
        except Exception as e:
            raise ValueError(f"Некорректное выражение: {expr}")

    def show_history(self):
        if not self.history:
            print(f"{Fore.YELLOW}История пуста{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}=== История вычислений ==={Style.RESET_ALL}")
        for i, item in enumerate(self.history[-10:], 1):
            print(f"{Fore.YELLOW}{i}. {item}{Style.RESET_ALL}")
        print()

if __name__ == "__main__":
    try:
        calc = AdvancedCalculator()
        calc.run()
    except Exception as e:
        print(f"{Fore.RED}Критическая ошибка: {e}{Style.RESET_ALL}")
        sys.exit(1)