import logging
import yaml

from fastai.vision.learner import load_learner

from coral_classifier import CoralClassifier

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s'
)

CONFIG_PATH = 'model_config.yml'
DEFAULT_MODEL = '/mnt/store/data/assets/fwc-coral-videos/frames/sample-resnet34.pkl'
BENTO_REPO = '/mnt/store/data/models/bentoml/repository'

def save_service(model_path, model_name='learner'):
    model = load_learner(model_path)
    model.metrics = []
    svc = CoralClassifier()
    svc.pack(model_name, model)
    saved_path = svc.save_to_dir(repo_path)

    logging.info(f"saved model {model_path} as BentoML service to {saved_path}")


def read_config(config_path='model_config.yml'):
    with open(config_path) as config:
        config = yaml.safe_load(config)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'model_path',
        type=str,
        help='path to serialized model'
    )

    save_service(model_path, model_name)