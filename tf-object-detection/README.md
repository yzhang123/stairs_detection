# Requirements
The Tensorflow Object Detection API has been installed as documented in the [installation instructions](https://github.com/tensorflow/models/blob/master/object_detection/g3doc/installation.md). This includes installing library dependencies, compiling the configuration protobufs and setting up the Python environment.
In the following instructions the `tensorflow/model` repository directory will be reference as `${PATH_TO_TENSORFLOW_MODEL_REPOSITORY}`.

For example:
```bash
export PATH_TO_TENSORFLOW_MODEL_REPOSITORY=../../models
```

# Download dataset and split into sets train, val, trainval and test
```bash
# From the stairs_detection/tf-object-detection directory
python fetch_cvhci_dataset.py
python filter_cvhci_dataset.py
python split_cvhci_dataset.py --dataset_dir=data/CVHCI --output_dir=data/CVHCI/ImageSets
```

# Convert dataset to TFRecords
```bash
# From the stairs_detection/tf-object-detection directory
python create_cvhci_tf_record.py --data_dir=data/CVHCI --set=train --output_path=data/cvhci_train.record

python create_cvhci_tf_record.py --data_dir=data/CVHCI --set=val --output_path=data/cvhci_val.record
```

# Download pretrained model
```bash
# From the stairs_detection/tf-object-detection directory
wget --directory-prefix=/tmp \
    http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet101_coco_11_06_2017.tar.gz
tar -xzvf /tmp/faster_rcnn_resnet101_coco_11_06_2017.tar.gz --directory=models
```

# Run the training job
```bash
# From the stairs_detection/tf-object-detection directory
# train
python ${PATH_TO_TENSORFLOW_MODEL_REPOSITORY}/object_detection/train.py --logtostderr --pipeline_config_path=faster_rcnn_resnet101_cvhci.config --train_dir=train_output
# use tensorboard to show training progress
tensorboard --logdir=train_output
```

# Run the evaluation job
```bash
# From the stairs_detection/tf-object-detection directory
python ${PATH_TO_TENSORFLOW_MODEL_REPOSITORY}/object_detection/eval.py --logtostderr --pipeline_config_path=faster_rcnn_resnet101_cvhci.config --checkpoint_dir=train_output --eval_dir=eval_output
# use tensorboard to show evaluation progress
tensorboard --logdir=eval_output
```

# Exporting the trained model for inference
```bash
# From the stairs_detection/tf-object-detection directory
# specify the checkpoint for inference export and create directory
export CHECKPOINT_NUMBER=28276
mkdir inference_output
# export inverence graph
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
python ${PATH_TO_TENSORFLOW_MODEL_REPOSITORY}/object_detection/export_inference_graph.py --input_type image_tensor --pipeline_config_path faster_rcnn_resnet101_cvhci.config --checkpoint_path train_output/model.ckpt-${CHECKPOINT_NUMBER} --inference_graph_path inference_output/output_inference_graph.pb
```

# Test the trained model with all images in the test_input directory
```bash
# From the stairs_detection/tf-object-detection directory
# create output directory
mkdir test_output
python test.py
```
