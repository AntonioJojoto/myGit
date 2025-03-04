import argparse

# Define the argparser for all the implemented functions
def define_argparser():
    # Define the arguments used when calling mygit, description is shown when --help
    argparser = argparse.ArgumentParser(description="Antonio Content tracker")

    # Extents the argparser by adding subparsers
    # The commands show
    argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
    argsubparsers.required = True   # Makes mandatory to add subparsers

    # Creates a new argparser for the init command
    argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")
    argsp.add_argument("path",
                       metavar="directory",
                       nargs="?",
                       default=".",
                       help="Where to create the repository.")

    # Subparser for cat file command
    # mygit cat-file TYPE OBJECT
    argsp = argsubparsers.add_parser("cat-file",
                                     help="Provide content of repository objects")

    argsp.add_argument("type",
                       metavar="type",
                       choices=["blob", "commit", "tag", "tree"],
                       help="Specify the type")

    argsp.add_argument("object",
                       metavar="object",
                       help="The object to display")

    # Subparser for the has-object command

    # return the final argparser object
    return argparser

