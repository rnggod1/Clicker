# utils.py - Вспомогательные функции для сохранения

import json
import os

def save_game(data, filename='save.json'):
    """Сохранение игры в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False

def load_game(filename='save.json'):
    """Загрузка игры из файла"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print("Файл сохранения не найден")
            return None
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return None

def delete_save(filename='save.json'):
    """Удалить сохранение"""
    try:
        if os.path.exists(filename):
            os.remove(filename)
            return True
    except Exception as e:
        print(f"Ошибка удаления: {e}")
        return False
