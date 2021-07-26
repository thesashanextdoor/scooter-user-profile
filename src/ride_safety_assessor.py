class RideSafetyAssessor:
    def __init__(self, max_rating_decrease, unsafety_factors_handlers, factors_weights, max_unsafety_points_by_factors):
        """
        unsafety_factors_handlers - список объектов классов - обработчиков факторов небезопасного вождения
            Например: HardStopFactor, FastPivotFactor
            Для добавления новых факторов небезопасного вождения
            (пример: фактор резкого торможения, фактор прохода поворота на большой скорости)
            достаточно написать реализацию абстрактного класса UnsafetynessFactor
        """
        self.max_rating_decrease = max_rating_decrease
        self.unsafety_factors_handlers = unsafety_factors_handlers
        self.factors_weights = factors_weights
        self.max_unsafety_points_by_factors = max_unsafety_points_by_factors

    def get_ride_driving_style_assessment(self, df):
        """
        Функция, возвращающая величину, которая будет отниматься от рейтинга пользователя для одной поездки.
        На формирование оценки влияют факторы небезопасного вождения, определенные в unsafety_factors_handlers
        """
        ride_assessment = 0
        for i, factor_handler in enumerate(self.unsafety_factors_handlers):
            current_unsafety_points = factor_handler.get_num_unsafety_points(df)
            factor_weight = self.factors_weights[i]
            max_factor_decrease = self.max_rating_decrease * factor_weight
            max_unsafety_points = self.max_unsafety_points_by_factors[i]
            if current_unsafety_points < max_unsafety_points:
                ride_assessment += max_factor_decrease * current_unsafety_points / max_unsafety_points
            else:
                ride_assessment += max_factor_decrease
        return ride_assessment
