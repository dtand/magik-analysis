import json

def replace_template_params(json, params):
    try:
        with open(json, 'r') as file:
            file_content = file.read()
            for key,value in params.items():
                file_content = file_content.replace(key, value)
            return file_content
    except FileNotFoundError:
        print(f"Error: File not found: {json}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  
    
def create_json_from_template(json, params):
    contents = replace_template_params(json, params)

    with open(json.replace('.json', '.tmp.json'), 'w') as json_file:
        json.dump(contents, json_file, indent=4)