import pandas as pd
df = pd.read_csv('split_dataset/item_weight_classified.csv')
df.head()
import os,sys
import tqdm
import asyncio
from src.utils import download_image,download_images_async

sys.path.append(os.path.abspath('src'))
FolderPath = "train_item_weight_2"
# download_images(df,FolderPath,allow_multiprocessing=True)

def main():
    df = pd.read_csv('dataset/test.csv')  # Replace with your CSV path
    download_folder = 'testing_dataset'
    
    # Properly await the coroutine using asyncio.run()
    asyncio.run(download_images_async(df, download_folder))

if __name__ == '__main__':
    main()