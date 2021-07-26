from abc import ABC, abstractmethod


class UnsafetynessFactor(ABC):
    """
    Базовый класс-обработчик факторов небезопасного вождения
    """

    @abstractmethod
    def preprocess_data(self, df):
        pass

    @abstractmethod
    def get_unsafety_points(self, df):
        """
        Функция, которая определяет небезопасные точки по отношению к некоторому фактору
        Например: точки прохождения поворотов на большой скорости или точки резких торможений
        """
        pass

    def get_num_unsafety_points(self, df):
        """
        Функция, возвращающая количество точек, в которых было идентифицировано неаккуратное вождение
        """
        return len(self.get_unsafety_points(df))
