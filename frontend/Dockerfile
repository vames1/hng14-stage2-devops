# Stage 1 - Builder
FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json .
RUN npm install --production

# Stage 2 - Production
FROM node:18-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy installed dependencies from builder
COPY --from=builder /app/node_modules ./node_modules

# Copy application code
COPY app.js .
COPY views ./views

# Set ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => r.statusCode === 200 ? process.exit(0) : process.exit(1)).on('error', () => process.exit(1))"

CMD ["node", "app.js"]
