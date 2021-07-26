import numpy as np
import rdp

from factors.abstract_factor import UnsafetynessFactor


class FastPivotFactor(UnsafetynessFactor):
    """
    Класс-обработчик фактора прохода поворота на большой скорости (микроаварийная ситуация)
    """

    def __init__(self, wheel_threshold=18, min_angle_degree=50, tolerance=0.0001):
        """
        wheel_threshold - скорость, на которой проходится поворот
        min_angle_degree - минимальное изменение направления движения для того, чтобы считаться поворотом
        tolerance - число, определяющее степень упрощения кривой в алгоритме Рамера — Дугласа — Пекера
        """
        self.wheel_threshold = wheel_threshold
        self.min_angle_degree = min_angle_degree
        self.tolerance = tolerance

    def preprocess_data(self, df):
        pass

    def get_unsafety_points(self, df):
        """
        Функция, которая возвращает точки прохождения поворотов на большой скорости
        """
        tolerance = self.tolerance
        min_angle = self.min_angle_degree / 180 * np.pi

        df_local = df.copy()
        df_local.index = range(len(df))
        points = df_local.loc[:, ['lat', 'lon']].values
        mask = np.array(rdp.rdp(points, tolerance, return_mask=True))
        simplified_df = df_local[mask]
        simplified = simplified_df.loc[:, ['lat', 'lon']]
        directions = np.diff(simplified, axis=0)
        theta = self._angle(directions)
        idx = np.where(theta > min_angle)[0] + 1
        turning_points_df = simplified_df.iloc[idx]
        unsafety_points = turning_points_df[turning_points_df['wheel'] >= self.wheel_threshold]
        fast_pivot_coords = unsafety_points.loc[:, ['lat', 'lon']].values
        return fast_pivot_coords

    @staticmethod
    def _angle(direction):
        dir2 = direction[1:]
        dir1 = direction[:-1]
        return np.arccos((dir1 * dir2).sum(axis=1) / (
            np.sqrt((dir1 ** 2).sum(axis=1) * (dir2 ** 2).sum(axis=1))))
