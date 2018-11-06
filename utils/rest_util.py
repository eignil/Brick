#

'''
Utils for Swagger
'''
from flex.core import validate_api_call
from genson import SchemaBuilder
from jsonpath_ng.ext import parse as parse_jsonpath
from jsonschema import Draft4Validator, FormatChecker
from jsonschema.exceptions import ValidationError


def assert_spec(spec, response):
    request = response.request
    try:
        validate_api_call(spec, raw_request=request, raw_response=response)
    except ValueError as e:
        raise AssertionError(e)

def validate_schema(self, schema, json_dict):
    for field in schema:
        self.assert_schema(schema[field], json_dict[field])

def assert_schema(schema, reality):
    try:
        schema_version = schema['version']
        if schema_version == 'draft04':
            validator = Draft4Validator(schema,
                format_checker=FormatChecker())
        else:
            raise RuntimeError("Unknown JSON Schema version " +
                "was given:\n%s" % (schema_version))
        validator.validate(reality)
    except ValidationError as e:
        raise AssertionError(e)

def new_schema(value):
    builder = SchemaBuilder(schema_uri=False)
    builder.add_object(value)
    return builder.to_schema()

def generate_schema_examples(schema, response):
    body = response['body']
    schema = schema['response']['body']
    if isinstance(body, (dict)):
        for field in body:
            schema['properties'][field]['example'] = body[field]
    elif isinstance(body, (list)):
        schema['example'] = body

def find_by_field(instance, field, return_schema=True, print_found=True):
    last_instance = instance
    schema = None
    paths = []
    if field.startswith("$"):
        value = last_instance['response']['body']
        if return_schema:
            schema = last_instance['schema']['response']['body']
        if field == "$":
            paths = []
        else:
            try:
                query = parse_jsonpath(field)
            except Exception as e:
                raise RuntimeError("Invalid JSONPath query '%s':\n%s" % (
                    field, e))
            matches = [str(match.full_path) for match in query.find(value)]
            if not matches:
                raise AssertionError("JSONPath query '%s' " % (field) +
                    "did not match anything.")
            for match in matches:
                path = match.replace("[", "").replace("]", "").split('.')
                paths.append(path)
    else:
        value = last_instance
        if return_schema:
            schema = last_instance['schema']
        path = field.split()
        paths.append(path)
    return [find_by_path(field, path, value, schema, print_found)
            for path in paths]


def find_by_path(self, field, path, value, schema=None, print_found=True):
    for key in path:
        try:
            value = value_by_key(value, key)
        except (KeyError, TypeError):
            if print_found:
                self.log_json(value,
                    "\n\nProperty '%s' does not exist in:" % (key))
            raise AssertionError(
                "\nExpected property '%s' was not found." % (field))
        except IndexError:
            if print_found:
                self.log_json(value,
                    "\n\nIndex '%s' does not exist in:" % (key))
            raise AssertionError(
                "\nExpected index '%s' did not exist." % (field))
        if schema:
            schema = self._schema_by_key(schema, key, value)
    found = {
        'path': path,
        'reality': value,
        'schema': schema
    }
    return found

def value_by_key(json, key):
    try:
        return json[int(key)]
    except ValueError:
        return json[key]

def schema_by_key(schema, key, value):
    if 'properties' in schema:
        schema = schema['properties']
    elif 'items' in schema:
        if isinstance(schema['items'], (dict)):
            schema['items'] = [schema['items']]
        new_schema = new_schema(value)
        try:
            return schema['items'][schema['items'].index(new_schema)]
        except ValueError:
            schema['items'].append(new_schema)
            return schema['items'][-1]
    if key not in schema:
        schema[key] = new_schema(value)
        
        schema[key]['example'] = value
    return schema[key]
