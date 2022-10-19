# ai

## Install
`docker-compose.yml`
```yml
version: '3.9'

services:
  app:
    container_name: ai
    image: ghcr.io/yuderobot/ai:latest
    volumes:
      - ./data:/app/data
    env_file:
      - ./.env
    environment:
      HOST: 0.0.0.0
      PORT: 8080
      TZ: Asia/Tokyo
      USERS: yude_jp
    restart: unless-stopped
```

## LICENSE
MIT License.
