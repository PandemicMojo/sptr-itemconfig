# https://github.com/PandemicMojo/sptr-itemconfig

import json
import os


# Defined functions

# PyInstaller EXE doesn't play nice if I don't do this
#def IsFrozen():
#    if getattr(sys, "frozen", False):
#        return
#
#    file_dir = os.path.dirname(sys.argv[0])
#    
#    try:
#        os.chdir(file_dir)
#    except OSError:  # Fail-safe
#        pass
## None of that shit works. Leaving it in here until I figure it out.

# JSON defs
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
	
def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# ItemID reference point to modify values
def modify_values(data, item_id, changes):
    if item_id in data:
        for key, value in changes.items():
            if key in data[item_id]:
                data[item_id][key] = value
        return True
    else:
        return False

# Recursive file search for string
def search_string_in_directory(directory, search_string):
    found_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            with open(file_path, 'r') as file:
                contents = file.read()
                if search_string in contents:
                    found_files.append(file_path)
    return found_files

# Get current values    
def get_current_values(data, item_id):
    current_values = {}
    for key, value in data[item_id].items():
        current_values[key] = value
    return current_values
	
	
# Main function
def main():
    # Check if script is running from templates folder
    if os.path.basename(os.getcwd()) != "templates":
        print("Error: This script must be run from the templates folder! Please verify that you are running it in '(SPT Server)/user/mods/SPT-Realism-Mod-Server/db/templates'")
        
    # Variables
    script_directory = os.getcwd()
    search_string = input("Enter the item ID string: ")
    found_files = search_string_in_directory(script_directory, search_string)
	
    # Search for the string
    if not found_files:
        print("Item ID not found! Please verify ID or run spt-iteminfo in the Aki_Data folder instead.")
        return
		
    print("Item ID is valid.")
    for file_path in found_files:
        print(file_path)
	
    # Load file from found_files
    first_found_file = found_files[0]
    data = load_data(first_found_file)
	
    # Verify ItemID and print basic info
    if search_string in data:
        item_id = search_string
        print("Name:", data[item_id]["Name"])
    else:
        print("ItemID not found. If you're seeing this, your SPTRealism may be corrupted.")
        return
    
    # Confirmation
    confirmation = input("Do you want to modify this item? (yes/no): ").lower()
    if confirmation != "yes":
        print("Modification cancelled.")
        return
        
    # Variable
    original_values = get_current_values(data, item_id)
    
    # Print the values table once after confirmation (could NOT find a cleaner way to do this sadly)
    print("\nEditable values:")
    current_values = get_current_values(data, item_id)
    for key, value in current_values.items():
        original_value = original_values.get(key, "N/A")
        if original_value != value:
            print(f"{key}: {value} (Original: {original_value}) [Modified]")
        else:
            print(f"{key}: {value}")
        
    edited_values = {}
    
    # The editable values list and edit script (this one blew dick to write)
    while True:
    
        # Loop that references editable_values_printed to ensure we don't print a new table every fucking time
        print("\nType 'done' to finish editing.")
        
        key_to_edit = input("\nChoose which value to edit (or type 'done'): ")
        if key_to_edit.lower() == 'done':
            break
            
        if key_to_edit not in current_values:
            print("Invalid value. Please choose from the list.")
            continue    
        
        # Prints original and current values once item is selected
        original_value = original_values.get(key_to_edit, "N/A")
        current_value = current_values[key_to_edit]
        print(f"\nOriginal Value: {original_value}")
        print(f"Current Value: {current_value}")
        
        new_value = input(f"Enter the new value for {key_to_edit}: ")
        edited_values[key_to_edit] = (original_value, new_value)
        
        # The actual value modification code
        success = modify_values(data, item_id, {key_to_edit: new_value})
	
	
        if success:
            print(f"Value for {key_to_edit} updated successfully.")
            
            # Checks current_values against original_values to show what values have been changed from & prints table
            print("\nEditable values:")
            current_values = get_current_values(data, item_id)
            for key, value in current_values.items():
                original_value = original_values.get(key, "N/A")
                if original_value != value:
                    print(f"{key}: {value} (Original: {original_value}) [Modified]")
                else:
                    print(f"{key}: {value}")
                    
            save_data(first_found_file, data)
            current_values[key_to_edit] = new_value         
        else:
            print("Failed to update values.")
        
if __name__ == "__main__":
    main()