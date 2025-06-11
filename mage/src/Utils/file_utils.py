import os

def create_file(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            return True
    else:
        return False