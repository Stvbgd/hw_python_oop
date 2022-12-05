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
        return str(f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {"%.3f" % round(self.duration, 3)} ч.; '
                   f'Дистанция: {"%.3f" % round(self.distance, 3)} км; '
                   f'Ср. скорость: {"%.3f" % round(self.speed, 3)} км/ч; '
                   f'Потрачено ккал: {"%.3f" % round(self.calories, 3)}.')
        pass


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 training_type: str = None,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = training_type
        # self.calories = 0
        # self.distance = 0
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()
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
        return info
        pass


class Running(Training):
    """Тренировка: бег"""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 training_type: str = 'Running',
                 ):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = training_type
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.mean_speed
                    + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM * (self.duration
                    * self.MIN_IN_H))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба"""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 training_type: str = 'SportsWalking'
                 ):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height
        self.training_type = training_type
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()

    def get_spent_calories(self) -> float:
        self.calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                         + (((self.mean_speed * self.KMH_IN_MSEC)**2)
                          / (self.height / self.CM_IN_M))
                         * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                         * self.weight) * (self.duration * self.MIN_IN_H))
        return self.calories


class Swimming(Training):
    """Тренировка: плавание"""
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 #  distance: float,
                 #  calories: int,
                 training_type: str = 'Swimming'):
        self.training_type = training_type
        self.action = action
        self.duration = duration
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.weight = weight
        self.mean_speed = self.get_mean_speed()
        self.distance = self.get_distance()
        self.calories = self.get_spent_calories()

    def get_mean_speed(self):
        self.mean_speed = (self.length_pool * self.count_pool
                           / self.M_IN_KM / self.duration)
        return self.mean_speed

    def get_spent_calories(self):
        self.calories = ((self.mean_speed + self.CALORIES_MEAN_SPEED_SHIFT)
                         * self.CALORIES_WEIGHT_MULTIPLIER
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
    print(training.show_training_info().get_message())


if __name__ == '__main__':

    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
