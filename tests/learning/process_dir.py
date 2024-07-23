import os


def process_dir(input_dir: str, output_dir: str) -> None:
    for root, dirs, files in os.walk(input_dir):
        relative_path = os.path.relpath(root, input_dir)
        output_root = os.path.join(output_dir, relative_path)

        if not os.path.exists(output_root):
            os.makedirs(output_root)

        # Process files
        for file_name in files:
            input_file_path = os.path.join(root, file_name)
            output_file_path = os.path.join(output_root, file_name)

            with open(output_file_path, "w") as o_file:
                with open(input_file_path, "r") as i_file:
                    o_file.write(i_file.read())


if __name__ == "__main__":
    process_dir("input_folder", "output_folder")
