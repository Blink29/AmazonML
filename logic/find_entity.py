async def findEntity(image_path, entity_name_key):
    from logic.image_processing import findText
    from logic.constants import entity_name, short_entity

    # Extract text from the image
    imageChar = findText(image_path)
    
    # Get entity units and short forms
    entity_units = entity_name.get(entity_name_key, set())
    short_units = set()
    for unit in entity_units:
        # Add full units
        short_units.add(unit.lower())
        # Check and add short forms if available
        short_units.update({key.lower() for key, value in short_entity.items() if value.lower() == unit.lower()})

    # Normalize the units to lowercase
    entity_units = set(keyword.lower() for keyword in entity_units)
    short_units = set(keyword.lower() for keyword in short_units)
    
    print(f"Entity units: {entity_units}")
    print(f"Short units: {short_units}")

    # Prepare the reduced data map
    reduced_data_map = []
    for key, value in imageChar:
        key_normalized = key.lower().strip()
        if key_normalized in entity_units or key_normalized in short_units:
            reduced_data_map.append([key, value])

    print("find entity map: ", reduced_data_map)

    return reduced_data_map



def findWeightEntity(image_path):
    return findEntity(image_path, 'item_weight')

def findHeightEntity(image_path):
    return findEntity(image_path, 'height')

def findWidthEntity(image_path):
    return findEntity(image_path, 'width')

def findDepthEntity(image_path):
    return findEntity(image_path, 'depth')

def findMaxWeightEntity(image_path):
    return findEntity(image_path, 'maximum_weight_recommendation')

def findVoltageEntity(image_path):
    return findEntity(image_path, 'voltage')

def findWattageEntity(image_path):
    return findEntity(image_path, 'wattage')

def findVolumeEntity(image_path):
    return findEntity(image_path, 'item_volume')

