from interpreterv3 import Interpreter

def read_txt_file(file_path):
    """
    Reads a text file and returns each line as a list of strings.

    Parameters:
        file_path (str): The path to the text file.

    Returns:
        list: A list of strings, where each string is a line from the text file.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


# Testing the interpreter
interpreter = Interpreter()
brewin_program = read_txt_file(
    "/home/mubai/CS131/cs131-project-2/program.txt"
)  # Provide a valid Brewin program here
interpreter.run(brewin_program)