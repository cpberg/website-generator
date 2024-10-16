from website import Website
from theme_manager import ThemeManager
import ollama

def generate_website_content(website_name, website_type, website_description=""):
    """
    Use Ollama to generate full website content based on the website name, type, and description.
    """
    prompt = f"Generate all the content for a {website_type} website called '{website_name}'. " \
             f"Include sections like homepage, about us, services (if applicable), contact us, and any other relevant sections. " \
             f"Here is the description of the website: {website_description}"

    # Use Ollama to generate the content
    response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])

    # Extract the generated content
    content = response["message"]["content"]
    print(f"AI-generated content for {website_name}:")
    print(content)

    return content

def main():
    print("Welcome to the Website Generator.")

    # Get user input for website details
    website_name = input("Please enter the website name: ").strip()
    website_type = input("What type of website is this (e.g., blog, business, portfolio)? ").strip().lower()
    website_description = input("Please provide a brief description of the website (optional): ").strip()

    # Ask user for the desired stack(s)
    stacks_input = input("Please enter the website stack(s) (e.g., 'hugo', 'next.js', or 'all' for all stacks): ").strip().lower().split(",")
    supported_stacks = ["hugo", "next.js"]
    stacks = supported_stacks if "all" in stacks_input else [stack.strip() for stack in stacks_input if stack.strip() in supported_stacks]

    if not stacks:
        print("No valid stacks selected. Exiting.")
        return

    # Generate full content using Ollama
    generated_content = generate_website_content(website_name, website_type, website_description)

    # Process each selected stack (Hugo, Next.js)
    for stack in stacks:
        print(f"Processing stack: {stack}")
        website = Website(stack=stack, website_name=website_name, shared_content=generated_content)

        # Check if the website is already initialized
        if website.is_website_initialized():
            action = input(f"The {stack} website is already initialized. Do you want to 'reset' or 'modify' the {stack} website? ").strip().lower()
            if action == "reset":
                website.initialize_stack(reset=True)  # Reinitialize the website stack
            elif action == "modify":
                print(f"Modifying {stack} website with AI-generated content...")
                website.modify_website()  # Apply the generated content to the website
            else:
                print(f"Unknown action: {action} for {stack}. Skipping.")
                continue
        else:
            website.initialize_stack()  # Initialize the website stack with generated content

        # Theme management options
        manage_theme = input(f"Would you like to change the theme for {stack}? (yes/no): ").strip().lower()
        if manage_theme == "yes":
            theme_manager = ThemeManager(stack, website.website_name)
            theme_manager.get_current_theme()  # Display current theme
            new_theme = input(f"Please enter the new theme for {stack}: ").strip()
            theme_manager.initialize_theme(new_theme)
            theme_manager.change_theme(new_theme)

    print("Website generation complete.")

if __name__ == "__main__":
    main()
