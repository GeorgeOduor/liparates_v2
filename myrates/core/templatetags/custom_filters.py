from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Splits the string by the given delimiter."""
    values  = [i for i in value.split(delimiter) if i != '']
    return values

@register.filter
def customDate(value):
    return value.strftime("%Y%m%d")


@register.filter
def associated_files(value):
    """
    Splits a comma-separated string of file paths and creates a dictionary
    mapping the filenames (extracted from the paths) to their full paths.

    Parameters:
    value (str): A string containing comma-separated file paths.

    Returns:
    dict: A dictionary where the keys are filenames and the values are the full paths.
    """
    # Split the input string by commas to get individual file paths
    file_paths = value.split(',')
    
    # Create a dictionary with filenames as keys and full paths as values
    result = {path.split('_')[0]: path for path in file_paths}
        
    return result
        
@register.filter(name='in_list')
def in_list(value, the_list):
    return value in the_list.split(',')