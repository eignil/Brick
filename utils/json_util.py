from json import dumps, load, loads
from yaml import load as load_yaml
from os import path, getcwd

import print_util


def beauty_json(json_data):
    json_str = dumps(json_data,indent=4)
    return json_str


def load_json(file_path):
    with open(file_path,'r') as f:
        jdata = load(f)
        return jdata

def print_json(json_data):
    print_util.print_std(beauty_json(json_data))



def input_boolean(value):
    '''
    Convert a json bool value to python bool value.
    '''
    if isinstance(value, (bool)):
        return value
    try:
        json_value = loads(value)
        if not isinstance(json_value, (bool)):
            raise TypeError("This is not a Python boolean: %s" % (json_value))
    except (ValueError, TypeError):
        raise RuntimeError("This is not a JSON boolean:\n%s" % (value))
    return json_value

def input_string(value):
    if value == "":
        return ""
    if isinstance(value, str):
        if not value.startswith('"'):
            value = '"' + value
        if not value.endswith('"'):
            value = value + '"'
    try:
        json_value = loads(value)
        if not isinstance(json_value, str):
            raise TypeError("This is not a Python string: %s" % (
                json_value))
    except (ValueError, TypeError):
        raise RuntimeError("This is not a JSON string:\n%s" % (value))
    return json_value

def input_object(value):
    if isinstance(value, (dict)):
        return value
    if path.isfile(value):
        json_value = input_json_from_file(value)
    else:
        try:
            json_value = loads(value)
            if not isinstance(json_value, (dict)):
                 raise TypeError("This is not a Python dict: %s" % (json_value))
        except (ValueError, TypeError):
            raise RuntimeError("This is neither a JSON object, " + 
                "nor a path to an existing file:\n%s" % (value))
    return json_value




def input_array(value):
    if isinstance(value, (list)):
        return value
    if path.isfile(value):
        json_value = input_json_from_file(value)
    else:
        try:
            json_value = loads(value)
            if not isinstance(json_value, (list)):
                raise TypeError("This is not a Python list: %s" % (
                json_value))
        except (ValueError, TypeError):
            raise RuntimeError("This is not a JSON array:\n%s" % (
                value))
    return json_value

def input_json_from_file(path):
    try:
        with open(path, encoding="utf-8") as file:
            return load(file)
    except IOError as e:
        raise RuntimeError("File '%s' cannot be opened:\n%s" % (
            path, e))
    except ValueError as e:
        try:
            with open(path, encoding="utf-8") as file:
                return load_yaml(file)
        except ValueError:
            raise RuntimeError("File '%s' is not valid JSON or YAML:\n%s" %
                (path, e))

def input_timeout(value):
    if isinstance(value, (int, float)):
        return [value, value]
    if isinstance(value, (list)):
        if len(value) != 2:
            raise RuntimeError("This timeout, given as a Python list, " +
                "must have length of 2:\n%s" % (value))
        return value
    try:
        value = loads(value)
        if not isinstance(value, (int, float, list)):
            raise TypeError("This is not a Python integer, " +
                "float or a list:\n%s" % (value))
    except (ValueError, TypeError):
        raise RuntimeError("This timeout must be either a JSON integer, " +
            "number or an array:\n%s" % (value))
    if isinstance(value, (list)):
        if len(value) != 2:
            raise RuntimeError("This timeout, given as a JSON array, " +
                "must have length of 2:\n" % (value))
        else:
            return value
    return [value, value]

def input_json_as_string(string):
        return loads(string)


def input_json_from_non_string(value):
    try:
        return input_json_as_string(dumps(value, ensure_ascii=False))
    except ValueError:
        raise RuntimeError("This Python value " +
            "cannot be read as JSON:\n%s" % (value))

def input(what):
    if what is None:
        return None
    if not isinstance(what, str):
        return input_json_from_non_string(what)
    if path.isfile(what):
        return input_json_from_file(what)
    try:
        return input_json_as_string(what)
    except ValueError:
        return input_string(what)

def output(self, what="", file_path=None, append=False,
           sort_keys=False):
    message = "\n%s as JSON is:" % (what.__class__.__name__)
    if what == "":
        message = "\n\nThe current instance as JSON is:"
        try:
            json = self._last_instance_or_error()
        except IndexError:
            raise RuntimeError(no_instances_error)
    elif isinstance(what, (str)):
        try:
            json = loads(what)
        except ValueError:
            self._last_instance_or_error()
            message = "\n\n%s as JSON is:" % (what)
            matches = self._find_by_field(what, return_schema=False)
            if len(matches) > 1:
                json = [found['reality'] for found in matches]
            else:
                json = matches[0]['reality']
    else:
        json = what
    sort_keys = input_boolean(sort_keys)
    if not file_path:
        self.log_json(json, message, sort_keys=sort_keys)
    else:
        content = dumps(json, ensure_ascii=False, indent=4,
                        separators=(',', ': ' ), sort_keys=sort_keys)
        write_mode = 'a' if input_boolean(append) else 'w'
        try:
            with open(path.join(getcwd(), file_path), write_mode,
                      encoding="utf-8") as file:

                file.write(content)
        except IOError as e:
            raise RuntimeError("Error outputting to file '%s':\n%s" % (
                file_path, e))
    return json


if __name__ == '__main__':
    pass
