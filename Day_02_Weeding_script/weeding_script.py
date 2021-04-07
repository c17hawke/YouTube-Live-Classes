import os
import shutil
from PIL import Image
import argparse


# TARGET_DIR = "demo_dir"

def move_to_trash(file_):
	shutil.move(file_, "Trash")

def weed_out(TARGET_DIR):
	os.chdir(TARGET_DIR)

	print(f'curent working dir: {os.getcwd()}')

	files = os.listdir(".")

	os.makedirs("Trash", exist_ok=True)
	print(f'Trash directory created')

	print("Starting file read operation\n")
	for file_ in files:
		try:
			print("###"*20)
			print(f"Opening {file_}\n")
			Image.open(file_)
		except Exception as e:
			move_to_trash(file_)
			print(f"Error: {e}")
			print(f"{file_} moved to Trash\n")

if __name__=="__main__":
	args = argparse.ArgumentParser()
	args.add_argument("--target", default="demo_dir")
	parsed_args = args.parse_args()
	weed_out(TARGET_DIR=parsed_args.target)
