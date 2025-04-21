#!/bin/bash

# ✨ Python 3.11.x Virtual Environment Initializer ✨
# Created: $(date '+%Y-%m-%d')

set -e  # Exit immediately if a command exits with a non-zero status

# ANSI color codes for better visual feedback
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default values
VENV_NAME="py311_env"
PYTHON_VERSION="3.11"
INSTALL_DIR="$HOME/.local/python$PYTHON_VERSION"
QUIET=false

# Echo with timestamp
echo_ts() {
  echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Display a spinning progress indicator
spinner() {
  local pid=$1
  local delay=0.1
  local spinstr='|/-\'
  echo -n "  "
  while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
    local temp=${spinstr#?}
    printf " [%c]  " "$spinstr"
    local spinstr=$temp${spinstr%"$temp"}
    sleep $delay
    printf "\b\b\b\b\b\b"
  done
  printf "    \b\b\b\b"
}

# Function to display usage information
show_help() {
  echo -e "${CYAN}Python 3.11.x Virtual Environment Initializer${NC}"
  echo -e "Usage: $0 [options]"
  echo -e "Options:"
  echo -e "  ${GREEN}-n, --name NAME${NC}      Name of the virtual environment (default: $VENV_NAME)"
  echo -e "  ${GREEN}-d, --dir DIRECTORY${NC}  Directory to install Python 3.11 (default: $INSTALL_DIR)"
  echo -e "  ${GREEN}-q, --quiet${NC}          Suppress detailed output"
  echo -e "  ${GREEN}-h, --help${NC}           Display this help message and exit"
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -n|--name)
      VENV_NAME="$2"
      shift 2
      ;;
    -d|--dir)
      INSTALL_DIR="$2"
      shift 2
      ;;
    -q|--quiet)
      QUIET=true
      shift
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      show_help
      exit 1
      ;;
  esac
done

echo_ts "${MAGENTA}🔮 Starting Python ${PYTHON_VERSION} Virtual Environment Creation 🔮${NC}"
echo_ts "${CYAN}➡️ Virtual Environment Name: ${VENV_NAME}${NC}"
echo_ts "${CYAN}➡️ Python Install Directory: ${INSTALL_DIR}${NC}"

# Check if Python 3.11 is already installed
echo_ts "${YELLOW}🔍 Checking for Python ${PYTHON_VERSION}...${NC}"
if command -v python${PYTHON_VERSION} &>/dev/null; then
  echo_ts "${GREEN}✅ Python ${PYTHON_VERSION} is already installed!${NC}"
  PYTHON_CMD="python${PYTHON_VERSION}"
elif [ -f "${INSTALL_DIR}/bin/python${PYTHON_VERSION}" ]; then
  echo_ts "${GREEN}✅ Python ${PYTHON_VERSION} found at ${INSTALL_DIR}/bin/python${PYTHON_VERSION}${NC}"
  PYTHON_CMD="${INSTALL_DIR}/bin/python${PYTHON_VERSION}"
else
  echo_ts "${YELLOW}⚙️ Python ${PYTHON_VERSION} not found. Attempting to install...${NC}"

  # Determine the OS
  if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
  else
    OS=$(uname -s)
  fi

  # Install Python 3.11 based on the OS
  case $OS in
    *Ubuntu*|*Debian*)
      echo_ts "${CYAN}📦 Detected ${OS}. Installing Python ${PYTHON_VERSION} using apt...${NC}"
      sudo apt update
      if ! $QUIET; then
        sudo apt install -y software-properties-common
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt update
        sudo apt install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python${PYTHON_VERSION}-dev
      else
        sudo apt install -y software-properties-common >/dev/null 2>&1
        sudo add-apt-repository -y ppa:deadsnakes/ppa >/dev/null 2>&1
        sudo apt update >/dev/null 2>&1
        sudo apt install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python${PYTHON_VERSION}-dev >/dev/null 2>&1
      fi
      PYTHON_CMD="python${PYTHON_VERSION}"
      ;;
    *Fedora*|*CentOS*|*RHEL*)
      echo_ts "${CYAN}📦 Detected ${OS}. Installing Python ${PYTHON_VERSION} using dnf/yum...${NC}"
      if command -v dnf &>/dev/null; then
        if ! $QUIET; then
          sudo dnf install -y python${PYTHON_VERSION}
        else
          sudo dnf install -y python${PYTHON_VERSION} >/dev/null 2>&1
        fi
      else
        if ! $QUIET; then
          sudo yum install -y python${PYTHON_VERSION}
        else
          sudo yum install -y python${PYTHON_VERSION} >/dev/null 2>&1
        fi
      fi
      PYTHON_CMD="python${PYTHON_VERSION}"
      ;;
    *)
      # Fallback to building from source for other distributions
      echo_ts "${CYAN}📦 Installing Python ${PYTHON_VERSION} from source...${NC}"
      mkdir -p "$INSTALL_DIR"
      
      # Install dependencies
      if command -v apt-get &>/dev/null; then
        echo_ts "${CYAN}Installing build dependencies...${NC}"
        if ! $QUIET; then
          sudo apt-get update
          sudo apt-get install -y build-essential libssl-dev zlib1g-dev \
            libbz2-dev libreadline-dev libsqlite3-dev llvm \
            libncurses5-dev libncursesw5-dev xz-utils tk-dev \
            libffi-dev liblzma-dev wget curl
        else
          sudo apt-get update >/dev/null 2>&1
          sudo apt-get install -y build-essential libssl-dev zlib1g-dev \
            libbz2-dev libreadline-dev libsqlite3-dev llvm \
            libncurses5-dev libncursesw5-dev xz-utils tk-dev \
            libffi-dev liblzma-dev wget curl >/dev/null 2>&1
        fi
      fi
      
      echo_ts "${YELLOW}⬇️ Downloading Python ${PYTHON_VERSION}...${NC}"
      # Get the latest patch version of Python 3.11
      LATEST_PY311=$(curl -s https://www.python.org/downloads/ | grep -oP 'Python 3\.11\.[0-9]+' | sort -V | tail -1 | cut -d ' ' -f 2)
      echo_ts "${CYAN}Latest version found: ${LATEST_PY311}${NC}"
      
      TMP_DIR=$(mktemp -d)
      cd "$TMP_DIR"
      
      if ! $QUIET; then
        wget "https://www.python.org/ftp/python/${LATEST_PY311}/Python-${LATEST_PY311}.tgz"
      else
        wget -q "https://www.python.org/ftp/python/${LATEST_PY311}/Python-${LATEST_PY311}.tgz"
      fi
      
      tar -xzf "Python-${LATEST_PY311}.tgz"
      cd "Python-${LATEST_PY311}"
      
      echo_ts "${YELLOW}🔨 Configuring and building Python ${LATEST_PY311}...${NC}"
      if ! $QUIET; then
        ./configure --prefix="$INSTALL_DIR" --enable-optimizations
        make -j$(nproc)
        make install
      else
        ./configure --prefix="$INSTALL_DIR" --enable-optimizations >/dev/null 2>&1
        make -j$(nproc) >/dev/null 2>&1 &
        PID=$!
        spinner $PID
        make install >/dev/null 2>&1 &
        PID=$!
        spinner $PID
      fi
      
      PYTHON_CMD="${INSTALL_DIR}/bin/python3"
      
      # Add Python to PATH temporarily
      export PATH="$INSTALL_DIR/bin:$PATH"
      
      cd -
      rm -rf "$TMP_DIR"
      echo_ts "${GREEN}✅ Python ${LATEST_PY311} installed successfully to ${INSTALL_DIR}${NC}"
      ;;
  esac
fi

# Create virtual environment
echo_ts "${YELLOW}🏗️ Creating virtual environment '${VENV_NAME}'...${NC}"
if [ -d "$VENV_NAME" ]; then
  echo_ts "${YELLOW}⚠️ Directory '${VENV_NAME}' already exists. Overwrite? (y/N)${NC}"
  read -r response
  if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    rm -rf "$VENV_NAME"
  else
    echo_ts "${RED}❌ Aborted.${NC}"
    exit 1
  fi
fi

if ! $QUIET; then
  $PYTHON_CMD -m venv "$VENV_NAME"
else
  $PYTHON_CMD -m venv "$VENV_NAME" >/dev/null 2>&1
fi

if [ $? -eq 0 ]; then
  echo_ts "${GREEN}✅ Virtual environment '${VENV_NAME}' created successfully!${NC}"
  
  # Additional setup
  echo_ts "${YELLOW}🧪 Setting up the virtual environment...${NC}"
  if ! $QUIET; then
    "$VENV_NAME/bin/pip" install --upgrade pip setuptools wheel
  else
    "$VENV_NAME/bin/pip" install --upgrade pip setuptools wheel >/dev/null 2>&1
  fi

  # Verify Python version in venv
  VENV_PY_VERSION=$("$VENV_NAME/bin/python" --version 2>&1)
  echo_ts "${GREEN}🐍 Virtual environment is using ${VENV_PY_VERSION}${NC}"

  # Add activation instructions
  echo -e "\n${MAGENTA}✨ To activate the virtual environment, run:${NC}"
  echo -e "${CYAN}    source ${VENV_NAME}/bin/activate${NC}"
  echo -e "\n${MAGENTA}✨ To deactivate when finished, run:${NC}"
  echo -e "${CYAN}    deactivate${NC}"
  
  # Create a simple activation script for convenience
  echo '#!/bin/bash' > activate_py311_env.sh
  echo "# Activation script for Python ${PYTHON_VERSION} virtual environment" >> activate_py311_env.sh
  echo "source \$(dirname \$(readlink -f \$0))/${VENV_NAME}/bin/activate" >> activate_py311_env.sh
  chmod +x activate_py311_env.sh
  
  echo -e "\n${MAGENTA}✨ For quick activation, you can also use:${NC}"
  echo -e "${CYAN}    source ./activate_py311_env.sh${NC}"
else
  echo_ts "${RED}❌ Failed to create virtual environment.${NC}"
  exit 1
fi

echo -e "\n${GREEN}🎉 Setup complete! Enjoy your Python ${PYTHON_VERSION} environment!${NC}"