import os
import pandas as pd
from src.config import get_config, get_base_path
import logging
import numpy as np

logger = logging.getLogger('data')


def get_raw_data(config_path: str = 'params.yaml') -> pd.DataFrame or None:
    config = get_config(config_path)
    base_path = get_base_path()
    raw_data_path = config['load_data']['raw_data']
    data = None
    try:
        data = pd.read_csv(os.path.join(base_path, raw_data_path))
    except FileNotFoundError as e:
        logging.error(f"File not found at {raw_data_path}")
        raise FileNotFoundError
    except Exception as e:
        logger.error("Unexpected error")
        logger.exception(e)
        raise Exception

    return data


def get_processed_data(config_path: str = 'params.yaml') -> pd.DataFrame or None:
    config = get_config(config_path)
    process_data = config['load_data']['process_data']
    base_dir = get_base_path()
    full_path = os.path.join(base_dir, process_data)
    if os.path.exists(full_path):
        logger.info('file already exists reading it')
        data = pd.read_csv(full_path)
        return data

    logger.info('file not present processing the raw data')

    # age bin
    data = get_raw_data(config_path)
    age_bin = [17, 25, 40, 60, np.Inf]
    lables = [0, 1, 2, 3]
    data['age_bin'] = pd.cut(data["age"], bins=age_bin, labels=lables)

    # bmi bin
    bmi_bin = [0, 18.5, 25, 30, np.Inf]
    bmi_lable = [0, 1, 2, 3]
    data['bmi_bin'] = pd.cut(data['bmi'], bins=bmi_bin, labels=bmi_lable)

    data.drop(axis=1, columns=['age', 'bmi'], inplace=True)
    data['expenses'] = data['expenses'].apply(np.round)
    en_coded = pd.get_dummies(data, columns=['sex', 'smoker', 'region'])

    logger.info("saving the data for future use")
    if not os.path.exists(os.path.dirname(full_path)):
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
    en_coded.to_csv(full_path)

    return en_coded


if __name__ == '__main__':
    from src.set_logger import set_logger

    set_logger('test_data')
    data = get_processed_data()
