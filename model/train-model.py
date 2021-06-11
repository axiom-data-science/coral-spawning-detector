#!python
"""Build coral spawning detection model.

Script to recreate, or train, another coral detection model that is derived
from the notebook used to create the original model used in the FWC Coral Spawning
project.
"""
import fastai.vision.all as fai_vision


def prepare_data_loader(image_dir):
    """Given path to image directory, return DataLoader."""
    images = fai_vision.get_image_files(image_dir)

    # assume dir struct is: <path>/<coral>/{'positive', 'negative'}/<images>
    labels = [str(img.parent).split('/')[-1] for img in images]
    data_loader = fai_vision.ImageDataLoaders.from_lists(
        'frames', # dunno why I need this here
        images,
        labels
    )

    return data_loader


def train_model(
    data_loader,
    model=fai_vision.resnet34,
    metrics=fai_vision.error_rate
):
    """Given DataLoader, return trained model."""
    model = fai_vision.cnn_learner(
        data_loader,
        model,
        metrics=metrics
    )
    model.fine_tune(1)

    return model


def create_model(
    image_dir,
    model_save_path,
):
    """Load training data, train model, and save to disk"""
    data_loader = prepare_data_loader(image_dir)
    model = train_model(data_loader)
    model.export(fname=model_save_path)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'image_dir',
        type=str,
        help='Path to training image directory'
    )
    parser.add_argument(
        'model_save_path',
        type=str,
        help='Path to save serialized trained model'
    )
    args = parser.parse_args()
    create_model(args.image_dir, args.model_save_path)