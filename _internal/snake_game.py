#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Malvage OS - Змейка (упрощенная кроссплатформенная версия)

import os
import random
import time
import sys
from colorama import init, Fore, Back, Style

init()

class SnakeGame:
    def __init__(self):
        self.width = 20
        self.height = 10
        self.snake = [[5, 10], [5, 9], [5, 8]]
        self.food = self.generate_food()
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'
        self.score = 0
        self.game_over = False
        self.speed = 0.2
        
    def generate_food(self):
        while True:
            food = [random.randint(0, self.height-1), 
                   random.randint(0, self.width-1)]
            if food not in self.snake:
                return food
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw(self):
        self.clear_screen()
        
        print(f"{Fore.YELLOW}=== Змейка === (Счет: {self.score})")
        print(f"{Fore.CYAN}Управление: WASD или стрелки, Q - выход{Style.RESET_ALL}")
        print()
        
        for y in range(self.height):
            line = []
            for x in range(self.width):
                if [y, x] == self.snake[0]:
                    line.append(f"{Fore.GREEN}O{Style.RESET_ALL}")  # Голова
                elif [y, x] in self.snake[1:]:
                    line.append(f"{Fore.GREEN}o{Style.RESET_ALL}")  # Тело
                elif [y, x] == self.food:
                    line.append(f"{Fore.RED}@{Style.RESET_ALL}")    # Еда
                else:
                    line.append(".")
            print(" ".join(line))
    
    def get_input(self):
        try:
            if os.name == 'nt':  # Windows
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode()
                    if key.lower() == 'q':
                        return 'QUIT'
                    elif key == '\xe0':  # Специальные клавиши
                        key = msvcrt.getch().decode()
                        if key == 'H': return 'UP'
                        elif key == 'P': return 'DOWN'
                        elif key == 'K': return 'LEFT'
                        elif key == 'M': return 'RIGHT'
                    else:
                        if key.lower() == 'w': return 'UP'
                        elif key.lower() == 's': return 'DOWN'
                        elif key.lower() == 'a': return 'LEFT'
                        elif key.lower() == 'd': return 'RIGHT'
            else:  # Linux/MacOS
                import tty, termios, sys
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    key = sys.stdin.read(1)
                    if key.lower() == 'q':
                        return 'QUIT'
                    elif key == '\x1b':  # Escape sequence
                        if sys.stdin.read(1) == '[':
                            key = sys.stdin.read(1)
                            if key == 'A': return 'UP'
                            elif key == 'B': return 'DOWN'
                            elif key == 'C': return 'RIGHT'
                            elif key == 'D': return 'LEFT'
                    else:
                        if key.lower() == 'w': return 'UP'
                        elif key.lower() == 's': return 'DOWN'
                        elif key.lower() == 'a': return 'LEFT'
                        elif key.lower() == 'd': return 'RIGHT'
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except:
            pass
        return None
    
    def update(self):
        # Обновляем направление
        key = self.get_input()
        if key == 'QUIT':
            self.game_over = True
            return
        elif key in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            # Запрещаем разворот на 180 градусов
            if (key == 'UP' and self.direction != 'DOWN') or \
               (key == 'DOWN' and self.direction != 'UP') or \
               (key == 'LEFT' and self.direction != 'RIGHT') or \
               (key == 'RIGHT' and self.direction != 'LEFT'):
                self.next_direction = key
        
        # Двигаем змейку
        head = self.snake[0].copy()
        
        self.direction = self.next_direction
        
        if self.direction == 'UP':
            head[0] -= 1
        elif self.direction == 'DOWN':
            head[0] += 1
        elif self.direction == 'LEFT':
            head[1] -= 1
        elif self.direction == 'RIGHT':
            head[1] += 1
        
        # Проверяем столкновения
        if (head[0] < 0 or head[0] >= self.height or
            head[1] < 0 or head[1] >= self.width or
            head in self.snake):
            self.game_over = True
            return
        
        self.snake.insert(0, head)
        
        # Проверяем, съели ли еду
        if head == self.food:
            self.score += 1
            self.food = self.generate_food()
            # Увеличиваем скорость каждые 3 очка
            if self.score % 3 == 0 and self.speed > 0.05:
                self.speed *= 0.9
        else:
            self.snake.pop()
    
    def run(self):
        try:
            while not self.game_over:
                self.draw()
                self.update()
                time.sleep(self.speed)
            
            self.clear_screen()
            print(f"{Fore.RED}Игра окончена!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Ваш счет: {self.score}{Style.RESET_ALL}")
            time.sleep(2)
        except KeyboardInterrupt:
            self.clear_screen()
            print(f"{Fore.YELLOW}Игра прервана.{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        game = SnakeGame()
        game.run()
    except Exception as e:
        print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
        sys.exit(1)