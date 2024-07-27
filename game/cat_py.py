import os


def concatenate_files_with_extension(file_extension, output_file):
    current_directory = os.getcwd()
    with open(output_file, "w") as outfile:
        for subdir, _, files in os.walk(current_directory):
            for file in files:
                if file.endswith(file_extension):
                    file_path = os.path.join(subdir, file)
                    with open(file_path, "r") as infile:
                        outfile.write("\n\n\n\n" + file_path + "\n\n\n\n")
                        outfile.write(infile.read())
                        outfile.write(
                            "\n"
                        )  # Add a newline between files for separation


if __name__ == "__main__":
    extension = ".py"  # Change this to your desired file extension
    output_filename = "out.txt"  # Change this to your desired output file name

    concatenate_files_with_extension(extension, output_filename)
