import yaml

from factors.fast_pivot_factor import FastPivotFactor
from factors.hard_stop_factor import HardStopFactor

CONFIG_PATH = '../config/config.yaml'


class ConfigLoader:
    """
    Класс, содержащий конфигурационные свойства модуля оценки аккуратности вождения
    """

    def __init__(self):
        with open(CONFIG_PATH, 'r') as f:
            self.cfg = yaml.safe_load(f)

    @property
    def num_last_considering_rides(self):
        """
        Число рассматриваемых последних поездок на самокате, на основе которых считается оценка аккуратности вождения
        """
        return self.cfg['userSafetyAssessor']['numLastConsideringRides']

    @property
    def factors_weights(self):
        """
        Веса, характеризующие вклад каждого фактора в итоговую оценку аккуратности вождения
        """
        factors_names = self.cfg['unsafetyFactors'].keys()
        factors_weights_list = list()
        for factor_name in factors_names:
            factors_weights_list.append(self.cfg['unsafetyFactors'][factor_name]['weight'])
        return factors_weights_list

    @property
    def max_unsafety_points_by_factors(self):
        """
        Максимальное число микроаварийных ситуаций (резкое торможение или быстрое прохождение поворота)
        по каждому фактору - влияет на расчет оценки аккуратности
        """
        factors_names = self.cfg['unsafetyFactors'].keys()
        factors_max_unsafety_points = list()
        for factor_name in factors_names:
            factors_max_unsafety_points.append(self.cfg['unsafetyFactors'][factor_name]['maxOccurrences'])
        return factors_max_unsafety_points

    @property
    def factors_handlers_list(self):
        """
        Список объектов классов-обработчиков факторов небезопасного вождения
        """
        factors_names = self.cfg['unsafetyFactors'].keys()
        factors_handlers_list = list()
        for factor_name in factors_names:
            if factor_name == 'hardStopFactor':
                factors_handlers_list.append(
                    HardStopFactor(**self.cfg['unsafetyFactors']['hardStopFactor']['hyperparameters']))
            elif factor_name == 'fastPivotFactor':
                factors_handlers_list.append(
                    FastPivotFactor(**self.cfg['unsafetyFactors']['fastPivotFactor']['hyperparameters']))
        return factors_handlers_list
