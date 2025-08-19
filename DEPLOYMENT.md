# Deployment Guide

This guide explains how to deploy your Flowise Telegram Bot using GitHub Actions and various deployment strategies.

## 🚀 GitHub Actions Deployment

### Overview
The project includes three GitHub Actions workflows:

1. **CI/CD Pipeline** (`ci-cd.yml`) - Builds and pushes Docker images
2. **Deploy** (`deploy.yml`) - Handles deployment to different environments
3. **Test** (`test.yml`) - Runs tests and code quality checks

### Prerequisites

1. **GitHub Repository**: Push your code to a GitHub repository
2. **GitHub Container Registry Access**: Ensure your repository has access to ghcr.io
3. **Secrets**: The workflows use `GITHUB_TOKEN` which is automatically available

### How It Works

#### 1. Automatic Builds
- **On Push to main/develop**: Automatically builds and pushes Docker images
- **On Pull Request**: Builds image for testing
- **On Release**: Creates versioned tags

#### 2. Image Naming Convention
Images are automatically tagged with:
- `latest` - For main branch
- `develop` - For develop branch
- `main-{sha}` - For specific commits
- `v1.0.0` - For semantic version tags

#### 3. Security Scanning
- **Trivy**: Scans Docker images for vulnerabilities
- **Results**: Uploaded to GitHub Security tab

### Deployment Environments

#### Staging (develop branch)
- Automatically deploys when pushing to `develop`
- Uses `ghcr.io/your-repo:develop` image
- Configure in `.github/workflows/deploy.yml`

#### Production (main branch)
- Automatically deploys when pushing to `main`
- Uses `ghcr.io/your-repo:latest` image
- Requires manual approval (if configured)

## 🐳 Docker Deployment

### Using Pre-built Images

After GitHub Actions builds your image, you can deploy it anywhere:

```bash
# Pull the latest image
docker pull ghcr.io/your-username/flowise-telegram-bot:latest

# Run with environment variables
docker run -d \
    --name flowise-telegram-bot \
    --restart unless-stopped \
    --env-file .env \
    --network host \
    ghcr.io/your-username/flowise-telegram-bot:latest
```

### Custom Deployment Script

Use the provided deployment script:

```bash
# Make it executable
chmod +x scripts/deploy.sh

# Deploy to production
ENVIRONMENT=production TAG=latest ./scripts/deploy.sh

# Deploy to staging
ENVIRONMENT=staging TAG=develop ./scripts/deploy.sh
```

## ☁️ Cloud Deployment Options

### 1. AWS ECS/Fargate
```yaml
# task-definition.json
{
  "family": "flowise-telegram-bot",
  "containerDefinitions": [{
    "name": "bot",
    "image": "ghcr.io/your-username/flowise-telegram-bot:latest",
    "environment": [
      {"name": "TELEGRAM_API_KEY", "value": "your-key"},
      {"name": "FLOWISE_API_KEY", "value": "your-key"},
      {"name": "FLOWISE_API_URL", "value": "your-url"},
      {"name": "FLOWISE_CHATFLOW_ID", "value": "your-id"}
    ]
  }]
}
```

### 2. Google Cloud Run
```bash
gcloud run deploy flowise-telegram-bot \
    --image ghcr.io/your-username/flowise-telegram-bot:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars="TELEGRAM_API_KEY=your-key,FLOWISE_API_KEY=your-key"
```

### 3. Azure Container Instances
```bash
az container create \
    --resource-group myResourceGroup \
    --name flowise-telegram-bot \
    --image ghcr.io/your-username/flowise-telegram-bot:latest \
    --environment-variables \
        TELEGRAM_API_KEY=your-key \
        FLOWISE_API_KEY=your-key \
        FLOWISE_API_URL=your-url \
        FLOWISE_CHATFLOW_ID=your-id
```

### 4. DigitalOcean App Platform
```yaml
# .do/app.yaml
name: flowise-telegram-bot
services:
  - name: bot
    source_dir: /
    github:
      repo: your-username/flowise-telegram-bot
      branch: main
    dockerfile_path: Dockerfile
    environment_slug: python
    envs:
      - key: TELEGRAM_API_KEY
        value: your-key
      - key: FLOWISE_API_KEY
        value: your-key
```

## 🔧 Environment Configuration

### Required Environment Variables
```env
TELEGRAM_API_KEY=your_telegram_bot_token
FLOWISE_API_KEY=your_flowise_api_key
FLOWISE_API_URL=your_flowise_url
FLOWISE_CHATFLOW_ID=your_chatflow_id
```

### Optional Environment Variables
```env
# Logging
LOG_LEVEL=INFO

# Bot Configuration
BOT_NAME=FlowiseBot
BOT_DESCRIPTION=AI-powered Telegram bot

# Flowise Configuration
FLOWISE_TIMEOUT=30000
FLOWISE_STREAMING=false
```

## 📊 Monitoring and Health Checks

### Health Check Endpoint
Add this to your bot for monitoring:

```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

### Docker Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

## 🔒 Security Considerations

### 1. Environment Variables
- Never commit `.env` files to version control
- Use secrets management in your deployment platform
- Rotate API keys regularly

### 2. Network Security
- Use private networks when possible
- Implement proper firewall rules
- Consider using VPN for internal services

### 3. Container Security
- Regularly update base images
- Scan images for vulnerabilities
- Use non-root users in containers

## 🚨 Troubleshooting

### Common Issues

#### 1. Image Pull Failures
```bash
# Check if you're logged in to ghcr.io
docker login ghcr.io

# Verify image exists
docker pull ghcr.io/your-username/flowise-telegram-bot:latest
```

#### 2. Environment Variable Issues
```bash
# Test environment variables
docker run --rm --env-file .env ghcr.io/your-username/flowise-telegram-bot:latest env | grep FLOWISE
```

#### 3. Network Connectivity
```bash
# Test Flowise connection
curl -H "Authorization: Bearer $FLOWISE_API_KEY" $FLOWISE_API_URL/api/v1/chatflows
```

### Debug Mode
Enable debug logging:
```bash
docker run -e LOG_LEVEL=DEBUG --env-file .env ghcr.io/your-username/flowise-telegram-bot:latest
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Deploy multiple bot instances behind a load balancer
- Use Redis for shared session storage
- Implement proper session affinity

### Vertical Scaling
- Monitor resource usage
- Adjust CPU/memory limits based on usage patterns
- Use resource quotas in Kubernetes

## 🔄 Continuous Deployment

### Automatic Deployment
The GitHub Actions workflows automatically:
1. Build and test your code
2. Create Docker images
3. Push to container registry
4. Deploy to appropriate environments

### Manual Deployment
For manual deployments:
```bash
# Build locally
docker build -t flowise-telegram-bot .

# Push to registry
docker tag flowise-telegram-bot ghcr.io/your-username/flowise-telegram-bot:manual
docker push ghcr.io/your-username/flowise-telegram-bot:manual

# Deploy
./scripts/deploy.sh
```

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Flowise Documentation](https://docs.flowiseai.com/)
