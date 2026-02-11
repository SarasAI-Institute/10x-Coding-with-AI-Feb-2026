#!/bin/bash
# Script to install dependencies and securely generate the entire config.yaml file.

echo "Starting secure environment setup (Generating config.yaml)..."

# --- CONFIGURATION VARIABLES ---
CONFIG_DIR="$HOME/.continue"
CONFIG_FILE="$CONFIG_DIR/config.yaml"
API_KEY="sk-helicone-2v7akjq-m2xueay-ttt23kq-hx57ubq"

# --- 1. INSTALLATION ---
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# --- 2. DYNAMIC USER ID EXTRACTION ---
GIT_EMAIL=$(git config user.email)
echo "Extracting username from $GIT_EMAIL..."

if [[ "$GIT_EMAIL" == *users.noreply.github.com ]]; then
    EMAIL_PREFIX=$(echo "$GIT_EMAIL" | sed 's/@.*//')
    FINAL_USERNAME=$(echo "$EMAIL_PREFIX" | sed -E 's/^[0-9]+\+//')
    if [ -z "$FINAL_USERNAME" ]; then
        FINAL_USERNAME=$(git config github.user)
    fi
else
    FINAL_USERNAME=$(echo "$GIT_EMAIL" | sed 's/@.*//')
fi

# --- 3. GENERATE AND WRITE CONFIGURATION FILE ---
echo "Writing configuration file to $CONFIG_FILE..."

mkdir -p "$CONFIG_DIR" || true

cat > "$CONFIG_FILE" <<- EOF
name: Local Config
version: 1.0.0
schema: v1
models:
  - name: OpenAI-via-Helicone-Proxy
    provider: openai
    model: gpt-4o
    apiBase: https://ai-gateway.helicone.ai/v1
    apiKey: '$API_KEY'
roles:
  - chat
  - edit
  - apply
requestOptions:
  headers:
    Helicone-User-Id: "$FINAL_USERNAME"
EOF

if [ -f "$CONFIG_FILE" ]; then
    echo "Configuration file successfully written and ready for Continue AI."
else
    echo "FATAL ERROR: Failed to write configuration file."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the server:"
echo "  python main.py"
echo ""
echo "API will be available at: http://localhost:8000"
echo ""
echo "Please Reload Window to load the Continue AI configuration."
