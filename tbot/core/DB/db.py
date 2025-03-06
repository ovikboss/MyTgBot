from pyexpat.errors import messages
from sqlalchemy.orm import  sessionmaker
from sqlalchemy import create_engine, select
from .models import Base, User, FoodEntry, Recipe
from datetime import datetime, timedelta


from core.DB.config import Settings


class Database:

    def __init__(self):
        settings = Settings()
        self.engine = create_engine(f"postgresql+psycopg2://{settings.USER}:{settings.PASSWORD}@db:{settings.PORT}/{settings.DBNAME}",
                                 isolation_level="READ COMMITTED",query_cache_size = 0 )
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def register_user(self, user_id, name, login, current_weight, height, age, is_male,activity_level):
        """Registers a new user in the database."""

        existing_user = self.session.query(User).filter(User.id == user_id).first()
        if existing_user:
                print(f"User with id {user_id} already exists.")
                return False

        user = User(name = name, login =  login,
                    current_weight = current_weight,
                    height = height,
                    age = age,
                    is_male = is_male,
                    activity_level = activity_level, id = user_id)
        self.session.add(user)
        try:
            self.session.commit()
            print(f"User {user.name} registered successfully.")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error registering user: {e}")
            return False

    def add_food(self,user_id, food_name, calories):
        food = FoodEntry(name = food_name, user_id = user_id, calories = calories)
        self.session.add(food)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error registering user: {e}")


    def get_today_food(self, user_id):
        now = datetime.now()
        one_day_ago = now - timedelta(days=1)

        food_entries = self.session.query(FoodEntry).filter(
                FoodEntry.user_id == str(user_id),
                FoodEntry.timestamp >= one_day_ago,
                FoodEntry.timestamp <= now  # Include entries up to now
                ).all()
        return food_entries

    def get_show_daily(self):
            return self.session.query(User).all()

    def get_data_bmr(self, user_id):
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            bmr  = self.calculate_bmr(user.current_weight, user.height, user.age, user.is_male)
            return bmr
        else:
            return False



    def calculate_bmr(self, weight_kg: float, height_cm: float, age_years: int, is_male: bool) -> float:
            """Calculates Basal Metabolic Rate (BMR) using Harris-Benedict equation."""
            if is_male:
                bmr = 66.5 + (13.75 * weight_kg) + (5.0 * height_cm) - (6.78 * age_years)
            else:
                bmr = 655 + (9.56 * weight_kg) + (1.85 * height_cm) - (4.68 * age_years)
            return bmr

    def get_activity_level(self, user_id):
        activity = self.session.query(User.activity_level).filter(User.id == user_id).first()[0]
        activity = 1.2 if activity < 2 else  1.4 if activity < 3 else 1.55 if activity < 4 else 1.7
        return activity

    def eat_time_entered(self, user_id, time, meal_type):
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            if meal_type == "ужин":
                 user.dinner_time = time
            elif meal_type == "завтрак":
                 user.breakfast_time = time
            else:
                 user.lunch_time = time
            try:
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                print(f"Error registering user: {e}")
            from core.middlewares.scheduler import SchedulerCustom
            SchedulerCustom.update_user_reminders(user, meal_type=meal_type, percent =0.3)
            return True
        else:
            return False


    def get_user(self, user_id):
        return self.session.query(User).filter(User.id == user_id).first()

    def get_user_subscribe(self, user_id):
        check = self.session.query(User.subscription).execution_options(compiled_cache=None).filter(User.id == str(user_id)).first()
        return check

    def get_recipe(self,calories, meal_type):
        recipe = self.session.query(Recipe).filter(Recipe.meal_type == meal_type,
            Recipe.calories  <= float(calories) + 150,
            Recipe.calories  >= float(calories)- 150,).all()
        return recipe

    def change_user_subscribe(self,user_id):
        user = self.session.query(User).filter(User.id == str(user_id)).first()
        user.subscription = True
        try:
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            print(ex)

    def change_message_on(self, user_id):
        user = self.session.query(User).filter(User.id == str(user_id)).first()
        if user.daily_message:
            user.daily_message = False
            message = "Уведомления выключены"
        else:
            user.daily_message = True
            message = "Уведомления включены"
        try:
            self.session.commit()
            return message
        except Exception as ex:
            self.session.rollback()
            print(ex)
            return "ошибка"



db = Database()










