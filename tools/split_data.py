from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import sys
import os
import numpy as np

def parse_args():
  """
  Parse input arguments
  """
  parser = argparse.ArgumentParser(description='split data into train, val, test')
  parser.add_argument('input_dir',  help='image directory')

  parser.add_argument('output_dir', help='output directory')

  if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

  args = parser.parse_args()
  return args



if __name__ == '__main__':
    args = parse_args()
    print('Called with args:')
    print(args)

    in_dir = args.input_dir
    out_dir = args.output_dir

    assert(os.path.exists(in_dir), "path does not exist")
    assert(os.path.exists(out_dir), "path does not exist")

    files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
    np.random.shuffle(files)

    num_test = int(len(files) / 5)
    num_trainval = len(files) - num_test
    num_val = int(num_trainval / 5)
    num_train = num_trainval - num_val
    print(num_test, num_val, num_train, num_trainval)

    file_indices = [os.path.splitext(f)[0] for f in files]

    train, val, trainval, test = file_indices[:num_train], file_indices[num_train:num_train+num_val],\
                                 file_indices[:num_train+num_val], file_indices[-num_test:]

    with open(os.path.join(out_dir, 'train'), 'w') as fp:
        for x in train:
            fp.write(x + '\n')
    with open(os.path.join(out_dir, 'val'), 'w') as fp:
        for x in val:
            fp.write(x + '\n')
    with open(os.path.join(out_dir, 'trainval'), 'w') as fp:
        for x in trainval:
            fp.write(x + '\n')
    with open(os.path.join(out_dir, 'test'), 'w') as fp:
        for x in test:
            fp.write(x + '\n')





