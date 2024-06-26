from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Выводимое сообщение."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    COEFF_RUN_1: ClassVar[int] = 18
    COEFF_RUN_2: ClassVar[int] = 20
    HR_TO_MIN: ClassVar[int] = 60

    def get_spent_calories(self) -> float:
        minutes = self.duration * self.HR_TO_MIN
        return ((self.COEFF_RUN_1
                * self.get_mean_speed() - self.COEFF_RUN_2)
                * self.weight / self.M_IN_KM * minutes)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_SQR: ClassVar[int] = 2
    COEF_CALORIE_4: ClassVar[float] = 0.029
    COEF_CALORIE_5: ClassVar[float] = 0.035
    HR_TO_MIN: ClassVar[int] = 60

    height: float

    def get_spent_calories(self) -> float:
        return (self.COEF_CALORIE_5 * self.weight
                + (self.get_mean_speed() ** self.COEFF_SQR // self.height)
                * self.COEF_CALORIE_4
                * self.weight
                ) * self.duration * self.HR_TO_MIN


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    COEFF_WLK_1: ClassVar[int] = 2
    COEFF_WLK_2: ClassVar[float] = 1.1

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed()
                + self.COEFF_WLK_2) * self.COEFF_WLK_1 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_trn_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in dict_trn_types:
        return dict_trn_types[workout_type](*data)
    raise ValueError(f"{workout_type} не поддерживается")


def main(training: Training) -> None:
    """Главная функция."""
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
