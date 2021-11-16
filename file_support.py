import json
import bugfixing_help as bh


def get_content(path, print_content=False):
    """
    :param print_content: to bugfix and find errors
    :param path: the path to the file (with filename)
    :return: the content of the file
    """
    with open(path, "r") as f:
        content_string = f.read()
    if print_content:
        print(content_string)
    return json.loads(content_string)


def save_content(path, content):
    with open(path, "w+") as f:
        f.write(json.dumps(content))
