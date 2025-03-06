from sqlalchemy import create_engine, Column, String, Boolean, Float, Integer, DateTime, ForeignKey, Time
from sqlalchemy.orm import relationship, DeclarativeBase

from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)  # Используйте String для хранения ID пользователей (например, Telegram User ID)
    name = Column(String)
    subscription = Column(DateTime, default=datetime.now())  # True, если пользователь подписан на премиум-функции
    login = Column(String)  # Например, никнейм в Telegram
    current_weight = Column(Float)
    height = Column(Float)
    age = Column(Integer)
    is_male = Column(Boolean, default=True)
    activity_level = Column(Float)
    daily_message = Column(Boolean, default=False)
    breakfast_time = Column(Time, default=datetime.strptime("08:00", "%H:%M").time())  # Default 8:00 AM
    lunch_time = Column(Time, default=datetime.strptime("13:00", "%H:%M").time())  # Default 1:00 PM
    dinner_time = Column(Time, default=datetime.strptime("19:00", "%H:%M").time())  # Default 7:00 PM

    # Определение связи "один ко многим" с моделью FoodEntry
    food_entries = relationship("FoodEntry", backref="user") # backref создает поле user в FoodEntry

    def __repr__(self):
        return f"<User(id='{self.id}', name='{self.name}', subscription={self.subscription}, login='{self.login}')>"


# 3. Определение модели FoodEntry (Запись о еде)
class FoodEntry(Base):
    __tablename__ = 'food_entries'

    id = Column(Integer, primary_key=True)
    name = Column(String)  # Название еды
    calories = Column(Float)  # Калорийность
    timestamp = Column(DateTime, default=datetime.now)  # Время, когда была съедена еда (с датой и временем)
    user_id = Column(String, ForeignKey('users.id'))  # Внешний ключ, связывающий запись о еде с пользователем

    def __repr__(self):
        return f"<FoodEntry(name='{self.name}', calories={self.calories}, timestamp='{self.timestamp}')>"


class Recipe(Base):
    __tablename__ = 'resipes'
    id = Column(Integer, primary_key=True)
    meal_type = Column(String)
    name = Column(String)
    calories = Column(Float)
    text = Column(String)

    def __repr__(self):
        return f"Рецепт: {self.name}\nНа {self.calories} ккал\n{self.text}"