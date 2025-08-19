# Flowise Telegram Bot

A Telegram bot that integrates with Flowise AI to provide conversational AI capabilities. This bot allows users to interact with your Flowise chatflows directly through Telegram.

## Features

- Seamless integration with Flowise AI
- Easy-to-use Telegram interface
- Support for custom chatflows
- Environment-based configuration
- Docker support for easy deployment
- Conversational memory support

## Prerequisites

- Python 3.13+
- Docker and Docker Compose
- Poetry for Python dependency management
- A Telegram Bot Token (obtained from [@BotFather](https://t.me/botfather))
- A running Flowise instance with API access

## Dependencies

- python-telegram-bot (>=21.10,<22.0)
- flowise (>=1.0.4,<2.0.0)
- python-dotenv (>=1.0.1,<2.0.0)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd flowise-telegram
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file in the root directory with the following variables:
```env
TELEGRAM_API_KEY=your_telegram_bot_token
FLOWISE_API_KEY=your_flowise_api_key
FLOWISE_API_URL=your_flowise_url
FLOWISE_CHATFLOW_ID=your_chatflow_id
```

## Configuration

### Environment Variables

- `TELEGRAM_API_KEY`: Your Telegram bot token from BotFather
- `FLOWISE_API_KEY`: API key from your Flowise instance
- `FLOWISE_API_URL`: URL of your Flowise instance (e.g., http://localhost:3000)
- `FLOWISE_CHATFLOW_ID`: ID of the chatflow you want to use (found in the Flowise dashboard URL when editing a flow)

### Docker Configuration

The project includes both a `docker-compose.yml` file for running Flowise and a `Dockerfile` for containerizing the bot.

To start Flowise:
```bash
docker compose up -d
```

#### Running with Local Build
To build and run the bot locally with Docker:
```bash
# Build the Docker image
docker build -t flowise-telegram-bot .

# Run the container
docker run --env-file .env --network host flowise-telegram-bot
```

#### Running with Pre-built Image
You can also use the pre-built image from GitHub Container Registry:
```bash
docker run --env-file .env --network host ghcr.io/OWNER/flowise-telegram:latest
```
Replace `OWNER` with your GitHub username.

Note: We use `--network host` to allow the bot container to communicate with Flowise running on localhost.

### CI/CD

The project includes comprehensive GitHub Actions workflows that automatically:
- Build and test the Docker image
- Push to GitHub Container Registry (ghcr.io)
- Run security scans and code quality checks
- Deploy to different environments
- Tag images based on:
  - Git branches (main, develop)
  - Git tags (v*.*.*)
  - Commit SHA

The workflows run on:
- Push to main/develop branches
- Pull requests to main branch
- New version tags

For detailed deployment information, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Flowise Chatflow Setup

1. Access Flowise at http://localhost:3000 after starting Docker
2. Create a new chatflow
3. Set up the following nodes:
   - **Chat Trigger**: Entry point for the conversation
   - **LLM (Language Model)**: Choose your preferred model (e.g., OpenAI, Anthropic)
   - **Conversation Memory**: Add memory to maintain context
   - **Agent**: Configure the agent with appropriate tools and settings
   - **Output Parser**: Format the response for Telegram

4. Configure the Agent node:
   - Set "Agent Type" to "Conversational"
   - Add system message to define bot behavior
   - Connect memory to maintain conversation context
   - Add relevant tools if needed

5. Enable API access for your chatflow:
   - Click on the "Chat Trigger" node
   - Enable "API Endpoint"
   - Save the chatflow

6. Copy the chatflow ID from the URL when editing the flow
7. Configure your API key in Flowise settings

Example System Message for Agent:
```
You are a helpful AI assistant integrated with Telegram. Your responses should be:
1. Concise and clear
2. Formatted appropriately for Telegram
3. Helpful and informative
4. Natural and conversational

Always maintain a friendly and professional tone. If you don't know something, say so directly.
```

## Running the Bot

### Local Development
1. Start the bot using Python:
```bash
python main.py
```

2. Start a conversation with your bot on Telegram
3. Send a message to test the integration

### Production Deployment
The bot can be deployed using the provided GitHub Actions workflows:

1. **Push to GitHub**: The workflows automatically build and deploy
2. **Use Pre-built Images**: Pull from GitHub Container Registry
3. **Custom Deployment**: Use the deployment scripts in `scripts/`

For complete deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Project Structure

```
flowise-telegram/
├── main.py                    # Main bot implementation
├── docker-compose.yml         # Docker configuration
├── Dockerfile                 # Bot container definition
├── .env                      # Environment configuration
├── .github/workflows/        # GitHub Actions workflows
│   ├── ci-cd.yml            # Main CI/CD pipeline
│   ├── deploy.yml           # Deployment automation
│   └── test.yml             # Testing and quality checks
├── scripts/                  # Deployment scripts
│   └── deploy.sh            # Automated deployment script
├── DEPLOYMENT.md            # Comprehensive deployment guide
├── README.md                # Project documentation
└── .gitignore              # Git ignore rules
```

## Development

### Local Development

1. Start Flowise using Docker:
```bash
docker compose up -d
```

2. Run the bot in development mode:
```bash
python main.py
```

### Making Changes

1. Update the code in `main.py`
2. Test your changes locally
3. Commit changes with descriptive messages
4. Push to your repository

## Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check if your Telegram token is correct
   - Verify the bot is running
   - Check Python logs for errors

2. **Flowise connection errors**
   - Ensure Flowise container is running (`docker ps`)
   - Verify your Flowise URL and API key
   - Check if Flowise is accessible in your browser

3. **Missing responses**
   - Verify your chatflow ID is correct
   - Ensure the chatflow is properly configured in Flowise
   - Check if the chatflow works in Flowise UI

4. **Memory Issues**
   - Verify the Conversation Memory node is properly connected
   - Check memory configuration in the Agent node
   - Test the chatflow in Flowise UI to verify memory retention

### Logs

To view logs:
- Bot logs: Run the bot directly to see output
- Flowise logs: `docker compose logs -f flowise`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
