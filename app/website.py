import os
import subprocess  # This import was missing earlier
import sys
import toml  # To handle .toml configuration files for Hugo
import json  # To handle .json configuration files for Next.js

# Base directory where websites are stored
BASE_DIR = "/mnt/sites"

class Website:
    def __init__(self, stack, website_name, shared_content):
        """
        Initialize the Website object with the stack, website_name, and shared content.
        The initializer method will handle stack initialization if necessary.
        """
        self.stack = stack
        self.website_name = website_name.lower().replace(" ", "-")  # Convert to kebab-case for directory naming
        self.shared_content = shared_content
        self.config_file = None  # This will hold the reference to the config file

    def get_config_file(self):
        """
        Determine the appropriate config file based on the stack type and set the config_file attribute.
        """
        website_dir = f"{BASE_DIR}/{self.stack}/{self.website_name}"

        if not os.path.exists(website_dir):
            raise FileNotFoundError(f"Website directory not found: {website_dir}")

        # Determine config file for Hugo, Next.js, or other stacks
        if self.stack == "hugo":
            config_file = os.path.join(website_dir, "hugo.toml")
        elif self.stack == "next.js":
            config_file = os.path.join(website_dir, "package.json")
        else:
            raise ValueError(f"Unsupported stack: {self.stack}")

        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")

        self.config_file = config_file
        print(f"Config file set to {self.config_file} for {self.stack}.")
        return config_file

    def is_website_initialized(self):
        """
        Check if the stack is already initialized by validating the presence of key files and directories.
        """
        try:
            self.get_config_file()  # This will set the config_file if it exists
            print(f"{self.stack} is already initialized for {self.website_name}.")
            return True
        except FileNotFoundError:
            return False

    def initialize_stack(self, reset=False):
        """
        Initialize the website stack based on the stack type using subprocess.
        If reset=True, the stack will be re-initialized.
        """
        website_dir = f"{BASE_DIR}/{self.stack}/{self.website_name}"

        try:
            # Check if the directory exists and is not empty
            if os.path.exists(website_dir) and os.listdir(website_dir):
                if reset:
                    print(f"Resetting {self.stack} at {website_dir}...")
                    subprocess.run(["rm", "-rf", website_dir], check=True)
                else:
                    # Prompt the user for an action if directory exists and is not empty
                    choice = input(f"The directory '{website_dir}' already exists and is not empty. Would you like to reset (1) or skip (2)? ")
                    if choice == "1":
                        print(f"Resetting {self.stack} at {website_dir}...")
                        subprocess.run(["rm", "-rf", website_dir], check=True)
                    else:
                        print(f"Skipping initialization for {self.stack}.")
                        return

            if self.stack == "hugo":
                print(f"Initializing Hugo site at {website_dir}...")
                subprocess.run(["hugo", "new", "site", website_dir], check=True)

            elif self.stack == "next.js":
                print(f"Initializing Next.js app at {website_dir} using npx...")
                subprocess.run(["npx", "create-next-app", website_dir], check=True)

            else:
                raise ValueError(f"Unsupported stack: {self.stack}")

            # After initialization, set the config_file reference
            self.get_config_file()

        except subprocess.CalledProcessError as e:
            print(f"Error initializing {self.stack}: {e}")
            sys.exit(1)  # Gracefully exit on error

    def initializer(self, reset=False):
        """
        Main initializer method. Checks if the website needs to be initialized and performs the action if necessary.
        If reset is True, the stack will be re-initialized.
        """
        if not self.is_website_initialized():
            print(f"{self.stack} is not initialized for {self.website_name}. Initializing now...")
            self.initialize_stack(reset=reset)
        else:
            # Prompt user if they want to generate new content or reset the stack
            choice = input(f"{self.stack} is already initialized. Would you like to generate new content (1) or reset the stack and theme (2)? ")
            if choice == "1":
                print(f"Generating new content for {self.stack}...")
                # Here we would handle generating new content (not implemented)
            elif choice == "2":
                print(f"Resetting {self.stack} and re-initializing the theme...")
                self.initialize_stack(reset=True)
            else:
                print(f"Invalid choice for {self.stack}. Skipping initialization.")

    def get_shared_content(self):
        """
        Placeholder method to handle shared content retrieval.
        In a complete implementation, this would manage shared content between different stacks.
        """
        pass  # Implement shared content logic if necessary

    def modify_website(self):
        """
        Placeholder method for modifying existing website content.
        """
        print(f"Modifying website content for {self.website_name} on stack {self.stack}.")
        # Implement the logic to modify the website here.
