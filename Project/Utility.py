
def check_attributes(obj, value):
    field_names = []
    for attr_name, attr_value in vars(obj).items():
        if isinstance(attr_value, str) and attr_value == value:
            field_names.append(attr_name)
        elif not isinstance(attr_value, str) and hasattr(attr_value, '__dict__'): 
            found_field_names = check_attributes(attr_value, value)
            for found_field_name in found_field_names:
                field_names.append(f'{attr_name}.{found_field_name}')
    return field_names

def get_nested_attribute(obj, attr_name):
    attrs = attr_name.split('.')
    for attr in attrs:
        obj = getattr(obj, attr)
    return obj

def set_nested_attr(obj, field_list, value):
    if len(field_list) > 1:
        next_field = field_list.pop(0)
        if not hasattr(obj, next_field):
            raise AttributeError(f"Object of type '{type(obj).__name__}' has no field '{next_field}'")
        set_nested_attr(getattr(obj, next_field), field_list, value)
    else:
        setattr(obj, field_list[0], value)
