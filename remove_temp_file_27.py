import os
file_to_remove = "D:/Dev/AI-TCP/remove_temp_file_26.py"
if os.path.exists(file_to_remove):
    os.remove(file_to_remove)
    print(f"Removed {file_to_remove}")
else:
    print(f"{file_to_remove} does not exist.")