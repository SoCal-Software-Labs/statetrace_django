import time


def new_id():
	return int(time.monotonic() * 1000000) % 2147483647