from class_def import ClassDef, TemplateClass
from intbase import InterpreterBase, ErrorType
from bparser import BParser
from object import ObjectDef
from type_value import TypeManager
# need to document that each class has at least one method guaranteed

# Main interpreter class


class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)
        self.trace_output = trace_output

    # run a program, provided in an array of strings, one string per line of source code
    # usese the provided BParser class found in parser.py to parse the program into lists
    def run(self, program):
        status, parsed_program = BParser.parse(program)
        print(parsed_program)
        if not status:
            super().error(
                ErrorType.SYNTAX_ERROR, f"Parse error on program: {parsed_program}"
            )

        self.__map_template_class(parsed_program)    
        self.__add_all_class_types_to_type_manager(parsed_program)
        self.__map_class_names_to_class_defs(parsed_program)

        # instantiate main class
        self.main_object = self.instantiate(
            InterpreterBase.MAIN_CLASS_DEF
        )

        # call main function in main class; return value is ignored from main
        self.main_object.call_method(
            InterpreterBase.MAIN_FUNC_DEF, [], False
        )

        # program terminates!

    # user passes in the line number of the statement that performed the new command so we can generate an error
    # if the user tries to new an class name that does not exist. This will report the line number of the statement
    # with the new command
    def instantiate(self, class_name):
        if class_name not in self.class_index:
            super().error(
                ErrorType.TYPE_ERROR,
                f"No class named {class_name} found",
            )
        class_def = self.class_index[class_name]
        obj = ObjectDef(
            self, class_def, None, self.trace_output
        )  # Create an object based on this class definition
        return obj

    # returns a ClassDef object
    def get_class_def(self, class_name):
        if class_name not in self.class_index:
            super().error(
                ErrorType.TYPE_ERROR,
                f"No class named {class_name} found",
            )
        return self.class_index[class_name]

    # returns a bool
    def is_valid_type(self, typename):
        return self.type_manager.is_valid_type(typename)

    # returns a bool
    def is_a_subtype(self, suspected_supertype, suspected_subtype):
        return self.type_manager.is_a_subtype(suspected_supertype, suspected_subtype)

    # typea and typeb are Type objects; returns true if the two type are compatible
    # for assignments typea is the type of the left-hand-side variable, and typeb is the type of the
    # right-hand-side variable, e.g., (set person_obj_ref (new teacher))
    def check_type_compatibility(self, typea, typeb, for_assignment=False):
        return self.type_manager.check_type_compatibility(typea, typeb, for_assignment)

    def __map_class_names_to_class_defs(self, program):
        self.class_index = {}
        for item in program:
            if item[0] == InterpreterBase.CLASS_DEF:
                if item[1] in self.class_index:
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f"Duplicate class name {item[1]}",
                    )
                self.class_index[item[1]] = ClassDef(item, self)

    # [class classname inherits superclassname [items]]
    def __add_all_class_types_to_type_manager(self, parsed_program):
        self.type_manager = TypeManager()
        for item in parsed_program:
            if item[0] == InterpreterBase.CLASS_DEF:
                class_name = item[1]
                superclass_name = None
                if item[2] == InterpreterBase.INHERITS_DEF:
                    superclass_name = item[3]
                self.type_manager.add_class_type(class_name, superclass_name)

    def add_declared_template_class(self, declared_template_class_code):
        if declared_template_class_code[0] == InterpreterBase.CLASS_DEF:
                class_name = declared_template_class_code[1]
                superclass_name = None
                self.type_manager.add_class_type(class_name, superclass_name)

        if declared_template_class_code[0] == InterpreterBase.CLASS_DEF:
            if declared_template_class_code[1] in self.class_index:
                super().error(
                    ErrorType.TYPE_ERROR,
                    f"Duplicate template class {declared_template_class_code[1]}",
                )
            self.class_index[declared_template_class_code[1]] = ClassDef(declared_template_class_code, self)

    def __map_template_class(self, program):
        self.template_class_index = {}
        self.template_class_type = {}
        for item in program:
            if item[0] == InterpreterBase.TEMPLATE_CLASS_DEF:
                if item[1] in self.template_class_index:
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f"Duplicate template class name {item[1]}",
                    )
                self.template_class_index[item[1]] = TemplateClass(item, self)

    def add_template_class_type(self, template_class_name, template_class_parameterized_types):
        if template_class_name not in self.template_class_type:
            self.template_class_type[template_class_name] = set()
            self.template_class_type[template_class_name].add(tuple(template_class_parameterized_types))
        else:
            self.template_class_type[template_class_name].add(tuple(template_class_parameterized_types))

    def declared_template_class_exist(self, new_template_class_name, new_template_class_types):
        if new_template_class_name in self.template_class_type:
            if tuple(new_template_class_types) in self.template_class_type[new_template_class_name]:
                return True
        
        return False
    
    def get_template_class_def(self, template_class_name):
        if template_class_name not in self.template_class_index:
            super().error(
                ErrorType.TYPE_ERROR,
                f"No template class named {template_class_name} found",
            )
        return self.template_class_index[template_class_name]


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
    "program.txt"
)  # Provide a valid Brewin program here
interpreter.run(brewin_program)
