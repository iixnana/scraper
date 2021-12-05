import os
from helpers.file_io import read_text_file

art = ""
for line in read_text_file("./configurations/art.txt"):
    art += line
print(art)

os.makedirs("./results/categorized", exist_ok=True)
#oda().start_crawling()