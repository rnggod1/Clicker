# zones.py - Классы зон

class Zone:
    """Класс зоны (ячейка на карте)"""
    def __init__(self, index):
        self.index = index
        self.building = None
        self.resource = 0
        self.building_count = 0  # Сколько зданий этого типа уже построено
        
    def has_building(self):
        return self.building is not None
    
    def get_resource_name(self):
        return self.building.resource if self.building else "Пусто"
    
    def get_display_name(self):
        if self.building:
            return f"{self.building.emoji} {self.building.name}"
        return "🟩 Пусто"
