import argparse
from tensorflow.python.tools.inspect_checkpoint import print_tensors_in_checkpoint_file


if __name__=="__main__":
	parser = argparse.ArgumentParser(description='print checkpoints')
	parser.add_argument('file_path', type=str)
	args = parser.parse_args()
	checkpoint_path = args.file_path
	print_tensors_in_checkpoint_file(file_name=checkpoint_path, tensor_name='', all_tensors=True)
