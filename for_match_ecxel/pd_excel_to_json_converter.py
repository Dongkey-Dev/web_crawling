import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    df = pd.read_excel(os.path.join(BASE_DIR, 'Geewon_.xlsx'))
    df['seq'] = 1
    for i in df.index:
        df.loc[i].to_json(os.path.join(BASE_DIR, "cook_" + str(df.loc[i]['cd_idx']) + ".json"))