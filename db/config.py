from configparser import ConfigParser

# This function loads a configuration file and returns the parameters in
# the specified section as a dictionary.
#
# file_path: The path to the configuration file.  section: The section
# in the configuration file to load.
#
# returns: a dictionary, where the keys are the parameter names and the
# values are the parameter values.
def load_config(file_path: str, section: str) -> dict:
    parser = ConfigParser()
    parser.read(file_path)

    if not parser.has_section(section):
        raise Exception(f"?section {section} not found in the {file_path} file")

    parameters = parser.items(section)
    config = {}

    for p in parameters:
        config[p[0]] = p[1]

    return config
