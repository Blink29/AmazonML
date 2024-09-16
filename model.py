import numpy as np
import os
from logic.find_entity import findEntity
from concurrent.futures import ThreadPoolExecutor
import asyncio
from aiofiles import open as aio_open
import random
import csv
from extra import Bounding_box, enhance_image, format_entity_value
import shutil

test_images = 'testing_dataset'
processed_images_folder = 'processed_images'
output_csv_file = 'predictions.csv'
max_concurrent_tasks = 5  # Max number of concurrent tasks

# Semaphore to limit concurrency
semaphore = asyncio.Semaphore(max_concurrent_tasks)

async def process_image_for_entity(image_filename):
    print('filename: ', image_filename)
    try:
        components = image_filename.split("#$")
        # if len(components) != 4:
        #     print(f"Filename format error: {image_filename}")
        #     return None, {}
        index = components[0]
        entity_name = components[3].split('.')[0]
        print("name:  ", entity_name)
        image_path = os.path.join(test_images, image_filename)
        
        # Initialize enhanced_image_path
        enhanced_image_path = None

        # Try to find entity directly
        reduced_data_map = await findEntity(image_path, entity_name)

        if not reduced_data_map:
            # If initial search fails, enhance image and try again
            try:
                enhanced_image_path = await enhance_image(image_path)
                reduced_data_map = await findEntity(enhanced_image_path, entity_name)
            except Exception as e:
                print(f"Error enhancing image: {e}")
                return index, {}

        if reduced_data_map:
            if len(reduced_data_map) >= 2:
                if (entity_name == "width") or (entity_name == "height"):
                    if len(reduced_data_map) == 2:
                        # Use bounding box dimensions
                        bbox_width, bbox_height = await Bounding_box(enhanced_image_path or image_path)
                        if bbox_width == 0 or bbox_height == 0:
                            random_index = random.randint(0, len(reduced_data_map) - 1)
                            selected_unit, selected_value = reduced_data_map[random_index]
                            reduced_data_map = {selected_unit: selected_value}
                            return index, reduced_data_map
                        
                        values = [value for _, value in reduced_data_map]
                        actual_height = max(values)
                        actual_width = min(values)
                        
                        if bbox_width > bbox_height:
                            actual_height, actual_width = actual_width, actual_height
                        
                        if entity_name == "width":
                            known_value = actual_width
                            for unit, value in reduced_data_map:
                                if value == actual_width:
                                    reduced_data_map = {unit: value}
                                    break
                            return index, reduced_data_map
                        else:
                            known_value = actual_height
                            for unit, value in reduced_data_map:
                                if value == actual_height:
                                    reduced_data_map = {unit: value}
                                    break
                            return index, reduced_data_map

                    elif len(reduced_data_map) > 2:
                        bbox_width, bbox_height = await Bounding_box(enhanced_image_path or image_path)
                        if bbox_width == 0 or bbox_height == 0:
                            random_index = random.randint(0, len(reduced_data_map) - 1)
                            selected_unit, selected_value = reduced_data_map[random_index]
                            reduced_data_map = {selected_unit: selected_value}
                            return index, reduced_data_map
                        
                        if entity_name == "width":
                            bbox_ratio = bbox_width / bbox_height
                            closest_ratio = float('inf')
                            closest_value = None
                            closest_unit = None

                            for i, (unit1, value1) in enumerate(reduced_data_map):
                                for j, (unit2, value2) in enumerate(reduced_data_map):
                                    if i != j:
                                        ratio = value1 / value2
                                        ratio_diff = abs(bbox_ratio - ratio)
                                        if ratio_diff < closest_ratio:
                                            closest_ratio = ratio_diff
                                            closest_value = value1
                                            closest_unit = unit1

                            if closest_value is not None:
                                return index, {closest_unit: closest_value}
                            else:
                                return index, {}

                        elif entity_name == "height":
                            bbox_ratio = bbox_height / bbox_width
                            closest_ratio = float('inf')
                            closest_value = None
                            closest_unit = None

                            for i, (unit1, value1) in enumerate(reduced_data_map):
                                for j, (unit2, value2) in enumerate(reduced_data_map):
                                    if i != j:
                                        ratio = value1 / value2
                                        ratio_diff = abs(bbox_ratio - ratio)
                                        if ratio_diff < closest_ratio:
                                            closest_ratio = ratio_diff
                                            closest_value = value1
                                            closest_unit = unit1

                            if closest_value is not None:
                                return index, {closest_unit: closest_value}
                            else:
                                return index, {}

                elif entity_name == "depth":
                    values = [value for _, value in reduced_data_map]
                    depth = min(values)
                    for unit, value in reduced_data_map:
                        if value == depth:
                            reduced_data_map = {unit: value}
                            break
                    return index, reduced_data_map

                elif (entity_name in ["item_weight", "item_volume", "voltage", "wattage"]):
                    random_index = random.randint(0, len(reduced_data_map) - 1)
                    selected_unit, selected_value = reduced_data_map[random_index]
                    reduced_data_map = {selected_unit: selected_value}
                    return index, reduced_data_map

                elif entity_name == "maximum_recommendation_weight":
                    values = [value for _, value in reduced_data_map]
                    depth = max(values)
                    for unit, value in reduced_data_map:
                        if value == depth:
                            reduced_data_map = {unit: value}
                            break
                    return index, reduced_data_map

        else:
            return index, {}
    except Exception as e:
        print(f"Error processing image for entity: {e}")
        return index, {}
    return index, {}
if not os.path.exists(processed_images_folder):
    os.makedirs(processed_images_folder)

async def update_csv(index, prediction, csv_file):
    async with aio_open(csv_file, mode='a', newline='') as f:
        # Access the underlying file object with `_file` and write synchronously
        writer = csv.writer(f._file)
        writer.writerow([index, prediction])

async def move_processed_image(filename, source_folder, destination_folder):
    try:
        shutil.move(os.path.join(source_folder, filename), os.path.join(destination_folder))
    except Exception as e:
        print(f"Error moving file {filename}: {e}")

async def process_image(filename):
    async with semaphore:  # Limit the number of concurrent tasks
        index, reduced_data_map = await process_image_for_entity(filename)
        if index is not None:
            if reduced_data_map:
                print("map is ", reduced_data_map)
                for key, value in reduced_data_map.items():
                    formatted_value = format_entity_value(key, value)  
                    await update_csv(index, formatted_value if formatted_value else "", output_csv_file)
            else:
                await update_csv(index, '', output_csv_file)

            # Ensure the processed_images_folder exists
            if not os.path.exists(processed_images_folder):
                os.makedirs(processed_images_folder)

            # Move the processed image
            
            shutil.move(os.path.join(test_images, filename), os.path.join(processed_images_folder, filename))
                # await move_processed_image(filename, test_images, processed_images_folder)

        else:
            print(f"Skipping file {filename} as no valid index was found.")

async def process_images_in_parallel(image_filenames):
    if not os.path.exists(output_csv_file):
        async with aio_open(output_csv_file, 'w', newline='') as f:
            # Use the `_file` attribute of `f` for writing with csv
            writer = csv.DictWriter(f._file, fieldnames=['Index', 'Prediction'])
            writer.writeheader()

    tasks = [process_image(filename) for filename in image_filenames]
    await asyncio.gather(*tasks)

async def generate_csv_test(test_dataset_folder):
    image_filenames = [f for f in os.listdir(test_dataset_folder) if os.path.isfile(os.path.join(test_dataset_folder, f))]
    await process_images_in_parallel(image_filenames)

if __name__ == "__main__":
    asyncio.run(generate_csv_test(test_images))
