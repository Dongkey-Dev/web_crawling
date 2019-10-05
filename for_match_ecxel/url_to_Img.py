import os
import urllib.request
import traceback
from urllib.parse import urlparse
from PIL import Image
import pandas as pd
from tqdm import tqdm


StartPoint = 0
EndPoint = 23

src = "/Users/mycelebs_dev/PycharmProjects/web_clowling/190801/searching_missing.xlsx"
print("엑셀 파일 여는중. . .")
df = pd.read_excel(src, sheet_name='searching_missing')
df.columns
row1 = df["cd_idx"]
test_name = ''
count = StartPoint
missing = []

for idx,row in tqdm(df[StartPoint:EndPoint].iterrows(), ascii=True, desc="rolling in the deep"):
    cd_idx = row['cd_idx']
    test_name = row['cd_name']
    try:
        tmp_file = urlparse(row['img_url'].replace('https', 'http')).path.split('/')[-1]
        urllib.request.urlretrieve(row['img_url'].replace('https', 'http'), tmp_file)
        im = Image.open(tmp_file)
        rgb_im = im.convert('RGB')
        rgb_im.save(f'/Users/mycelebs_dev/PycharmProjects/web_clowling/190801/{cd_idx}_00.jpg')
        count = count +1
        os.system(f'rm /Users/mycelebs_dev/PycharmProjects/web_clowling/190801/{tmp_file}')
    except:
        ll = str(row['cd_idx']) + ' ' + row['cd_name']
        missing.append(ll)
        continue

with open("/Users/mycelebs_dev/PycharmProjects/web_clowling/190801/missing_list2.txt","w") as f:
    for item in missing:
        f.write("%s\n" % item)