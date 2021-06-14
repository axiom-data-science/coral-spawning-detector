# Coral Spawning Detector

This repo is a collection of models, applications, and configurations used to create an [automated coral spawning detection and alerting system](coral-spawning.srv.axds.co) in collaboration with the [Florida Fish and Wildlife Conservation Commission](https://myfwc.com/) and [The Florida Aquarium](https://www.flaquarium.org/).

## System Components

The implemented system is designed to ingest video data streams from networked cameras, apply a spawning detection model to the stream to identify when coral are spawning, provide alerts to registered users if a spawning event is detected, and gather statistics about all spawning events.

The system was built on open source software and all components of the system are pubicaly available to assist in reuse by other entities.

### Video Ingestion

The video ingestion system includes components to save entire video streams to storage, persist a subset of frames to storage, and make API requests to other services. A minimal configuration for ingestion of networked cameras and examples are available in the [FWC Camera Ingest repo](https://github.com/axiom-data-science/coral-camera-ingest).

### Spawning Detection Model

The spawning detection model is an off the shelf ResNet34 implemented in [fastai](https://www.fast.ai/) and trained
on spawning coral video samples provided to us by The Florida Aquarium. The model is packaged as a BentoML service
and is available as a [Docker image](https://hub.docker.com/repository/docker/axiom/coral-spawning-detector).

### Log Parsing and Alerting

The logs and Prometheus metrics from the detection model are parsed for spawning events and calculations are made about the
duration of such events. The results from these calculations are ingested into Graphana which is configured to
to send alerts to an email list when a spawning event occurs.