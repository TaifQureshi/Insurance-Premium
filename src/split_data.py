from src.config import get_config
import os
import logging
import pandas as pd
from src.get_data import get_processed_data
from sklearn.model_selection import train_test_split

logger = logging.getLogger('split_data')


def split_data(config_path: str = 'params.yaml') -> (pd.DataFrame, pd.DataFrame) or (None, None):
    config = get_config(config_path)
    train_path = config.get('split_data')['train_path']
    test_path = config.get('split_data')['test_path']
    if os.path.exists(train_path):
        try:
            logger.info('split data exists reading the present data')
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)
            return train_data, test_data
        except FileNotFoundError as e:
            logger.error("File not found")
            logger.exception(e)
            return None, None

    try:
        logger.info('cannot find the existing data')
        logger.info('creating the split data')
        data = get_processed_data(config_path)
        split_ratio = config.get('split_data')['split_ratio']
        random_state = config.get('split_data')['random_state']
        train, test = train_test_split(data, test_size=split_ratio, random_state=random_state)
        return train, test
    except Exception as e:
        logger.error('error')
        logger.exception(e)
        return None, None


if __name__ == '__main__':
    from src.set_logger import set_logger

    set_logger('split_data')
    train, test = split_data()

