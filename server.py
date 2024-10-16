import os
import yaml
import subprocess

# Base directory where websites are stored
BASE_DIR = "/app"

# Default ports for different stacks
DEFAULT_PORTS = {
    "hugo": 1313,
    "next.js": 3000
}

def detect_website_stacks(base_dir=BASE_DIR):
    websites = []
    for dirpath, dirnames, filenames in os.walk(base_dir):
        if "hugo.toml" in filenames:
            websites.append({"name": os.path.basename(dirpath), "stack": "hugo", "path": dirpath})
        elif "next.config.js" in filenames:
            websites.append({"name": os.path.basename(dirpath), "stack": "next.js", "path": dirpath})
    return websites

def generate_docker_compose(websites, output_file="utils/docker-compose.generated.yml"):
    services = {}
    used_ports = set()
    
    for website in websites:
        stack = website["stack"]
        name = website["name"]
        path = website["path"]

        # Find an available port, starting from the default
        port = DEFAULT_PORTS.get(stack, 8000)
        while port in used_ports:
            port += 1  # Increment port if already used
        used_ports.add(port)

        # Define service configuration for this stack
        service = {
            "build": path,
            "ports": [f"{port}:{port}"],
            "volumes": [f"./{stack}/{name}:/app"],
            "container_name": f"{stack}_{name}_container",
            "restart": "always"
        }

        if stack == "hugo":
            service["command"] = ["hugo", "server", "--bind", "0.0.0.0", "--port", str(port)]
        elif stack == "next.js":
            service["command"] = ["npm", "start"]

        # Add the service to the docker-compose services
        services[f"{stack}_{name}"] = service

    # Create docker-compose content
    docker_compose_content = {
        "version": "3",
        "services": services
    }

    # Write to the output file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as file:
        yaml.dump(docker_compose_content, file)

    print(f"Docker Compose file generated at {output_file}")

def serve_website(website):
    stack = website["stack"]
    path = website["path"]
    
    # Run docker-compose to bring up the service
    if stack == "hugo":
        subprocess.run(["docker-compose", "-f", "utils/docker-compose.generated.yml", "up", "-d"])
    elif stack == "next.js":
        subprocess.run(["docker-compose", "-f", "utils/docker-compose.generated.yml", "up", "-d"])

def main():
    websites = detect_website_stacks()
    
    if not websites:
        print("No websites found. Exiting.")
        return

    # Generate docker-compose file dynamically
    generate_docker_compose(websites)
    
    # Serve websites using the generated Docker Compose file
    for website in websites:
        print(f"Serving {website['stack']} website: {website['name']}")
        serve_website(website)

if __name__ == "__main__":
    main()

