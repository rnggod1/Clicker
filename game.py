# game.py - Основная логика игры

import tkinter as tk
from tkinter import messagebox
from zones import Zone
from buildings import get_buildings
from utils import save_game, load_game  # ← ПРОВЕРЬТЕ ЭТУ СТРОКУ

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏗️ Строительный кликер")
        self.root.geometry("1100x900+50+30")
        self.root.configure(bg='#1a1a2e')
        
        self.resources = {
            '🌾 Пшеница': 10,
            '🪵 Древесина': 0,
            '⛏️ Руда': 0,
            '💰 Золото': 0
        }
        
        self.buildings_data = get_buildings()
        self.zones = [Zone(i) for i in range(9)]
        self.building_counts = {}
        
        self.running = True
        
        from ui import GameUI
        self.ui = GameUI(self.root, self)
        
        self.update_ui()
    
    def get_building_count(self, name):
        return self.building_counts.get(name, 0)
    
    def build_zone(self, zone, building_name):
        if zone.has_building():
            self.ui.show_message("❌ На этой зоне уже есть здание!")
            return
        
        if building_name not in self.buildings_data:
            self.ui.show_message("❌ Здание не найдено!")
            return
        
        building = self.buildings_data[building_name]
        count = self.get_building_count(building_name)
        price = building.get_price(count)
        
        if not building.can_unlock(self.resources) and count == 0:
            unlock_text = []
            for res, amount in building.unlock_cost.items():
                if amount > 0:
                    unlock_text.append(f"{res}: {amount}")
            self.ui.show_message(f"🔒 Здание закрыто! Нужно: {', '.join(unlock_text)}")
            return
        
        if building.name != 'Ферма' or count > 0:
            if self.resources.get('🌾 Пшеница', 0) < price:
                self.ui.show_message(f"❌ Нужно 🌾 {price} пшеницы!")
                return
        
        if building.name != 'Ферма' or count > 0:
            self.resources['🌾 Пшеница'] -= price
        
        zone.building = building
        zone.resource = 0
        zone.level = 1
        zone.click_upgrade_level = 0
        zone.auto_upgrade_level = 0
        zone.click_upgrade_cost = 50
        zone.auto_upgrade_cost = 100
        self.building_counts[building_name] = count + 1
        
        self.ui.show_message(f"✅ Построена {building.emoji} {building.name}!")
    
    def upgrade_zone_click(self, zone):
        if not zone.has_building():
            self.ui.show_message("❌ На этой зоне нет здания!")
            return
        
        cost = int(zone.click_upgrade_cost * (1.5 ** zone.click_upgrade_level))
        
        if self.resources.get('🌾 Пшеница', 0) < cost:
            self.ui.show_message(f"❌ Нужно 🌾 {cost} пшеницы для +1 клика на этой зоне!")
            return
        
        self.resources['🌾 Пшеница'] -= cost
        zone.click_upgrade_level += 1
        zone.building.click_power += 1
        
        self.ui.show_message(f"🖱️ Сила клика на зоне {zone.index+1} улучшена! +1 (всего +{zone.click_upgrade_level})")
    
    def upgrade_zone_auto(self, zone):
        if not zone.has_building():
            self.ui.show_message("❌ На этой зоне нет здания!")
            return
        
        cost = int(zone.auto_upgrade_cost * (1.5 ** zone.auto_upgrade_level))
        
        if self.resources.get('🌾 Пшеница', 0) < cost:
            self.ui.show_message(f"❌ Нужно 🌾 {cost} пшеницы для +1 авто на этой зоне!")
            return
        
        self.resources['🌾 Пшеница'] -= cost
        zone.auto_upgrade_level += 1
        zone.building.autoproduction += 1
        
        self.ui.show_message(f"⚡ Автопроизводство на зоне {zone.index+1} улучшено! +1/сек (всего +{zone.auto_upgrade_level}/сек)")
    
    def demolish_zone(self, zone):
        if not zone.has_building():
            self.ui.show_message("❌ На этой зоне нет здания!")
            return
        
        if messagebox.askyesno("Снос", f"Снести {zone.building.emoji} {zone.building.name}?"):
            name = zone.building.name
            self.building_counts[name] = max(0, self.building_counts.get(name, 1) - 1)
            zone.building = None
            zone.resource = 0
            zone.level = 0
            
            self.ui.show_message(f"💥 {name} снесена!")
    
    def on_click(self, zone, event=None):
        if zone.has_building():
            gained = zone.building.click_power
            zone.resource += gained
            self.resources[zone.building.resource] += gained
            
            self.ui.show_message(f"{zone.building.emoji} +{gained} {zone.building.resource}!")
    
    def save_game(self):
        """Сохранение игры"""
        try:
            data = {
                'resources': self.resources,
                'zones': [{
                    'index': z.index,
                    'building': z.building.name if z.building else None,
                    'resource': z.resource,
                    'level': getattr(z, 'level', 0),
                    'click_upgrade_level': getattr(z, 'click_upgrade_level', 0),
                    'auto_upgrade_level': getattr(z, 'auto_upgrade_level', 0)
                } for z in self.zones],
                'building_counts': self.building_counts
            }
            
            if save_game(data):
                self.ui.show_message("💾 Игра сохранена!")
            else:
                self.ui.show_message("❌ Ошибка сохранения!")
        except Exception as e:
            self.ui.show_message(f"❌ Ошибка: {e}")
            print(f"Ошибка сохранения: {e}")
    
    def load_game(self):
        """Загрузка игры"""
        try:
            data = load_game()
            if data:
                self.resources = data['resources']
                self.building_counts = data['building_counts']
                
                for i, zone_data in enumerate(data['zones']):
                    zone = self.zones[i]
                    zone.resource = zone_data['resource']
                    if zone_data['building']:
                        for name, building in self.buildings_data.items():
                            if building.name == zone_data['building']:
                                zone.building = building
                                zone.level = zone_data.get('level', 1)
                                zone.click_upgrade_level = zone_data.get('click_upgrade_level', 0)
                                zone.auto_upgrade_level = zone_data.get('auto_upgrade_level', 0)
                                zone.click_upgrade_cost = 50
                                zone.auto_upgrade_cost = 100
                                break
                    else:
                        zone.building = None
                        zone.level = 0
                
                self.ui.show_message("📂 Игра загружена!")
            else:
                self.ui.show_message("❌ Файл сохранения не найден!")
        except Exception as e:
            self.ui.show_message(f"❌ Ошибка: {e}")
            print(f"Ошибка загрузки: {e}")
    
    def update_ui(self):
        if not self.running:
            return
        
        try:
            for zone in self.zones:
                if zone.has_building() and zone.building.autoproduction > 0:
                    zone.resource += zone.building.autoproduction
                    self.resources[zone.building.resource] += zone.building.autoproduction
            
            self.ui.update_ui()
            self.root.after(100, self.update_ui)
        except Exception as e:
            print(f"Ошибка обновления: {e}")
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    
    def on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    game = Game()
    game.run()
