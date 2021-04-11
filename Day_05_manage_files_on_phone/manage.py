import os
import shutil
import glob

PATH = "11April2021"
files = glob.glob(f"{PATH}/*")
THRESHOLD = 14.0 # 14MB

large_files_dir = os.path.join(PATH, "large_files")
os.makedirs(large_files_dir, exist_ok=True)

large_files_count = 0

for file_ in files:
	file_stat = os.stat(file_)
	size_in_MB = file_stat.st_size / (1024.0)
	if size_in_MB > THRESHOLD:
		src = file_
		dest = large_files_dir
		print(src, dest)
		shutil.move(src, dest)
		large_files_count += 1

print(f"total: {large_files_count} moved to {large_files_dir}")