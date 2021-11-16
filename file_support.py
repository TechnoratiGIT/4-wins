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


def save_list(path, content: list):
    with open(path, "w+") as f:
        f.write("[\n")
        extra = ",\n"
        for i in range(len(content)):
            if i == len(content) - 1:
                extra = "\n"
            f.write(str(content[i]) + extra)
        f.write("]")


def list_to_save_string(list_: list, st=False):
    s = "\n"
    extra = ",\n"
    for i in range(len(list_)):
        if i == len(list_) - 1:
            extra = "\n"
        if isinstance(list_[i], str):
            a = "\"" + list_[i] + "\"" + extra
        else:
            a = str(list_[i]) + extra
        s += a
    if not st:
        return [s]
    else:
        return "[" + s + "]"
