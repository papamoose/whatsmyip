# Whats My IP

Self-hosted web app that will return the requestors ip address in json format.

```
$ curl https://ip.example.com
{"ip":"1.2.3.4"}
```

## Example Usage with docker-compose.yml

```
services:

  redis:
    image: redis:latest
    container_name: redis
    networks:
    - internal
    deploy:
      resources:
        limits:
          memory: 128m

  web:
    build:
      context: .
      dockerfile: ./Dockerfile
    container_name: "whatsmyip"
    hostname: "whatsmyip"
    restart: unless-stopped
    #environment:
      #- PYTHONUNBUFFERED=true
      #- REDIS_HOST=redis
      #- REDIS_PORT=6379
      #- FLASK_ENV=development
      #- FLASK_ENV=production
    networks:
      - internal
      - gateway
    labels:
      - traefik.enable=true
      - traefik.http.routers.whatsmyip.entrypoints=https
      - traefik.http.routers.whatsmyip.rule=Host(`ip.example.com`)
      - traefik.http.routers.whatsmyip.tls.certresolver=le
      - traefik.http.routers.whatsmyip.tls.domains[0].main=ip.example.com
      - traefik.http.services.whatsmyip.loadbalancer.server.port=5000
      # Watchtower autoupdate
      - com.centurylinklabs.watchtower.enable=true


networks:
  internal:
    external: false
  gateway:
    external: true
```
