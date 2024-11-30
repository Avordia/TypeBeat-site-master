def parse_beatpack_details(details_file):
    """
    Parses a .txt file containing Beatpack and Beatmap details.

    Args:
        details_file: File object representing the uploaded .txt file.

    Returns:
        A tuple containing:
        - A dictionary of Beatpack data (e.g., beatpack_title, music_author).
        - A list of dictionaries, each representing a Beatmap.

    Raises:
        ValueError: If the file is invalid or contains malformed data.
    """
    print("Starting parsing of Beatpack details...")  # Debug message
    details = details_file.read().decode('utf-8').splitlines()
    print(f"Raw details content:\n{details}")  # Debug message

    beatpack_data = {}
    beatmaps_data = []
    current_section = None
    current_beatmap = {}

    for line in details:
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        print(f"Processing line: {line}")  # Debug message

        if line.startswith("[") and line.endswith("]"):
            # Handle section switch
            section = line[1:-1]
            print(f"Switching to section: {section}")  # Debug message

            if section == "Beatmap" and current_beatmap:
                # Save the previous Beatmap if valid
                if "beatmap_title" not in current_beatmap:
                    raise ValueError("Each [Beatmap] section must have a 'beatmap_title'.")
                beatmaps_data.append(current_beatmap)
                current_beatmap = {}

            current_section = section
            continue

        if current_section == "Beatpack":
            try:
                key, value = map(str.strip, line.split(":", 1))
                print(f"Found Beatpack key-value pair: {key} - {value}")  # Debug message
                beatpack_data[key] = value
            except ValueError:
                raise ValueError(f"Malformed Beatpack line: '{line}'")

        elif current_section == "Beatmap":
            try:
                key, value = map(str.strip, line.split(":", 1))
                print(f"Found Beatmap key-value pair: {key} - {value}")  # Debug message
                current_beatmap[key] = value
            except ValueError:
                raise ValueError(f"Malformed Beatmap line: '{line}'")

    # Add the last Beatmap if it exists
    if current_section == "Beatmap" and current_beatmap:
        if "beatmap_title" not in current_beatmap:
            raise ValueError("Each [Beatmap] section must have a 'beatmap_title'.")
        beatmaps_data.append(current_beatmap)

    print(f"Parsed Beatpack data: {beatpack_data}")  # Debug message
    print(f"Parsed Beatmaps data: {beatmaps_data}")  # Debug message

    # Validate Beatpack data
    required_beatpack_keys = {"beatpack_title", "music_author"}
    missing_keys = required_beatpack_keys - beatpack_data.keys()
    if missing_keys:
        raise ValueError(f"The [Beatpack] section is missing required fields: {', '.join(missing_keys)}")

    print("Finished parsing Beatpack details.")  # Debug message
    return beatpack_data, beatmaps_data

def parse_single_beatmap(details_file):
    """
    Parses a .txt file containing a single Beatmap's details.

    Args:
        details_file: File object representing the uploaded .txt file.

    Returns:
        A dictionary representing the Beatmap details.

    Raises:
        ValueError: If the file is invalid or contains malformed data.
    """
    print("Starting parsing of Beatmap details...")  # Debug message
    details = details_file.read().decode('utf-8').splitlines()
    print(f"Raw details content:\n{details}")  # Debug message

    beatmap_data = {}
    current_section = None

    for line in details:
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        print(f"Processing line: {line}")  # Debug message

        # Check for section headers
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1]
            print(f"Switching to section: {current_section}")  # Debug message
            if current_section != "Beatmap":
                raise ValueError("Invalid section in Beatmap file. Expected [Beatmap].")
            continue

        if current_section == "Beatmap":
            try:
                key, value = map(str.strip, line.split(":", 1))
                print(f"Found Beatmap key-value pair: {key} - {value}")  # Debug message
                beatmap_data[key.lower().replace(" ", "_")] = value  # Normalize keys
            except ValueError:
                raise ValueError(f"Malformed Beatmap line: '{line}'")

    # Validate Beatmap data
    required_beatmap_keys = {"beatmap_title", "difficulty", "no_of_letters", "no_of_spaces"}
    missing_keys = required_beatmap_keys - beatmap_data.keys()
    if missing_keys:
        raise ValueError(f"The Beatmap is missing required fields: {', '.join(missing_keys)}")

    # Convert numeric fields to integers
    try:
        beatmap_data["difficulty"] = int(beatmap_data["difficulty"])
        beatmap_data["no_of_letters"] = int(beatmap_data["no_of_letters"])
        beatmap_data["no_of_spaces"] = int(beatmap_data["no_of_spaces"])
    except ValueError as e:
        raise ValueError(f"Invalid numeric value in Beatmap details: {e}")

    print(f"Parsed Beatmap data: {beatmap_data}")  # Debug message
    print("Finished parsing Beatmap details.")  # Debug message
    return beatmap_data
