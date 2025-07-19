import os
import humanize


total_size = 0

for root, dirs, files in os.walk('.'):
    for file in files:
        total_size += os.path.getsize(os.path.join(root, file))

# print(humanize.naturalsize(os.path.getsize("test.zip"), True, True))
# print(humanize.naturalsize(total_size, True, True))