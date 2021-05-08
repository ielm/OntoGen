#!/usr/bin/python3
import os
import sys
import time
from   fnmatch import fnmatch


def get_all_python_files(base_dir="tests"):
	test_fns = []
	for root, subdirs, files in os.walk(base_dir):
		for fn in files:
			if fnmatch(fn, "*.py") and not fn.startswith("_"):
				test_fns.append(os.path.join(root, fn))
	# print(test_fns)
	return sorted(test_fns)

if __name__ == "__main__":
	test_fns = get_all_python_files()