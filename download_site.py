import subprocess
import shutil
from pathlib import Path

from bs4 import BeautifulSoup

for p in ['wp-contents', 'wp-includes', 'wp-json']:
    path = Path(p)
    if path.exists():
        shutil.rmtree(path)

index = Path('index.html')

if index.exists():
    index.unlink()

subprocess.call(['wget', '-N', '-m', '-p', '-E', '-nH', '-k', '--no-check-certificate', '--no-if-modified-since', 'https://zan.zqf.mybluehost.me'])

with open("index.html") as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

for div in soup.find_all("div", {'class':'av-siteloader-wrap av-transition-enabled av-transition-with-logo'}):
    print("DELETING", str(div))
    div.decompose()

with open("index.html", "w") as f:
    f.write(str(soup))

