import os
import io
import sys
import zipfile


folder_dir = r"C:\Users\SKRR6773\Downloads\nssm-2.24"

with io.BytesIO()as tmp:
    with zipfile.ZipFile(tmp, 'w')as zf:

        for root, dirs, files in os.walk(folder_dir):
            for file in files:
                filePath = os.path.join(root, file)
                zf.write(filePath, os.path.relpath(filePath, folder_dir))


    tmp.seek(0)
    # print(tmp.read())

    sys.stdout.buffer.write(tmp.read())