def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            print("Content of the file:")
            print(content)
    except FileNotFoundError:
        print("File not found!")


def write_file(filename, content):
    try:
        with open(filename, 'w') as file:
            file.write(content)
            print("Content successfully written to the file.")
    except IOError:
        print("Error occurred while writing to the file.")


def main():
    filename = "example.txt"
    content_to_write = "Hello, this is some content written into the file!"

    # Write content into file
    write_file(filename, content_to_write)

    # Read content from file
    read_file(filename)


if __name__ == "__main__":
    main()
