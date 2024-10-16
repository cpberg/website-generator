import ollama

def generate_text_with_ollama(prompt):
    response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def replace_theme_with_ai(stack, config_file, new_theme):
    with open(config_file, 'r') as file:
        config_content = file.read()

    prompt = f"""
    You are an expert in web development. You have the following configuration file:
    {config_content}
    Your task is to identify where the current theme is set, and replace it with the new theme: {new_theme}.
    Please return the updated configuration file with the theme changed accordingly.
    """
    response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])
    updated_config = response['message']['content']

    with open(config_file, 'w') as file:
        file.write(updated_config)

    print(f"Theme successfully updated in {config_file}.")

