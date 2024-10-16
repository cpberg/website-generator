# Website Generator with Multi-Stack Support (Hugo, Next.js)

This project is a dynamic website generator designed to handle multiple web development stacks (e.g., Hugo, Next.js). It automatically detects the website stacks, assigns unique ports, generates a Docker Compose file, and serves each website in its own container. The solution is designed to be cloud-portable and easy to use.

## Features
- **Multi-Stack Detection**: Automatically detects websites built with different stacks (Hugo, Next.js, etc.).
- **Dynamic Port Assignment**: Automatically assigns and manages ports for each website.
- **Docker Compose Generation**: Generates a valid Docker Compose file dynamically, which includes port forwarding and configuration for each stack.
- **Content Generation**: Uses AI (Ollama) for generating or modifying website content and configurations.
- **Theme Management**: Supports dynamic theme changes, validating themes using AI and sourcing them from official repositories.

## How It Works
1. **Website Detection**: The generator scans the `/app` directory to identify websites using supported stacks (Hugo, Next.js).
2. **Docker Compose Generation**: It automatically creates a `docker-compose.yml` file with services for each detected stack.
3. **Port Assignment**: Each website gets a unique port to avoid conflicts.
4. **Serving Websites**: The system runs `docker-compose up` to serve the websites based on their respective stacks.

## Stack Support
- **Hugo**: Static site generation.
- **Next.js**: Full-stack React framework for building server-side rendered and static websites.

## Prerequisites
- **Docker** and **Docker Compose** installed on your machine.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/website-generator.git
   cd website-generator
	 ```

2. Run Docker Compose:
   ```bash
    docker-compose up -d
	 ```

3. Access the Website Generator Service:
   You can interact with the website generator service via Docker:
   ```bash
    docker exec -it website-generator-container python3 main.py
	 ```

    This will allow you to initialize or modify websites through the interactive prompt.


## Usage

1. Initializing/Modifying a Website:
    Once inside the container, you will be prompted to either initialize a website (if it hasn't been set up) or modify an existing one.
   
2. Changing Themes:
    If needed, the script can query AI to find and install a new theme for the website.

3. Automatic Content Generation:
    The generator can generate base content (e.g., homepage, services) using AI based on the website type.


## Example

- To initialize and serve a Hugo site:
    1. Run docker exec -it website-generator-container python3 main.py
    2. Select "Hugo" as the stack.
    3. Follow the prompts to initialize or modify the Hugo website.

- To initialize and serve a Next.js site:
    1. Run docker exec -it website-generator-container python3 main.py
    2. Select "Next.js" as the stack.
    3. Follow the prompts to initialize or modify the Next.js website.

## Project Structure
```plaintext
.
├── app/                              # Main folder containing python
│   ├── main.py                       # Interactive prompt entry point
│   ├── requirements.txt              # Python dependencies
│   ├── server.py                     # Main Python script for serving websites
│   ├── theme_manager.py              # Python module for managing themes
│   ├── website.py                    # Website object class
├── utils/                            # Utility folder
│   └── docker-compose.generated.yml  # Auto-generated Docker Compose file
├── websites/                         # Main folder containing website directories
│   ├── hugo/                         # Hugo websites
│   └── next.js/                      # Next.js websites
└── README.md                         # Project documentation
