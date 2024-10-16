import os
import subprocess
import ollama
import re
import requests
from bs4 import BeautifulSoup

# Base directory where websites are stored
BASE_DIR = "/mnt/sites"

class ThemeManager:
    def __init__(self, stack, website_name):
        self.stack = stack
        self.website_name = website_name
        self.config_file = self.get_config_file()
        self.known_repos = {
            "ananke": "https://github.com/theNewDynamic/gohugo-theme-ananke"
        }  # Fallback for known themes

    def get_config_file(self):
        """
        Return the config file path based on the website stack.
        """
        if self.stack == "hugo":
            return f"{BASE_DIR}/{self.stack}/{self.website_name}/hugo.toml"
        elif self.stack == "next.js":
            return f"{BASE_DIR}/{self.stack}/{self.website_name}/next.config.js"
        else:
            raise ValueError(f"Unsupported stack: {self.stack}")

    def get_current_theme(self):
        """
        Display the current theme by reading the config file.
        """
        try:
            with open(self.config_file, 'r') as config:
                content = config.read()
                if self.stack == "hugo":
                    theme_line = next((line for line in content.splitlines() if "theme" in line), None)
                    if theme_line:
                        current_theme = theme_line.split('=')[-1].strip().strip('"')
                        print(f"Current theme: {current_theme}")
                        return current_theme
                    else:
                        print("No theme found in config.")
                        return None
                elif self.stack == "next.js":
                    print("Next.js doesn't use a direct theme config.")
                    return None
        except FileNotFoundError:
            print(f"Config file not found at {self.config_file}")
            return None

    def initialize_theme(self, new_theme):
        """
        Use AI to find the best source for the theme and install it for the given stack.
        """
        theme_urls = self.get_theme_sources_with_validation(new_theme)
        if theme_urls:
            selected_url = theme_urls[0]  # Select the first valid URL
            print(f"Installing theme from: {selected_url}")
            if self.stack == "hugo":
                if self.install_hugo_theme(new_theme, selected_url):
                    return  # Stop further attempts if successful
            elif self.stack == "next.js":
                self.install_nextjs_theme(new_theme, selected_url)
                return  # Stop further attempts if successful
            else:
                raise ValueError(f"Unsupported stack: {self.stack}")
        else:
            print(f"Theme '{new_theme}' could not be found or is invalid.")
            self.install_from_fallback(new_theme)

    def install_from_fallback(self, new_theme):
        """
        Use a known fallback repository if no valid sources were found from the AI.
        """
        fallback_url = self.known_repos.get(new_theme.lower())
        if fallback_url:
            print(f"Using fallback URL for {new_theme}: {fallback_url}")
            if self.validate_github_repo(fallback_url):
                self.install_hugo_theme(new_theme, fallback_url)
            else:
                print(f"Failed to validate fallback URL for {new_theme}.")
        else:
            print(f"No known fallback repository for theme '{new_theme}'.")
            self.prompt_for_new_theme()

    def get_theme_sources_with_validation(self, theme_name):
        """
        Use AI to find the best sources (URLs or repositories) to download the theme and validate them.
        """
        # Ask AI for possible theme sources
        prompt = f"Find direct repository URLs for the theme '{theme_name}' for {self.stack}."
        try:
            response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])
            response_text = response['message']['content']

            # Extract URLs using regex and filter out search result pages
            urls = [url for url in re.findall(r'https?://[^\s]+', response_text) if '?' not in url and url.startswith('https')]

            valid_urls = []
            for url in urls:
                # Validate GitHub or GitLab repositories
                if 'github.com' in url:
                    if self.validate_github_repo(url):
                        valid_urls.append(url)
                        break  # Stop after the first valid URL is found
                elif 'gitlab.com' in url:
                    if self.validate_gitlab_repo(url):
                        valid_urls.append(url)
                        break  # Stop after the first valid URL is found
                elif 'themes.gohugo.io' in url or 'hugohub.com' in url:
                    if self.scrape_and_validate(url):
                        valid_urls.append(url)
                        break  # Stop after the first valid URL is found

            if valid_urls:
                print(f"Valid URLs found: {valid_urls}")
                return valid_urls
            else:
                print("No valid URLs found in AI suggestions.")
                return None
        except Exception as e:
            print(f"Error finding theme sources with AI: {e}")
            return None

    def validate_github_repo(self, repo_url):
        """
        Use GitHub API to validate if the URL is a valid repository.
        """
        try:
            # Convert URL to API-friendly format for GitHub API
            api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/")
            response = requests.get(api_url)

            if response.status_code == 200:
                print(f"Valid GitHub repository: {repo_url}")
                return True
            else:
                print(f"Invalid repository or not found: {repo_url}")
                return False
        except Exception as e:
            print(f"Error validating GitHub repository: {e}")
            return False

    def validate_gitlab_repo(self, repo_url):
        """
        Use GitLab API to validate if the URL is a valid repository.
        """
        try:
            api_url = repo_url.replace("https://gitlab.com/", "https://gitlab.com/api/v4/projects/")
            response = requests.get(api_url)

            if response.status_code == 200:
                print(f"Valid GitLab repository: {repo_url}")
                return True
            else:
                print(f"Invalid GitLab repository: {repo_url}")
                return False
        except Exception as e:
            print(f"Error validating GitLab repository: {e}")
            return False

    def scrape_and_validate(self, url):
        """
        Scrape theme-related URLs (e.g., Hugo theme directories) to check if the theme exists.
        """
        try:
            print(f"Scraping {url} for theme metadata...")
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Error accessing {url}: {response.status_code}")
                return False

            soup = BeautifulSoup(response.text, 'html.parser')

            # Basic validation: Check if a link to a GitHub repository exists in the theme page
            repo_link = soup.find('a', href=re.compile(r'https://github.com/'))
            if repo_link:
                print(f"Found valid repository link: {repo_link['href']}")
                return True
            else:
                print(f"No valid theme repository found on {url}.")
                return False
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return False

    def install_hugo_theme(self, theme, theme_url):
        """
        Install the theme for Hugo from the valid theme URL.
        """
        theme_dir = f"{BASE_DIR}/{self.stack}/{self.website_name}/themes/{theme}"
        if not os.path.exists(theme_dir):
            print(f"Installing Hugo theme '{theme}' from {theme_url}...")
            try:
                subprocess.run(["git", "clone", theme_url, theme_dir], check=True)
                print(f"Theme '{theme}' installed successfully.")
                return True  # Stop further URL checks after successful installation
            except subprocess.CalledProcessError as e:
                print(f"Error installing theme '{theme}': {e}")
                return False
        else:
            print(f"Theme '{theme}' is already installed.")
            return True  # Stop further URL checks if already installed

    def install_nextjs_theme(self, theme, theme_url):
        """
        Install the theme for Next.js using npm from a valid theme URL.
        """
        print(f"Installing Next.js theme '{theme}' from {theme_url}...")
        try:
            subprocess.run(["npm", "install", theme], cwd=f"{BASE_DIR}/{self.stack}/{self.website_name}", check=True)
            print(f"Theme '{theme}' installed successfully for Next.js.")
            return True  # Stop further URL checks after successful installation
        except subprocess.CalledProcessError as e:
            print(f"Error installing theme '{theme}': {e}")
            return False

    def change_theme(self, new_theme):
        """
        Change the theme in the config file after ensuring it's valid.
        """
        try:
            with open(self.config_file, 'r') as file:
                config_content = file.read()

            if self.stack == "hugo":
                new_content = self.replace_theme_in_hugo_config(config_content, new_theme)
            elif self.stack == "next.js":
                print(f"Next.js doesn't use a direct theme config change.")
                return
            else:
                raise ValueError(f"Unsupported stack: {self.stack}")

            # Save the new content back to the config file
            with open(self.config_file, 'w') as file:
                file.write(new_content)
            print(f"Theme changed to {new_theme} in {self.stack} for {self.website_name}.")
        except FileNotFoundError:
            print(f"Config file not found at {self.config_file}")
        except Exception as e:
            print(f"Error changing theme in {self.stack} for {self.website_name}: {e}")
        print(f"Theme '{new_theme}' could not be found.")

    def replace_theme_in_hugo_config(self, config_content, new_theme):
        """
        Use AI (Ollama) to replace the theme in the Hugo config file.
        """
        prompt = f"Replace the current theme in the following Hugo config content with '{new_theme}': {config_content}"

        try:
            response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])
            return response['message']['content']
        except Exception as e:
            print(f"Error using Ollama for theme replacement: {e}")
            return config_content  # Return original config if AI fails

    def prompt_for_new_theme(self):
        """
        Prompt the user for a new theme if the previous one is invalid or unknown.
        """
        new_theme = input("Please enter a new theme or type 'skip' to move on: ").strip()
        if new_theme.lower() == 'skip':
            print("Skipping theme change.")
            return
        self.initialize_theme(new_theme)
