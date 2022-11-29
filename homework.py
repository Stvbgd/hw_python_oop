class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: int,
                 distance: int,
                 speed: float,
                 calories: float) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return str(f'{self.training_type}; '
                   f' Длительность: {self.duration} ч.;'
                   f' Дистанция: {round(self.distance, 3)} км;'
                   f' Ср. скорость: {round(self.speed, 3)} км/ч;'
                   f' Потрачено ккал: {round(self.calories, 3)}.')
    pass


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_MIN = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 mean_speed: float,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight
        self.calories = 0
        self.distance = 0
        self.mean_speed = 0
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_speed = self.distance / self.duration
        return self.mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return info.get_message()
        pass


class Running(Training):
    """Тренировка: бег"""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 training_type: str = __doc__,
                 ):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = training_type
        # self.get_mean_speed(self, Training)

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.mean_speed
                    + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM * (self.duration
                    * self.H_IN_MIN))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба"""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    FIRST_KOEF = 0.035
    SECOND_KOEF = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 training_type: str = __doc__
                 ):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height
        self.training_type = training_type
        # self.mean_speed

    def get_spent_calories(self) -> float:
        self.calories = ((self.FIRST_KOEF * self.weight + (self.mean_speed ** 2
                          / self.height)
                          * self.SECOND_KOEF * self.weight)
                         * (self.duration * self.H_IN_MIN))
        return self.calories


class Swimming(Training):
    """Тренировка: плавание"""
    THIRD_KOEF = 1.1
    LEN_STEP = 1.38

    def __init__(self,
                 action: int = 0,
                 duration: float = 0,
                 weight: float = 0,
                 length_pool: int = 0,
                 count_pool: int = 0,
                 distance: float = 0,
                 mean_speed: float = 0,
                 training_type: str = __doc__,
                 calories: int = 0):
        self.training_type = training_type
        self.action = action
        self.duration = duration
        self.mean_speed = mean_speed
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.distance = distance
        self.calories = calories

    def get_mean_speed(self):
        mean_speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self):
        self.calories = ((self.mean_speed + self.THIRD_KOEF) * 2
                         * self.weight * self.duration)
        return self.calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    slovar = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    for i in slovar.keys():
        if workout_type == i:
            target_class = slovar[i]
            object = target_class(*data)
            return object
    pass


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
