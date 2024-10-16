def merge_csv_files(file_paths, output_file):
    with open(output_file, mode='w') as outfile:
        # Flag to track if the header is written
        header_written = False

        for file_path in file_paths:
            with open(file_path, mode='r') as infile:
                if header_written:
                    # Skip the first line (header) for all files except the first one
                    next(infile)
                else:
                    header_written = True  # Ensure header is only written once

                # Write the content of the file to the output file
                outfile.write(infile.read())


if __name__ == '__main__':
    file_paths = [
        '/home/roman/PycharmProjects/personal/diploma/parsers/runnures/obi/data/2024-10-14_13-45_products.csv',
        '/home/roman/PycharmProjects/personal/diploma/parsers/runnures/obi/data/2024-10-15_07-54_products.csv',
        '/home/roman/PycharmProjects/personal/diploma/parsers/runnures/obi/data/2024-10-15_13-47_products.csv',
        '/home/roman/PycharmProjects/personal/diploma/parsers/runnures/obi/data/2024-10-16_00-03_products.csv',
    ]
    output_file = '/home/roman/PycharmProjects/personal/diploma/parsers/runnures/obi/data/products_merged.csv'
    merge_csv_files(file_paths, output_file)
