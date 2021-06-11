# Coral Spawning Detector Model

A [BentoML](https://www.bentoml.ai/) based service that serves the coral detection
model developed for a Florida Fish and Wildlife Conservation Commmission (FWC) funded [coral
spawning detection project](http://stage-coral-spawning.srv.axds.co/).

## Model

The model is an off the shelf ResNet34 implemented in [fastai](https://www.fast.ai/).

It is available as a [Docker image](https://hub.docker.com/repository/docker/axiom/coral-spawning-detector).

### Model training

The model was trained using video of four different coral spawning in aquaria provided by the Florida Aquarium.
The videos were split into individual frames, then manually divided into directories of non-spawning images ("negative") and
spawning images ("positive").

These images were then used to train the last, dense layer of a ResNet34 model using the script `train-model.py`.
Note that the notebook is not directly runnable and reproducible because the training data is not publically available.

### Model Deployment

The trained model was serialized and packed into a BentoService and then containerized so that it could be run using
Docker.

Once the model has been built, it can be ran using Docker commands such as:

```bash
docker run -p 5000:5000 axiom/coral-spawning-detector:latest
```

To use the running coral spawning detector, you can POST an image to the service and it returns "positive":

```bash
curl -X POST "http://localhost:5000/predict" -F "image=@sample-data/positive-01.png
"positive"
```

### Updating the model

If a model is retrained and serialized in a pickled format, the model can be updated using the `update_model.sh` script.

#### Environment prerequisites for model

Create a python environment with `requirements.txt` installed.  BentoML is only available in `pip`, so
it is easier to just install everything using that package manager.

```bash
conda create --name coral-model python=3.7
conda activate coral-model
pip install -f requirements.txt
```

#### Update the model

To update the model, run `update_model.sh`:

```bash
bash update_model.sh
```

This script will:

1. Update the BentoService.

2. Build a Docker image of the BentoService updated in step 1.