from configparser import ConfigParser


def load_config(file_path: str, section: str) -> dict:
    parser = ConfigParser()
    parser.read(file_path)

    if not parser.has_section(section):
        raise Exception(
            f'?section {section} not found in the {file_path} file')

    parameters = parser.items(section)
    config = {}

    for p in parameters:
        config[p[0]] = p[1]

    return config
