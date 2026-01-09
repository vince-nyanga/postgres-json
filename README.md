# Working with JSON Data in PostgreSQL

This repository provides a comprehensive guide on how to work with JSON data types in PostgreSQL. You'll find examples and best practices for storing, querying, and manipulating JSON data using

**PostgreSQL 18** on your local machine.

## 📋 Prerequisites

Ensure you have the following installed:

1. **Docker & Docker Compose**: [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. **uv**: The high-performance Python package manager.
   - **Installation**: [Official UV Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
   - _Quick Tip (Mac/Linux):_ `curl -LsSf https://astral.sh/uv/install.sh | sh`

## ⚡ Quick Start

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd postgres-json
   ```
2. **Run the automated setup:**

   ```bash
   make setup
   ```

3. **Launch the lab:**
   ```bash
   make lab
   ```

### Commands

`make setup`: Fresh install of environment and data.

`make lab`: Launches the Jupyter notebook locally.

`make reset`: Wipes the database and re-seeds from scratch.
`make clean`: Deletes the virtual environment and all Docker volumes.
