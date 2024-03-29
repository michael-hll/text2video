import yaml

class Utility:
    
    @staticmethod
    def read_yaml_content(file):
        with open(file, 'r') as f:
            data = yaml.safe_load(f)
            return data
    
    @staticmethod    
    def get_api_key(key_file, key):
        data = Utility.read_yaml_content(key_file)
        if key in data.keys():
            return data[key]
        return None
    
    @staticmethod
    def write_line_to_file(file, how='a', line=''):
        with open(file, how) as f:
            f.write(line + '\n')