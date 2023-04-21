import os
import uuid

# Define constants for file extensions and directories
VIDEO_EXTENSIONS = (".mp4", ".avi", ".mov")
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif")
DIRECTORIES = {
    "videos": os.path.join(os.getcwd(), "videos"),
    "images": os.path.join(os.getcwd(), "images"),
}

# Define a function to handle sorting of files
def sort_files():
    # Initialize a dictionary to store the file types and their counts
    file_type_count = {}

    # Loop through all files in the directory and rename/move them
    for directory in [os.getcwd(), *DIRECTORIES.values()]:
        for filename in os.listdir(directory):
            if filename.endswith((".txt", ".py")):
                continue

            extension = os.path.splitext(filename)[1]

            if extension in VIDEO_EXTENSIONS:
                destination = DIRECTORIES["videos"]
            elif extension in IMAGE_EXTENSIONS:
                destination = DIRECTORIES["images"]
            else:
                continue

            # Generate a new filename using a UUID
            new_filename = str(uuid.uuid1()) + extension
            new_path = os.path.join(destination, new_filename)

            # Move the file to the appropriate destination directory
            os.rename(os.path.join(directory, filename), new_path)

            # Update the file type count
            file_type_count[extension] = file_type_count.get(extension, 0) + 1

    # Read the existing content of the rename file, if it exists
    existing_content = {}
    if os.path.isfile("count.txt"):
        with open("count.txt", "r") as f:
            for line in f:
                try:
                    extension, count = line.strip().split(" = ")
                    existing_content[extension] = int(count)
                except ValueError:
                    continue

    # Update the existing file type counts with the new counts
    for extension, count in file_type_count.items():
        existing_content[extension] = existing_content.get(extension, 0) + count

    # Write the updated file type count to the rename file in list format
    with open("count.txt", "w") as f:
        f.write("[\n")
        for extension, count in sorted(existing_content.items()):
            f.write(f"    {extension} = {count}\n")
        f.write("]\n")

    print("Sorting completed successfully!")

# Define a function to handle counting of files
def count_files():
    # Initialize a dictionary to store the file types and their counts
    file_type_count = {}

    # Loop through all files in the directory and count the file types
    for directory in [os.getcwd(), *DIRECTORIES.values()]:
        for filename in os.listdir(directory):
            extension = os.path.splitext(filename)[1]

            if extension in (".txt", ".py"):
                continue

            if extension in VIDEO_EXTENSIONS or extension in IMAGE_EXTENSIONS:
                file_type_count[extension] = file_type_count.get(extension, 0) + 1

    # Print the file type counts
    print("File type counts:")
    for extension, count in sorted(file_type_count.items()):
        print(f"{extension}: {count}")

# Define the main function that handles user input
def main():
    while True:
        # Get user input and convert to lowercase
        cmd = input("Enter command (sort, count, close): ").lower()

        if cmd == "sort":
            sort_files()
        elif cmd == "count":
            count_files()
        elif cmd == "close":
            print("Goodbye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()