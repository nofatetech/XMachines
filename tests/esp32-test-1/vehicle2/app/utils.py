# app/utils.py

def render_template(template_name, **data):
    """
    A very simple template renderer.
    It reads a template file and replaces {{ key }} placeholders with values from data.
    """
    # In MicroPython, paths might need to be relative to the root
    template_path = f"app/templates/{template_name}"
    try:
        with open(template_path, 'r') as f:
            content = f.read()
    except OSError as e:
        print(f"Error reading template: {e}")
        return "Template not found."

    for key, value in data.items():
        content = content.replace("{{ " + key + " }}", str(value))
    return content
