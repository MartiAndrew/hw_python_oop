from typing import List, Dict
from dataclasses import dataclass


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')
    # Здравствуй, Алексей, приятно познакомиться. Исправил класс на
    # датакласс как советовал, как то красиво сделать get_message не смог,
    # видел что кто-то делает через вывод словаря, но мне не понятно тогда,
    # что я должен ставить в атрибуты InfoClass в методе show_training_info
    # при возврате.


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        return None
        # Сначала исправил строку эту на докстинг, но pytest меня отругал:
        # test_homework.py:194: in test_Training_get_spent_calories
        # assert training.get_spent_calories() is None, (
        # E   AssertionError: Метод `get_spent_calories` класса `Training`
        # не должен высчитывать потреченные калории,
        # так как для каждого типа тренировки своя формула подсчета калорий.
        # E   assert 'Потраченные каллории' is None

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed_mc = self.get_mean_speed() * self.KMH_IN_MSEC
        result = (self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                  + (mean_speed_mc ** 2 / (self.height / self.CM_IN_M))
                  * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                  * self.weight) * self.duration * self.MIN_IN_H
        return result


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                * self.duration)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_class_d: Dict[str, [Training, int]] = {
        'SWM': [Swimming, 5],
        'RUN': [Running, 3],
        'WLK': [SportsWalking, 4]
    }
    if workout_type in training_class_d:
        if len(data) == training_class_d[workout_type][1]:
            return training_class_d[workout_type][0](*data)
    raise ValueError('Ошибка в пакете данных')


def main(training: Training) -> None:
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
