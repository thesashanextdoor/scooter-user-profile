import pandas as pd

from config import ConfigLoader
from user_safety_assessor import UserSafetyAssessor

if __name__ == '__main__':
    """
    Пример использования функционала
    """
    df = pd.read_csv("ks_22000.csv", sep=';', parse_dates=['gps_dt'])

    config = ConfigLoader()

    user_safety_assessor = UserSafetyAssessor(config)

    ride_df = df[df['ride_id'] == 0]
    ride_df10 = df[df['ride_id'] == 10]

    print(user_safety_assessor.get_user_driving_style_assessment([ride_df, ride_df10]))
