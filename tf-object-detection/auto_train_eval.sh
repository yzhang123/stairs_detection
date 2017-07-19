#!/bin/bash

MAX_ITERATIONS=150000
TRAIN_EVAL_STEPSIZE=5000
CLASSIFICATION_SCORE_THRES=0.0

mkdir -p /tmp/p17g3
cp faster_rcnn_resnet101_cvhci.config /tmp/p17g3/faster_rcnn_resnet101_cvhci.config

mkdir train_output_backup

# set second_stage_post_processing score_threshold to CLASSIFICATION_SCORE_THRES, i.e. only boxes with scores above the specified value will
# be regarded as positive

sed -i -e "s/^        score_threshold: [0-9].[0-9]/        score_threshold: $CLASSIFICATION_SCORE_THRES/g" /tmp/p17g3/faster_rcnn_resnet101_cvhci.config


for i in `seq $TRAIN_EVAL_STEPSIZE $TRAIN_EVAL_STEPSIZE $MAX_ITERATIONS`; do
  sed -i -e "s/^  num_steps: [0-9]*/  num_steps: $i/g" /tmp/p17g3/faster_rcnn_resnet101_cvhci.config

  # train
  python ${PATH_TO_TENSORFLOW_MODEL_REPOSITORY}/object_detection/train.py --logtostderr --pipeline_config_path=/tmp/p17g3/faster_rcnn_resnet101_cvhci.config --train_dir=train_output
  # evaluate
  python ${PATH_TO_TENSORFLOW_MODEL_REPOSITORY}/object_detection/eval.py --logtostderr --pipeline_config_path=/tmp/p17g3/faster_rcnn_resnet101_cvhci.config --checkpoint_dir=train_output --eval_dir=eval_output
  # backup weights to other location
  cp train_output/model.ckpt-${i}* train_output_backup/
done

rm /tmp/p17g3/faster_rcnn_resnet101_cvhci.config
