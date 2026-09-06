# ui.py - Интерфейс игры (УПРОЩЁННЫЙ)

import tkinter as tk
from tkinter import ttk, messagebox
from buildings import get_buildings

class GameUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.buildings_data = get_buildings()
        self.zone_widgets = []
        
        self.create_widgets()
        
    def create_widgets(self):
        """Создание интерфейса"""
        self.create_resource_panel()
        self.create_build_panel()
        self.create_selected_info()
        self.create_zone_grid()
        
        self.info_label = tk.Label(self.root, text="🏗️ Нажмите 'Построить' на пустой зоне",
                                   font=('Arial', 10), fg='#81D4FA', bg='#1a1a2e')
        self.info_label.pack(pady=5)
        
        self.create_control_panel()
    
    def create_resource_panel(self):
        """Панель ресурсов"""
        self.resources_frame = tk.Frame(self.root, bg='#16213e', height=50)
        self.resources_frame.pack(fill='x', pady=5, padx=10)
        self.resources_frame.pack_propagate(False)
        
        self.resource_labels = {}
        for name, amount in self.game.resources.items():
            label = tk.Label(self.resources_frame,
                           text=f"{name}: {amount}",
                           font=('Arial', 11, 'bold'),
                           fg='#FFD700', bg='#16213e')
            label.pack(side='left', padx=12, pady=8)
            self.resource_labels[name] = label
    
    def create_build_panel(self):
        """Панель выбора здания"""
        self.build_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.build_frame.pack(fill='x', pady=5, padx=10)
        
        tk.Label(self.build_frame, text="🏗️ ВЫБЕРИТЕ ЗДАНИЕ:",
                font=('Arial', 10, 'bold'), fg='white', bg='#1a1a2e').pack(pady=2)
        
        buttons_container = tk.Frame(self.build_frame, bg='#1a1a2e')
        buttons_container.pack(fill='x', pady=2)
        
        self.build_buttons = {}
        buildings_list = list(self.buildings_data.items())
        
        rows = [buildings_list[i:i+4] for i in range(0, len(buildings_list), 4)]
        
        for row_buildings in rows:
            row_frame = tk.Frame(buttons_container, bg='#1a1a2e')
            row_frame.pack(pady=2)
            
            for name, building in row_buildings:
                btn_text = f"{building.emoji} {building.name}\n+{building.click_power} клик | +{building.autoproduction}/сек"
                
                btn = tk.Button(row_frame,
                              text=btn_text,
                              font=('Arial', 9),
                              bg='#37474F', fg='white',
                              width=20, height=2,
                              command=lambda n=name: self.select_building(n))
                btn.pack(side='left', padx=4, pady=2)
                self.build_buttons[name] = btn
        
        self.selected_building = None
    
    def create_selected_info(self):
        """Панель с информацией о выбранном здании"""
        self.selected_frame = tk.Frame(self.root, bg='#0D1B2A', height=100)
        self.selected_frame.pack(fill='x', pady=3, padx=10)
        self.selected_frame.pack_propagate(False)
        
        self.selected_label = tk.Label(self.selected_frame,
                                      text="⬅️ Выберите здание для постройки",
                                      font=('Arial', 10, 'bold'),
                                      fg='#81D4FA', bg='#0D1B2A',
                                      wraplength=950,
                                      justify='center')
        self.selected_label.pack(expand=True, fill='both', padx=10, pady=10)
    
    def select_building(self, name):
        """Выбор здания"""
        self.selected_building = name
        
        for btn_name, btn in self.build_buttons.items():
            if btn_name == name:
                btn.config(bg=self.buildings_data[name].color)
            else:
                btn.config(bg='#37474F')
        
        building = self.buildings_data[name]
        count = self.game.get_building_count(name)
        price = building.get_price(count)
        
        info_lines = []
        info_lines.append(f"{building.emoji} {building.name}")
        
        if building.name == 'Ферма' and count == 0:
            info_lines.append("💰 БЕСПЛАТНО!")
        else:
            info_lines.append(f"💰 Цена: {price} 🌾")
        
        info_lines.append(f"⚡ Клик: +{building.click_power} {building.resource}")
        info_lines.append(f"⚡ Авто: +{building.autoproduction}/сек {building.resource}")
        
        costs = []
        for res, amount in building.cost.items():
            if amount > 0:
                costs.append(f"{res}: {amount}")
        if costs:
            info_lines.append("📦 Требует: " + " | ".join(costs))
        
        if building.unlock_cost and any(building.unlock_cost.values()) and count == 0:
            unlocks = []
            for res, amount in building.unlock_cost.items():
                if amount > 0:
                    unlocks.append(f"{res}: {amount}")
            info_lines.append("🔓 Открыть: " + " | ".join(unlocks))
        
        can_afford = self.game.resources.get('🌾 Пшеница', 0) >= price if price > 0 else True
        if building.name == 'Ферма' and count == 0:
            can_afford = True
        
        for res, amount in building.cost.items():
            if amount > 0 and self.game.resources.get(res, 0) < amount:
                can_afford = False
                break
        
        color = building.color if can_afford else '#E53935'
        
        self.selected_label.config(
            text="".join(info_lines),
            fg=color,
            font=('Arial', 8, 'bold')
        )
        
        status = "✅ Доступно!" if can_afford else "❌ Не хватает ресурсов!"
        self.hint_label.config(
            text=f"{status} | Выбрано: {building.emoji} {building.name}",
            fg=color
        )
    
    def create_zone_grid(self):
        """Сетка зон"""
        self.zones_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.zones_frame.pack(expand=True, fill='both', padx=15, pady=5)
        
        for i, zone in enumerate(self.game.zones):
            row = i // 3
            col = i % 3
            
            frame = tk.Frame(self.zones_frame, bg='#16213e', relief='raised', bd=2)
            frame.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
            
            zone_label = tk.Label(frame,
                                text=f"ЗОНА {i+1}\n🟩 ПУСТО",
                                font=('Arial', 10, 'bold'),
                                fg='#81D4FA', bg='#16213e')
            zone_label.pack(pady=3)
            
            click_btn = tk.Button(frame,
                                text="🖱️ КЛИКНУТЬ\n(нет здания)",
                                font=('Arial', 9, 'bold'),
                                bg='#37474F', fg='white',
                                command=lambda z=zone: self.game.on_click(z),
                                height=2, width=14,
                                state='disabled')
            click_btn.pack(pady=3)
            
            actions_frame1 = tk.Frame(frame, bg='#16213e')
            actions_frame1.pack(fill='x', pady=1)
            
            build_btn = tk.Button(actions_frame1,
                                 text="🏗️\nПОСТРОИТЬ",
                                 font=('Arial', 7, 'bold'),
                                 bg='#FF6F00', fg='white',
                                 width=6, height=2,
                                 command=lambda z=zone: self.build_on_zone(z))
            build_btn.pack(side='left', padx=2, expand=True, fill='x')
            
            demolish_btn = tk.Button(actions_frame1,
                                    text="💥\nСНЕСТИ",
                                    font=('Arial', 7, 'bold'),
                                    bg='#E53935', fg='white',
                                    width=6, height=2,
                                    command=lambda z=zone: self.game.demolish_zone(z),
                                    state='disabled')
            demolish_btn.pack(side='left', padx=2, expand=True, fill='x')
            
            actions_frame2 = tk.Frame(frame, bg='#16213e')
            actions_frame2.pack(fill='x', pady=1)
            
            click_upgrade_btn = tk.Button(actions_frame2,
                                         text="🖱️\n+1 КЛИК\n(50🌾)",
                                         font=('Arial', 7, 'bold'),
                                         bg='#FF8F00', fg='white',
                                         width=6, height=3,
                                         command=lambda z=zone: self.game.upgrade_zone_click(z),
                                         state='disabled')
            click_upgrade_btn.pack(side='left', padx=2, expand=True, fill='x')
            
            auto_upgrade_btn = tk.Button(actions_frame2,
                                        text="⚡\n+1 АВТО\n(100🌾)",
                                        font=('Arial', 7, 'bold'),
                                        bg='#0D47A1', fg='white',
                                        width=6, height=3,
                                        command=lambda z=zone: self.game.upgrade_zone_auto(z),
                                        state='disabled')
            auto_upgrade_btn.pack(side='left', padx=2, expand=True, fill='x')
            
            self.zone_widgets.append({
                'frame': frame,
                'zone_label': zone_label,
                'click_btn': click_btn,
                'build_btn': build_btn,
                'demolish_btn': demolish_btn,
                'click_upgrade_btn': click_upgrade_btn,
                'auto_upgrade_btn': auto_upgrade_btn,
                'zone': zone
            })
        
        for i in range(3):
            self.zones_frame.grid_rowconfigure(i, weight=1)
            self.zones_frame.grid_columnconfigure(i, weight=1)
    
    def build_on_zone(self, zone):
        if not self.selected_building:
            self.show_message("❌ Сначала выберите здание!")
            return
        self.game.build_zone(zone, self.selected_building)
    
    def create_control_panel(self):
        control_frame = tk.Frame(self.root, bg='#1a1a2e')
        control_frame.pack(fill='x', pady=3)
        
        save_btn = tk.Button(control_frame,
                           text="💾 СОХРАНИТЬ",
                           font=('Arial', 9, 'bold'),
                           bg='#4CAF50', fg='white',
                           command=self.game.save_game)
        save_btn.pack(side='right', padx=5)
        
        load_btn = tk.Button(control_frame,
                           text="📂 ЗАГРУЗИТЬ",
                           font=('Arial', 9, 'bold'),
                           bg='#FF6F00', fg='white',
                           command=self.game.load_game)
        load_btn.pack(side='right', padx=5)
        
        self.hint_label = tk.Label(control_frame,
                                  text="",
                                  font=('Arial', 11, 'bold'),
                                  fg='#4CAF50', bg='#1a1a2e')
        self.hint_label.pack(side='left', padx=10)
    
    def show_message(self, message):
        self.info_label.config(text=message)
        self.root.after(3000, lambda: self.info_label.config(text=""))
    
    def update_ui(self):
        try:
            for name, label in self.resource_labels.items():
                label.config(text=f"{name}: {self.game.resources.get(name, 0)}")
            
            for name, btn in self.build_buttons.items():
                building = self.buildings_data[name]
                btn_text = f"{building.emoji} {building.name}\n+{building.click_power} клик | +{building.autoproduction}/сек"
                btn.config(text=btn_text)
            
            if self.selected_building:
                building = self.buildings_data[self.selected_building]
                count = self.game.get_building_count(self.selected_building)
                price = building.get_price(count)
                
                info_lines = []
                
                if building.name == 'Ферма' and count == 0:
                    info_lines.append("💰 БЕСПЛАТНО!")
                else:
                    info_lines.append(f"💰 Цена: {price} 🌾")
                
                info_lines.append(f"⚡ Клик: +{building.click_power} {building.resource}")
                info_lines.append(f"⚡ Авто: +{building.autoproduction}/сек {building.resource}")
                
                costs = []
                for res, amount in building.cost.items():
                    if amount > 0:
                        costs.append(f"{res}: {amount}")
                if costs:
                    info_lines.append("📦 Требует: " + " | ".join(costs))
                
                if building.unlock_cost and any(building.unlock_cost.values()) and count == 0:
                    unlocks = []
                    for res, amount in building.unlock_cost.items():
                        if amount > 0:
                            unlocks.append(f"{res}: {amount}")
                    info_lines.append("🔓 Открыть: " + " | ".join(unlocks))
                
                can_afford = self.game.resources.get('🌾 Пшеница', 0) >= price if price > 0 else True
                if building.name == 'Ферма' and count == 0:
                    can_afford = True
                
                for res, amount in building.cost.items():
                    if amount > 0 and self.game.resources.get(res, 0) < amount:
                        can_afford = False
                        break
                
                color = building.color if can_afford else '#E53935'
                self.selected_label.config(
                    text="\n".join(info_lines),
                    fg=color
                )
                
                status = "✅ Доступно!" if can_afford else "❌ Не хватает ресурсов!"
                self.hint_label.config(
                    text=f"{status} | Выбрано: {building.emoji} {building.name}",
                    fg=color
                )
            
            for widget in self.zone_widgets:
                zone = widget['zone']
                if zone.has_building():
                    click_power = zone.building.click_power
                    auto_power = zone.building.autoproduction
                    click_cost = int(zone.click_upgrade_cost * (1.5 ** zone.click_upgrade_level))
                    auto_cost = int(zone.auto_upgrade_cost * (1.5 ** zone.auto_upgrade_level))
                    
                    widget['zone_label'].config(
                        text=f"ЗОНА {zone.index+1}\n{zone.building.emoji} {zone.building.name}"
                    )
                    widget['click_btn'].config(
                        text=f"🖱️ КЛИК\n+{click_power} {zone.building.resource}",
                        bg=zone.building.color, state='normal'
                    )
                    widget['build_btn'].config(state='disabled', bg='#37474F', text='❌\nЗАНЯТО')
                    widget['demolish_btn'].config(state='normal', bg='#E53935', text='💥\nСНЕСТИ')
                    
                    can_click = self.game.resources.get('🌾 Пшеница', 0) >= click_cost
                    can_auto = self.game.resources.get('🌾 Пшеница', 0) >= auto_cost
                    
                    widget['click_upgrade_btn'].config(
                        state='normal',
                        bg='#FF8F00' if can_click else '#5D4037',
                        text=f"🖱️\n+1 КЛИК\n({click_cost}🌾)"
                    )
                    widget['auto_upgrade_btn'].config(
                        state='normal',
                        bg='#0D47A1' if can_auto else '#1A237E',
                        text=f"⚡\n+1 АВТО\n({auto_cost}🌾)"
                    )
                else:
                    widget['zone_label'].config(text=f"ЗОНА {zone.index+1}\n🟩 ПУСТО")
                    widget['click_btn'].config(
                        text="🖱️ КЛИК\n(нет здания)",
                        bg='#37474F', state='disabled'
                    )
                    widget['build_btn'].config(state='normal', bg='#FF6F00', text='🏗️\nПОСТРОИТЬ')
                    widget['demolish_btn'].config(state='disabled', bg='#4A148C', text='💥\nНЕТ ЗДАНИЯ')
                    widget['click_upgrade_btn'].config(state='disabled', bg='#3E2723', text='🖱️\nНЕТ ЗДАНИЯ')
                    widget['auto_upgrade_btn'].config(state='disabled', bg='#1A237E', text='⚡\nНЕТ ЗДАНИЯ')
        except Exception as e:
            print(f"Ошибка обновления UI: {e}")
