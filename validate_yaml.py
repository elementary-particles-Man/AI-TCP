import os
import sys
import re
import yaml

SCHEMA_PATHS = [
    os.path.join('structured_yaml', 'schemas', 'master_schema_v1.yaml'),
    os.path.join('structured_yaml', 'master_schema_v1.yaml')
]

for p in SCHEMA_PATHS:
    if os.path.exists(p):
        MASTER_SCHEMA = p
        break
else:
    print('Master schema not found.', file=sys.stderr)
    sys.exit(1)

with open(MASTER_SCHEMA, 'r', encoding='utf-8') as f:
    MASTER_DATA = yaml.safe_load(f)

SCHEMA = MASTER_DATA.get('structure', {})

RE_DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')

def validate_node(data, schema, path=''):
    errors = []
    if isinstance(schema, dict):
        if not isinstance(data, dict):
            errors.append(f'{path or "."} should be mapping')
            return errors
        for key, sub in schema.items():
            if key not in data:
                errors.append(f'{path}{key} missing')
            else:
                errors.extend(validate_node(data[key], sub, f'{path}{key}.'))
    elif isinstance(schema, list):
        if not isinstance(data, list):
            errors.append(f'{path[:-1]} should be list')
        else:
            sub = schema[0]
            for i, item in enumerate(data):
                errors.extend(validate_node(item, sub, f'{path}[{i}].'))
    else:
        if schema == 'string' or schema == 'YYYY-MM-DD':
            if not isinstance(data, str):
                errors.append(f'{path[:-1]} should be string')
            elif schema == 'YYYY-MM-DD' and not RE_DATE.match(data):
                errors.append(f'{path[:-1]} should match YYYY-MM-DD')
        elif schema.startswith('[') and schema.endswith(']'):
            if not isinstance(data, list) or not all(isinstance(x, str) for x in data):
                errors.append(f'{path[:-1]} should be list of strings')
    return errors

def check_required_sections(data):
    required = ['meta', 'header', 'body']
    return [s for s in required if s not in data]

def validate_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f'YAML parse error: {e}']

    errors = []
    missing = check_required_sections(data)
    if missing:
        errors.append(f'Missing sections: {", ".join(missing)}')

    schema_errors = validate_node(data, SCHEMA)
    errors.extend(schema_errors)
    return errors

def main():    base_dir = os.path.join('structured_yaml', 'validated_yaml')    ok_files = []    err_list = []    for fname in sorted(os.listdir(base_dir)):        if not fname.endswith('.yaml'):            continue        path = os.path.join(base_dir, fname)        errs = validate_file(path)        if errs:            err_list.append((fname, errs))        else:            ok_files.append(fname)    print('Validation Results:')    print('\nSuccessful files:')    for f in ok_files:        print(f' - {f}')    print('\nErrors:')    for f, errs in err_list:        for e in errs:            print(f' - {f}: {e}')    if err_list:        sys.exit(1)if __name__ == '__main__':    main()
