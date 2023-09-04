import os
from tronpy.keys import PrivateKey
import random
import string
import shutil
import sys

count = 0
target_address = "TXgmLv00E4B7EZwij5rJVcdsgR1BRo16gfo"
max_file_size = 5 * 1024 * 1024  # 5 MB
max_total_size = 2 * 1024 * 1024 * 1024  # 2 TB
output_directory = "adresses"
delete_directory = "delete"

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def create_new_output_file():
    random_string = generate_random_string(10)
    output_filename = f"{random_string}.txt"
    output_path = os.path.join(output_directory, output_filename)
    return output_path

def move_file_to_delete_directory(file_path):
    filename = os.path.basename(file_path)
    delete_path = os.path.join(delete_directory, filename)
    shutil.move(file_path, delete_path)

output_path = create_new_output_file()
output_file = open(output_path, "a")
output_file_size = os.path.getsize(output_path)
total_file_size = output_file_size

while True:
    count += 1
    private_key = PrivateKey.random()
    address = private_key.public_key.to_base58check_address()

    output = f"Count: {count}, Private Key: {private_key}, Address: {address}\n"
    output_size = len(output)

    # Check if the current output file plus the new output exceeds the maximum file size
    if output_file_size + output_size >= max_file_size:
        output_file.close()
        total_file_size += os.path.getsize(output_path)

        if total_file_size >= max_total_size:
            move_file_to_delete_directory(output_path)
            os.execv(sys.executable, ['python'] + sys.argv)  # Restart the program
            break

        move_file_to_delete_directory(output_path)
        output_path = create_new_output_file()
        output_file = open(output_path, "a")
        output_file_size = 0

    output_file.write(output)
    output_file_size += output_size

    if address == target_address:
        gotcha = f"Gotcha!!\nCount: {count}, Private Key: {private_key}, Address: {address}\n"
        gotcha_filename = f"gotcha-{count}.txt"
        gotcha_path = os.path.join(output_directory, gotcha_filename)
        with open(gotcha_path, "a") as gotcha_file:
            gotcha_file.write(gotcha)
        break

output_file.close()
print(f"Process completed. Total number of steps: {count}")