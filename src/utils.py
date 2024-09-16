import os
from pathlib import Path
import asyncio
import aiohttp
from PIL import Image
from tqdm import tqdm

def sanitize_filename(filename):
    return filename.replace('/', '').replace('\\', '').replace(':', '_')

async def download_image(session, image_link, extraName, save_folder,index,  retries=3, delay=3):
    if not isinstance(image_link, str):
        return
    
    filename = Path(image_link).name
    extraName = sanitize_filename(extraName)
    filename = f"{index}#${Path(filename).stem}#${extraName}{Path(filename).suffix}"
    image_save_path = os.path.join(save_folder, filename)

    if os.path.exists(image_save_path):
        return

    for attempt in range(retries):
        try:
            async with session.get(image_link) as response:
                if response.status == 200:
                    with open(image_save_path, 'wb') as f:
                        f.write(await response.read())
                    print(f"Downloaded: {image_save_path}")  # Confirm successful download
                    return
                elif response.status in [500, 503]:
                    print(f"Server error {response.status} for {image_link}. Retrying...")
                else:
                    print(f"Received status code {response.status} for {image_link}")
        except Exception as e:
            print(f"Error downloading image {image_link}: {e}")
            await asyncio.sleep(delay)

    print(f"Failed to download image: {image_link}")  # Log failed attempts

async def download_images_async(df, download_folder, max_connections=10):
    if not {'index', 'image_link', 'group_id', 'entity_name'}.issubset(df.columns):
        raise KeyError("One or more required columns are missing from the DataFrame")

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    connector = aiohttp.TCPConnector(limit_per_host=max_connections)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for _, row in df.iterrows():
            index = str(row['index'])
            image_link = row['image_link']
            groupId = str(row['group_id'])
            entity_name = str(row['entity_name'])
            # entity_value = str(row['entity_value'])
            extraName = f"{groupId}#${entity_name}"
            
            filename = Path(image_link).name
            extraName = sanitize_filename(extraName)
            filename = f"{index}#${Path(filename).stem}#${extraName}{Path(filename).suffix}"
            # print(filename)
            image_save_path = os.path.join(download_folder, filename)

            if not os.path.exists(image_save_path):
                tasks.append(download_image(session, image_link, extraName, download_folder, index))


        for f in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            await f

# import os
# from urllib import request
# from pathlib import Path
# import time
# from tqdm import tqdm
# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from PIL import Image

# def sanitize_filename(filename):
#     # Replace invalid characters and slashes with underscores
#     return filename.replace('/', '').replace('\\', '').replace(':', '_')

# def download_image(image_link, extraName, save_folder, retries=5, delay=5):
#     if not isinstance(image_link, str):
#         return

#     filename = Path(image_link).name
#     extraName = sanitize_filename(extraName)
#     filename = f"{Path(filename).stem}#${extraName}{Path(filename).suffix}"
#     image_save_path = os.path.join(save_folder, filename)

#     # Skip if image already exists
#     if os.path.exists(image_save_path):
#         return

#     for attempt in range(retries):
#         try:
#             # Attempt to download the image
#             request.urlretrieve(image_link, image_save_path)
#             print(f"Downloaded: {image_save_path}")
#             return
#         except Exception as e:
#             print(f"Error downloading image {image_link}: {e}")
#             time.sleep(delay)
    
#     # If it fails all retries, don't save anything or create a placeholder
#     print(f"Failed to download image after {retries} attempts: {image_link}")

# def download_images(df, download_folder, allow_multiprocessing=True, num_threads=8):
#     if not {'image_link', 'group_id', 'entity_name', 'entity_value'}.issubset(df.columns):
#         raise KeyError("One or more required columns are missing from the DataFrame")

#     # Create the download folder if it doesn't exist
#     if not os.path.exists(download_folder):
#         os.makedirs(download_folder)

#     if allow_multiprocessing:
#         with ThreadPoolExecutor(max_workers=num_threads) as executor:
#             futures = []
#             for _, row in df.iterrows():
#                 image_link = row['image_link']
#                 groupId = str(row['group_id'])
#                 entity_name = str(row['entity_name'])
#                 entity_value = str(row['entity_value']).replace(" ", "_")
#                 extraName = f"{groupId}#${entity_name}#${entity_value}"
                
#                 # Submit the download task
#                 futures.append(executor.submit(download_image, image_link, extraName, download_folder))
                
#             # Wait for all futures to complete
#             for future in tqdm(as_completed(futures), total=len(futures)):
#                 pass
#     else:
#         # Sequential downloading (non-multiprocessing option)
#         for _, row in tqdm(df.iterrows(), total=len(df)):
#             image_link = row['image_link']
#             groupId = str(row['group_id'])
#             entity_name = str(row['entity_name'])
#             entity_value = str(row['entity_value']).replace(" ", "_")
#             extraName = f"{groupId}#${entity_name}#${entity_value}"
            
#             download_image(image_link, extraName, save_folder=download_folder, retries=5, delay=5)

