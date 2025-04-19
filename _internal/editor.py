#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Malvage OS - Текстовый редактор

import os
import sys
from colorama import init, Fore, Style

init(autoreset=True)

class TextEditor:
    SYNTAX_HIGHLIGHT = {
        'vbs': {
            'keywords': ['dim', 'set', 'function', 'sub', 'end', 'if', 'then', 'else', 'for', 'next', 'while', 'wend'],
            'comments': "'",
            'strings': ['"', "'"],
            'color': Fore.YELLOW
        },
        'bat': {
            'keywords': ['@echo', 'set', 'if', 'else', 'for', 'in', 'do', 'goto', 'call', 'start'],
            'comments': '::',
            'strings': ['"', "'"],
            'color': Fore.GREEN
        },
        'cmd': {
            'keywords': ['echo', 'set', 'if', 'else', 'for', 'in', 'do', 'goto', 'call'],
            'comments': '::',
            'strings': ['"', "'"],
            'color': Fore.CYAN
        }
    }

    def __init__(self):
        self.file_path = None
        self.content = []
        self.modified = False
        self.show_help()

    def show_help(self):
        print(f"\n{Fore.CYAN}=== Malvage OS Text Editor ===")
        print(f"{Fore.GREEN}Команды:")
        print(f"{Fore.YELLOW}open <file>{Style.RESET_ALL} - Открыть файл")
        print(f"{Fore.YELLOW}save [file]{Style.RESET_ALL} - Сохранить файл")
        print(f"{Fore.YELLOW}edit{Style.RESET_ALL} - Редактировать содержимое")
        print(f"{Fore.YELLOW}view{Style.RESET_ALL} - Просмотреть содержимое")
        print(f"{Fore.YELLOW}help{Style.RESET_ALL} - Показать справку")
        print(f"{Fore.YELLOW}exit{Style.RESET_ALL} - Выход\n")

    def run(self):
        while True:
            try:
                cmd = input(f"{Fore.BLUE}editor>{Style.RESET_ALL} ").strip().lower()
                if not cmd:
                    continue

                parts = cmd.split()
                action = parts[0]
                args = parts[1:]

                if action == "exit":
                    if self.check_unsaved_changes():
                        break
                elif action == "help":
                    self.show_help()
                elif action == "open" and args:
                    self.open_file(args[0])
                elif action == "save":
                    self.save_file(args[0] if args else None)
                elif action == "edit":
                    self.edit_content()
                elif action == "view":
                    self.view_content()
                else:
                    print(f"{Fore.RED}Неизвестная команда. Введите 'help' для справки.{Style.RESET_ALL}")

            except (KeyboardInterrupt, EOFError):
                if self.check_unsaved_changes():
                    print(f"{Fore.YELLOW}Выход из редактора...{Style.RESET_ALL}")
                    break
            except Exception as e:
                print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")

    def check_unsaved_changes(self):
        if self.modified:
            confirm = input(f"{Fore.YELLOW}Есть несохраненные изменения. Выйти без сохранения? (y/n): {Style.RESET_ALL}")
            return confirm.lower() == 'y'
        return True

    def open_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.content = f.readlines()
            self.file_path = file_path
            self.modified = False
            print(f"{Fore.GREEN}Файл '{file_path}' успешно открыт.{Style.RESET_ALL}")
            self.view_content()
        except Exception as e:
            print(f"{Fore.RED}Ошибка при открытии файла: {e}{Style.RESET_ALL}")

    def save_file(self, file_path=None):
        save_path = file_path or self.file_path
        if not save_path:
            print(f"{Fore.RED}Не указан путь для сохранения.{Style.RESET_ALL}")
            return

        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.writelines(self.content)
            self.file_path = save_path
            self.modified = False
            print(f"{Fore.GREEN}Файл успешно сохранен: {save_path}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Ошибка при сохранении файла: {e}{Style.RESET_ALL}")

    def edit_content(self):
        if not self.content:
            self.content = [""]

        print(f"{Fore.YELLOW}Редактирование (для завершения введите 'end' на новой строке):{Style.RESET_ALL}")
        new_content = []
        try:
            while True:
                line = input()
                if line.lower() == 'end':
                    break
                new_content.append(line + "\n")
        except (KeyboardInterrupt, EOFError):
            print(f"{Fore.YELLOW}Прервано пользователем.{Style.RESET_ALL}")

        if new_content:
            self.content = new_content
            self.modified = True

    def view_content(self):
        if not self.content:
            print(f"{Fore.YELLOW}Файл пуст.{Style.RESET_ALL}")
            return

        file_ext = os.path.splitext(self.file_path)[1][1:] if self.file_path else None
        syntax = self.SYNTAX_HIGHLIGHT.get(file_ext) if file_ext else None

        print(f"\n{Fore.CYAN}=== Содержимое файла ==={Style.RESET_ALL}")
        for i, line in enumerate(self.content, 1):
            line = line.rstrip('\n')
            if syntax:
                colored_line = self.highlight_syntax(line, syntax)
                print(f"{Fore.WHITE}{i:3d}| {colored_line}{Style.RESET_ALL}")
            else:
                print(f"{Fore.WHITE}{i:3d}| {line}{Style.RESET_ALL}")
        print()

    def highlight_syntax(self, line, syntax):
        # Подсветка комментариев
        if syntax['comments'] and line.lstrip().startswith(syntax['comments']):
            return f"{Fore.BLUE}{line}{Style.RESET_ALL}"

        # Подсветка строк
        for quote in syntax['strings']:
            if quote in line:
                parts = line.split(quote)
                for i in range(1, len(parts), 2):
                    parts[i] = f"{Fore.MAGENTA}{quote}{parts[i]}{quote}{Style.RESET_ALL}"
                line = ''.join(parts)

        # Подсветка ключевых слов
        for keyword in syntax['keywords']:
            line = line.replace(keyword, f"{syntax['color']}{keyword}{Style.RESET_ALL}")

        return line

if __name__ == "__main__":
    try:
        editor = TextEditor()
        editor.run()
    except Exception as e:
        print(f"{Fore.RED}Критическая ошибка: {e}{Style.RESET_ALL}")
        sys.exit(1)