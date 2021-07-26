from factors.abstract_factor import UnsafetynessFactor


class HardStopFactor(UnsafetynessFactor):
    """
    Класс-обработчик фактора резкого торможения с последующей остановкой (микроаварийная ситуация)
    """

    def __init__(self, acc_threshold=-2.5, wheel_threshold_after_stop=1, num_zero_points_after_stop=1,
                 min_acc_threshold=-100):
        """
        acc_threshold - ускорение, начиная с которого торможение считается резким
        min_acc_threshold - нижняя граница ускорения торможения;
                            введена т.к. в данных есть точки с неадекватно большим ускорением, например -5000 м/с^2
                            мы связываем такие большие отрицательные ускорения с багом датчиков,
                            но допускаем наличие других причин
        wheel_threshold_after_stop - скорость, которая определяет отсутствие значимого движения у самоката, например 1км/ч
        num_zero_points_after_stop - кол-во точек после торможения с незначимой скоростью
        """
        self.acc_threshold = acc_threshold
        self.wheel_threshold_after_stop = wheel_threshold_after_stop
        self.num_zero_points_after_stop = num_zero_points_after_stop
        self.min_acc_threshold = min_acc_threshold

    def preprocess_data(self, df):
        """
        Функция для расчета ускорений по формуле a[i] = (v[i] - v[i-1]) / (t[i] - t[i-1])
        У первой точки датафрейма ускорение будет 0
        """
        df_local = df.copy()
        df_local.index = range(len(df))
        df_local['acc'] = 0
        for i in range(1, len(df_local)):
            wheel_dif = (df_local.loc[i, 'wheel'] - df_local.loc[i - 1, 'wheel']) * 1000 / 3600
            time_dif = (df_local.loc[i, 'gps_dt'] - df_local.loc[i - 1, 'gps_dt']).total_seconds()
            df_local.loc[i, 'acc'] = wheel_dif / time_dif
        df_local.index = df.index
        return df_local

    def get_unsafety_points(self, df):
        """
        Функция, которая возвращает точки резких торможений
        """
        df_acc = self.preprocess_data(df)
        df_acc_local = df_acc.copy()
        df_acc_local.index = range(len(df_acc))
        df_acc_local['is_hard_stop'] = False

        for i in range(len(df_acc_local) - self.num_zero_points_after_stop):
            if (df_acc_local.loc[i]['acc'] <= self.acc_threshold) and \
                    (df_acc_local.loc[i]['acc'] >= self.min_acc_threshold) and \
                    (df_acc_local.loc[i]['wheel'] <= self.wheel_threshold_after_stop):
                for j in range(1, self.num_zero_points_after_stop + 1):
                    if df_acc_local.loc[i + j, 'wheel'] > self.wheel_threshold_after_stop:
                        break
                    elif (df_acc_local.loc[i + j, 'wheel'] <= self.wheel_threshold_after_stop) and \
                            (j == self.num_zero_points_after_stop):
                        df_acc_local.loc[i, 'is_hard_stop'] = True
        df_acc_local.index = df_acc.index
        hard_stop_coords = df_acc_local[df_acc_local['is_hard_stop'] == True].loc[:, ['lat', 'lon']].values
        return hard_stop_coords
