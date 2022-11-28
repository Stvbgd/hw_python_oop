class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: int,
                 distance: int,
                 mean_speed: float,
                 calories: int) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.mean_speed = mean_speed
        self.calories = calories

    def get_message(self):
        return (f'{self.training_type};'
                f'Длительность: {self.duration} ч.;'
                f'Дистанция: {self.distance} км;'
                f'Ср. скорость: {self.mean_speed} км/ч;'
                f'Потрачени ккал: {self.calories}.')
    pass


M_IN_KM = 1000


class Training:

    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 calories: float = 0.0,
                 distance: float = 0.0,
                 mean_speed: float = 0.0,
                 LEN_STEP: float = 0.65
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight
        self.calories = calories
        self.distance = distance
        self.mean_speed = mean_speed
        self.LEN_STEP = LEN_STEP
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / M_IN_KM
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
        pass


class Running(Training):

    """Тренировка: бег."""
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 CALORIES_MEAN_SPEED_MULTIPLIER: int = 18,
                 CALORIES_MEAN_SPEED_SHIFT: float = 1.79):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.CALORIES_MEAN_SPEED_MULTIPLIER = CALORIES_MEAN_SPEED_MULTIPLIER
        self.CALORIES_MEAN_SPEED_SHIFT = CALORIES_MEAN_SPEED_SHIFT

    def get_spent_calories(self):
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.mean_speed + self.CALORIES_MEAN_SPEED_SHIFT)
        * self.weight / M_IN_KM * self.duration)
        return calories
    
    def show_training_info(self):
        stas_idiot = InfoMessage(Running.__doc__, self.duration, self.distance, self.mean_speed, self.calories)
        return stas_idiot


class SportsWalking(Training):
   
    """Тренировка: спортивная ходьба."""
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 FIRST_KOEF: float = 0.035,
                 SECOND_KOEF: float = 0.029):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height
        self.FIRST_KOEF = FIRST_KOEF
        self.SECOND_KOEF = SECOND_KOEF

    def get_spent_calories(self):
        self.calories = ((self.FIRST_KOEF * self.weight + (self.mean_speed ** 2 / self.height) * 
        self.SECOND_KOEF * self.weight) * self.duration)
        return self.calories

    def get_distance(self) -> float:
        return super().get_distance()

    def show_training_info(self):
        stas_idiot = InfoMessage(SportsWalking.__doc__, self.duration, self.distance, self.mean_speed, self.calories)
        return stas_idiot


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self,
                 training_type: str = __doc__,
                 action: int = 0,
                 duration: float = 0,
                 mean_speed: float = 0,
                 weight: float = 0,
                 length_pool: int = 0,
                 count_pool: int = 0,
                 distance: float = 0,
                 LEN_STEP: float = 1.38,
                 calories: int = 0):
        self.training_type = training_type
        self.action = action
        self.duration = duration
        self.mean_speed = mean_speed
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.distance = distance
        self.LEN_STEP = LEN_STEP
        self.calories = calories
        
    def get_mean_speed(self):
        mean_speed = self.length_pool * self.count_pool / M_IN_KM / self.duration
        return mean_speed

    def get_distance(self) -> float:
        return super().get_distance()
    
    def get_spent_calories(self):
        self.calories = (self.mean_speed + 1.1) * 2 * self.weight * self.duration
        return self.calories
    
    def show_training_info(self):
        stas_idiot = InfoMessage(self.training_type,
                                 self.duration,
                                 self.distance,
                                 self.mean_speed,
                                 self.calories)
        return stas_idiot


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    slovar: dict = {
        'SWM': Swimming(data[0], data[1], data[2], data[3], data[4]),
        'RUN': Running(data[0], data[1], data[2]),
        'WLK': SportsWalking(data[0], data[1], data[2], data[3])}
    for i in slovar.keys():
        if workout_type == i:
            return (slovar[i])
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

