# Web3 Vulnerabilities in Web3 Security Labs

This repository contains interactive security labs that demonstrate how traditional web vulnerabilities can impact Web3 applications. These labs are designed for educational purposes to help developers, security researchers, and blockchain ecosystem builders understand and mitigate common security risks.

## Overview

The labs focus on two critical vulnerabilities that can affect off-chain components in Web3 applications:

1. **IDOR (Insecure Direct Object Reference)** in a Solana Relayer API
2. **SSRF (Server-Side Request Forgery)** in an NFT Metadata Fetcher

Each lab includes both vulnerable and fixed versions, allowing you to explore the vulnerabilities and understand how to properly secure your applications.

## Architecture

This project uses a hybrid architecture:
- **Frontend**: Next.js application (JavaScript/React)
- **Backend**: Flask application (Python)

## Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher (for frontend development)
- Docker and Docker Compose (optional, for containerized setup)

## Installation and Setup

### Backend Setup

1. Clone this repository:
   \`\`\`bash
   git clone https://github.com/Stephnoraa/Web3_Vulnerabilities.git
   cd Web3_Vulnerabilities
   \`\`\`

2. Create a virtual environment and activate it:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Run the Flask application:
   \`\`\`bash
   python app.py
   \`\`\`

The backend will be available at `http://localhost:5000`.

### Frontend Setup

The frontend is a Next.js application that communicates with the Flask backend.

1. Navigate to the frontend directory:
   \`\`\`bash
   cd frontend
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

3. Build the frontend:
   \`\`\`bash
   npm run build
   \`\`\`

4. (Optional) For development, you can run the frontend separately:
   \`\`\`bash
   npm run dev
   \`\`\`

## Docker Setup

You can also run the entire application using Docker:

\`\`\`bash
docker-compose up --build
\`\`\`

This will start both the Flask backend and serve the Next.js frontend.

## Deployment

### Deploying to a Production Server

1. Build the Next.js frontend:
   \`\`\`bash
   cd frontend
   npm run build
   \`\`\`

2. Deploy the Flask application with the built frontend:
   \`\`\`bash
   gunicorn --bind 0.0.0.0:5000 app:app
   \`\`\`

### Deploying to Heroku

1. Create a Procfile:
   \`\`\`
   web: gunicorn app:app
   \`\`\`

2. Deploy to Heroku:
   \`\`\`bash
   heroku create
   git push heroku main
   \`\`\`

### Deploying to AWS, GCP, or Azure

The application can be deployed to any cloud provider that supports Docker containers or Python applications. Refer to the specific cloud provider's documentation for detailed deployment instructions.

## Lab 1: IDOR Vulnerability in a Solana Relayer API

### Vulnerability Description

Insecure Direct Object Reference (IDOR) occurs when an application provides direct access to objects based on user-supplied input. This vulnerability allows attackers to bypass authorization and access resources directly by modifying the value of a parameter used to directly point to an object.

In this lab, the vulnerable API endpoint allows any user to access any other user's data simply by changing the user ID parameter, without proper authentication or authorization checks.

### Exploitation

1. Navigate to the vulnerable version of Lab 1
2. Notice that you can view Jordan's data (User ID: 1) by default
3. Change the User ID to 2 in the input field and click "Fetch User Data"
4. Observe that you can now access Taylor's data, including sensitive information like private API keys

### Security Fix

The fixed version implements proper authentication and authorization:

1. Users must authenticate before accessing any data
2. Users can only access their own data
3. The server verifies the user's session and permissions before returning data

## Lab 2: SSRF Vulnerability in an NFT Metadata Fetcher

### Vulnerability Description

Server-Side Request Forgery (SSRF) allows an attacker to induce the server-side application to make requests to an unintended location. In a Web3 context, this could allow attackers to access internal services, metadata, or even private blockchain nodes.

In this lab, the vulnerable metadata fetcher service allows the client to specify any URL, including internal resources that should not be accessible from the outside.

### Exploitation

1. Navigate to the vulnerable version of Lab 2
2. Enter a normal URL like `https://example.com/nft/metadata.json` to see how the service fetches NFT metadata
3. Try entering an internal URL like `http://localhost:8080/admin`
4. Observe that you can access internal admin data that should not be accessible

### Security Fix

The fixed version implements proper URL validation and domain allowlisting:

1. Only HTTPS URLs are allowed, preventing `file://` and other dangerous protocols
2. Only trusted domains are allowed, preventing access to internal resources
3. URLs are properly parsed and validated before making any requests

## Security Best Practices for Web3 Applications

### For IDOR Prevention:

1. Implement proper authentication for all API endpoints
2. Use session-based or token-based authorization
3. Validate that the authenticated user has permission to access the requested resource
4. Use indirect references (e.g., UUIDs instead of sequential IDs)
5. Implement proper access control checks on the server side

### For SSRF Prevention:

1. Validate and sanitize all user-supplied URLs
2. Use an allowlist of permitted domains and protocols
3. Block requests to private IP ranges and localhost
4. Implement network-level protections (e.g., firewalls, network segmentation)
5. Use a dedicated service account with minimal privileges for external requests

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

These labs are for educational purposes only. Do not use these vulnerable examples in production environments.
\`\`\`

Let's also create a `.env` file for environment variables:

```plaintext file=".env"
# Flask configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-for-sessions-change-this-in-production

# Server configuration
PORT=5000
HOST=0.0.0.0

# CORS settings
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
