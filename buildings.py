# buildings.py - Данные о зданиях (С БЕСПЛАТНОЙ ФЕРМОЙ)

class Building:
    """Класс здания"""
    def __init__(self, name, emoji, color, resource, 
                 click_power=1, autoproduction=1,
                 cost_wheat=0, cost_wood=0, cost_ore=0, cost_gold=0,
                 unlock_wheat=0, unlock_wood=0, unlock_ore=0, unlock_gold=0,
                 base_price=500, price_increase=2.0,
                 upgrade_cost_wheat=0, upgrade_cost_wood=0, upgrade_cost_ore=0, upgrade_cost_gold=0,
                 upgrade_multiplier=1.5):
        self.name = name
        self.emoji = emoji
        self.color = color
        self.resource = resource
        self.click_power = click_power
        self.autoproduction = autoproduction
        self.level = 1
        
        # Стоимость постройки
        self.cost = {
            '🌾 Пшеница': cost_wheat,
            '🪵 Древесина': cost_wood,
            '⛏️ Руда': cost_ore,
            '💰 Золото': cost_gold
        }
        
        # Условия открытия
        self.unlock_cost = {
            '🌾 Пшеница': unlock_wheat,
            '🪵 Древесина': unlock_wood,
            '⛏️ Руда': unlock_ore,
            '💰 Золото': unlock_gold
        }
        
        # Стоимость улучшения
        self.upgrade_cost_base = {
            '🌾 Пшеница': upgrade_cost_wheat,
            '🪵 Древесина': upgrade_cost_wood,
            '⛏️ Руда': upgrade_cost_ore,
            '💰 Золото': upgrade_cost_gold
        }
        
        self.upgrade_multiplier = upgrade_multiplier
        
        # Базовая цена и множитель для повторных построек
        self.base_price = base_price
        self.price_increase = price_increase
        
    def get_price(self, count):
        """Цена здания с учётом количества уже построенных"""
        # Первая ферма бесплатна!
        if self.name == 'Ферма' and count == 0:
            return 0
        if self.name == 'Ферма':
            # Вторая ферма = 500, третья = 1000 и т.д.
            return int(500 * (2.0 ** (count - 1)))
        return int(self.base_price * (self.price_increase ** count))
    
    def get_upgrade_cost(self, level):
        """Стоимость улучшения в зависимости от уровня"""
        cost = {}
        for res, amount in self.upgrade_cost_base.items():
            if amount > 0:
                cost[res] = int(amount * (self.upgrade_multiplier ** (level - 1)))
        return cost
    
    def can_upgrade(self, resources, level):
        """Проверка, можно ли улучшить здание"""
        cost = self.get_upgrade_cost(level)
        for res, amount in cost.items():
            if resources.get(res, 0) < amount:
                return False
        return True
    
    def can_build(self, resources, count=0):
        """Проверка ресурсов для постройки"""
        price = self.get_price(count)
        # Первая ферма бесплатна
        if self.name == 'Ферма' and count == 0:
            return True
        return resources.get('🌾 Пшеница', 0) >= price
    
    def can_unlock(self, resources):
        """Проверка условий открытия"""
        for res, amount in self.unlock_cost.items():
            if amount > 0 and resources.get(res, 0) < amount:
                return False
        return True

# Доступные здания
def get_buildings():
    return {
        '🌾 Ферма': Building(
            'Ферма', '🌾', '#4CAF50', '🌾 Пшеница',
            click_power=1, autoproduction=1,
            base_price=500, price_increase=2.0,
            upgrade_cost_wheat=50,
            upgrade_multiplier=1.5
        ),
        '🪵 Лесопилка': Building(
            'Лесопилка', '🪵', '#8D6E63', '🪵 Древесина',
            click_power=1, autoproduction=1,
            unlock_wheat=500,
            base_price=1000, price_increase=2.0,
            upgrade_cost_wheat=200, upgrade_cost_wood=50,
            upgrade_multiplier=1.6
        ),
        '⛏️ Рудник': Building(
            'Рудник', '⛏️', '#78909C', '⛏️ Руда',
            click_power=1, autoproduction=1,
            cost_wood=50,
            unlock_wheat=5000, unlock_wood=100,
            base_price=5000, price_increase=2.2,
            upgrade_cost_wheat=500, upgrade_cost_wood=100,
            upgrade_multiplier=1.7
        ),
        '🔨 Кузница': Building(
            'Кузница', '🔨', '#E65100', '💰 Золото',
            click_power=2, autoproduction=1,
            cost_wheat=1000, cost_wood=200, cost_ore=50,
            unlock_wheat=20000, unlock_wood=500,
            base_price=15000, price_increase=2.5,
            upgrade_cost_wheat=1000, upgrade_cost_wood=200, upgrade_cost_ore=50,
            upgrade_multiplier=1.8
        ),
        '🏰 Замок': Building(
            'Замок', '🏰', '#5D4037', '💰 Золото',
            click_power=5, autoproduction=3,
            cost_wheat=5000, cost_wood=1000, cost_ore=500, cost_gold=50,
            unlock_wheat=50000, unlock_wood=2000,
            base_price=50000, price_increase=2.5,
            upgrade_cost_wheat=2000, upgrade_cost_wood=500, upgrade_cost_ore=100, upgrade_cost_gold=20,
            upgrade_multiplier=1.8
        ),
        '🌿 Плантация': Building(
            'Плантация', '🌿', '#2E7D32', '🌾 Пшеница',
            click_power=3, autoproduction=5,
            cost_wheat=500, cost_wood=100,
            unlock_wheat=10000,
            base_price=3000, price_increase=2.0,
            upgrade_cost_wheat=300, upgrade_cost_wood=50,
            upgrade_multiplier=1.5
        ),
        '🎣 Рыбалка': Building(
            'Рыбалка', '🎣', '#00838F', '🌾 Пшеница',
            click_power=2, autoproduction=4,
            cost_wheat=300,
            unlock_wheat=8000,
            base_price=2000, price_increase=2.0,
            upgrade_cost_wheat=200,
            upgrade_multiplier=1.5
        ),
        '🧺 Ткацкая': Building(
            'Ткацкая', '🧺', '#4A148C', '🪵 Древесина',
            click_power=2, autoproduction=3,
            cost_wheat=1000, cost_wood=200,
            unlock_wheat=20000, unlock_wood=500,
            base_price=8000, price_increase=2.2,
            upgrade_cost_wheat=500, upgrade_cost_wood=100,
            upgrade_multiplier=1.7
        ),
        '🏛️ Храм': Building(
            'Храм', '🏛️', '#F9A825', '💰 Золото',
            click_power=10, autoproduction=10,
            cost_wheat=20000, cost_wood=5000, cost_ore=1000, cost_gold=200,
            unlock_wheat=100000, unlock_wood=5000,
            base_price=100000, price_increase=2.5,
            upgrade_cost_wheat=5000, upgrade_cost_wood=1000, upgrade_cost_ore=200, upgrade_cost_gold=50,
            upgrade_multiplier=2.0
        )
    }
