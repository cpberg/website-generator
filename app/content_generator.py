from utils.ollama_client import generate_text_with_ollama

class ContentGenerator:
    def __init__(self, website_name, website_type):
        self.website_name = website_name.lower()  # Case insensitive
        self.website_type = website_type.lower()  # Normalize the website type
        self.shared_content = {}
        self.additional_details = {}
        print(f"ContentGenerator initialized for {self.website_name} ({self.website_type})")

    def ask_for_additional_details(self):
        if self.website_type == "business":
            business_type = input(f"What kind of business is {self.website_name}? (e.g., Tech, Retail, etc.): ").lower()
            self.additional_details['business_type'] = business_type
        elif self.website_type == "portfolio":
            portfolio_type = input(f"What kind of portfolio is {self.website_name}? (e.g., Photography, Graphic Design, etc.): ").lower()
            self.additional_details['portfolio_type'] = portfolio_type
        elif self.website_type == "blog":
            blog_topic = input(f"What is the main topic of the {self.website_name} blog? (e.g., Technology, Lifestyle, etc.): ").lower()
            self.additional_details['blog_topic'] = blog_topic

    def generate_homepage(self):
        try:
            self.ask_for_additional_details()  # Ask for more details before generating content
            if self.website_type == "business":
                prompt = f"Write a compelling homepage introduction for {self.website_name}, a {self.additional_details['business_type']} business."
            elif self.website_type == "portfolio":
                prompt = f"Write an engaging homepage for {self.website_name}, showcasing a {self.additional_details['portfolio_type']} portfolio."
            elif self.website_type == "blog":
                prompt = f"Create a homepage introduction for {self.website_name}, a blog about {self.additional_details['blog_topic']}."
            else:
                prompt = f"Create a homepage for {self.website_name}, a {self.website_type} website."
            
            print(f"Generating homepage content for {self.website_name}")
            self.shared_content['homepage'] = generate_text_with_ollama(prompt)
        except Exception as e:
            print(f"Exception: Error generating homepage content: {e}")

    def generate_about(self):
        try:
            if self.website_type == "business":
                prompt = f"Compose an 'About Us' section for {self.website_name}, a {self.additional_details['business_type']} business."
            elif self.website_type == "portfolio":
                prompt = f"Compose an 'About Me' section for {self.website_name}, showcasing {self.additional_details['portfolio_type']} work."
            elif self.website_type == "blog":
                prompt = f"Write an 'About Me' section for {self.website_name}, explaining the focus on {self.additional_details['blog_topic']}."
            else:
                prompt = f"Write an 'About' section for {self.website_name}."
            
            print(f"Generating 'About' content for {self.website_name}")
            self.shared_content['about'] = generate_text_with_ollama(prompt)
        except Exception as e:
            print(f"Exception: Error generating 'About' content: {e}")

    def get_shared_content(self):
        return self.shared_content
