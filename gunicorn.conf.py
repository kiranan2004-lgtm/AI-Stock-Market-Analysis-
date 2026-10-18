import os

# Dynamic port binding from Render environment ($PORT defaults to 10000 on Render)
port = os.environ.get("PORT", "10000")
bind = f"0.0.0.0:{port}"

# Concurrency configuration suitable for Render 512MB free tier
workers = 2
threads = 4
timeout = 120
keepalive = 5

# Logging to standard output for Render Dashboard live log streaming
accesslog = "-"
errorlog = "-"
loglevel = "info"
capture_output = True
enable_stdio_inheritance = True
