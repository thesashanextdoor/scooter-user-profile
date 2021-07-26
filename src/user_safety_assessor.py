from ride_safety_assessor import RideSafetyAssessor


class UserSafetyAssessor:
    def __init__(self, config):
        """
        num_last_considering_rides - количество последних рассматриваемых поездок,
            по которым считается оценка аккуратности вождения пользователя
        unsafety_factors_handlers - список объектов классов-обработчиков факторов небезопасного вождения
        factors_weights - веса, характеризующие вклад каждого фактора в итоговую оценку аккуратности вождения
        max_unsafety_points_by_factors - максимальное число микроаварийных ситуаций (резкое торможение или быстрое
            прохождение поворота)
        по каждому фактору - влияет на расчет оценки аккуратности
        ride_safety_assessor - объект класса, в котором инкапсулирована логика расчета оценки аккуратности
            на основе одной поездки
        """
        self.config = config
        self.num_last_considering_rides = config.num_last_considering_rides
        self.safety_assessment = 10
        max_rating_decrease = round(self.safety_assessment / self.num_last_considering_rides, 1)
        self.unsafety_factors_handlers = config.factors_handlers_list
        self.factors_weights = config.factors_weights
        self.max_unsafety_points_by_factors = config.max_unsafety_points_by_factors
        self.ride_safety_assessor = RideSafetyAssessor(max_rating_decrease, self.unsafety_factors_handlers,
                                                       self.factors_weights,
                                                       self.max_unsafety_points_by_factors)

    def get_user_driving_style_assessment(self, last_rides_df_list):
        """
        Функция, которая возвращает оценку аккуратности вождения пользователя
         на основе конфигурируемого числа последних поездок
        """
        if len(last_rides_df_list) < self.num_last_considering_rides:
            last_rides_df_list_local = last_rides_df_list.copy()
        else:
            last_rides_df_list_local = last_rides_df_list[-self.num_last_considering_rides:].copy()

        current_safety_assessment = self.safety_assessment
        for current_ride_df in last_rides_df_list_local:
            current_safety_assessment -= self.ride_safety_assessor.get_ride_driving_style_assessment(current_ride_df)
        return max(round(current_safety_assessment, 2), 0)
