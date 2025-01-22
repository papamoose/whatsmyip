#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
from os import getenv

redis_host = getenv('REDIS_HOST', 'redis')
redis_port = int(getenv('REDIS_PORT', 6379))

app = Flask(__name__)
limiter = Limiter(
  key_func=lambda: request.headers.get('X-Forwarded-For', request.remote_addr),
  app=app,
  default_limits=["200 per day", "50 per hour"],
  storage_uri=f"redis://{redis_host}:{redis_port}",
)

# Custom handler for "Too Many Requests"
@app.errorhandler(429)
def too_many_requests_handler(e):
    return jsonify({
        "error": "Too many requests",
        "message": "You have exceeded the allowed number of requests.",
        "status_code": 429,
        "limit": e.description,  # Description contains rate limit details
        "retry_after": e.retry_after  # Time in seconds until the limit resets
    }), 429

@app.route("/")
@limiter.limit("10 per hour")
def get_ip():
  # Check if the request contains the X-Forwarded-For header
  client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

  # In case there are multiple IPs in the X-Forwarded-For header, use the first one
  if ',' in client_ip:
    client_ip = client_ip.split(',')[0].strip()

  print(f"{client_ip} | Got a request from this ip")

  # Return the IP in JSON format
  return jsonify({"ip": client_ip})

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
