import hashlib

# import ssdeep
import pefile
import tlsh
import sys
import os
import pyperclip
from pynput import keyboard


def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def calculate_sha1(file_path):
    hash_sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()


def calculate_sha256(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


# def calculate_ssdeep(file_path):
#     return ssdeep.hash_from_file(file_path)


def calculate_imphash(file_path):
    pe = pefile.PE(file_path)
    return pe.get_imphash().lower()


def calculate_tlsh(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return tlsh.hash(data).lower()


def on_press(key, clipboardtext):
    if key == keyboard.Key.enter:
        print("Exiting...")
        sys.exit(0)
    try:
        k = key.char
    except:
        k = key.name
    if k in ["c"]:
        pyperclip.copy(clipboardtext)
        print("Hashes copied to clipboard!")
    # else:
    #     print(f"Key pressed: {k}")


def main(file_path):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"File: {file_path}")
    print("MD5, SHA1, SHA256, Imphash, TLSH")
    md5 = calculate_md5(file_path)
    sha1 = calculate_sha1(file_path)
    sha256 = calculate_sha256(file_path)
    imphash = calculate_imphash(file_path)
    tlsh = calculate_tlsh(file_path)
    hashes = f"{md5}\n{sha1}\n{sha256}\n{imphash}\n{tlsh}"
    print(f"{md5}\n{sha1}\n{sha256}\n{imphash}\n{tlsh}")
    # print(f"ssdeep: {calculate_ssdeep(file_path)}")

    print("\n\nPRESS ENTER KEY TO EXIT, C TO COPY HASHES TO CLIPBOARD")
    listener = keyboard.Listener(on_press=lambda event: on_press(event, hashes))
    listener.start()  # start to listen on a separate thread
    try:
        listener.join()  # remove if main thread is polling self.keys
    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        sys.stdin.readline()  # flush the stdin


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hash_calculator.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
