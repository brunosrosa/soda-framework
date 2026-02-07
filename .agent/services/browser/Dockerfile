FROM mcr.microsoft.com/playwright:v1.41.0-jammy

WORKDIR /app

# Install dependencies layer
RUN npm install -g @executeautomation/playwright-mcp-server

# Entrypoint
CMD ["npx", "-y", "@executeautomation/playwright-mcp-server"]
