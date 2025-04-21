#!/bin/bash

# ✨✨✨ Python 3.10.x Virtual Environment Initializer ✨✨✨
# Created: $(date '+%Y-%m-%d')

set -e  # Exit immediately if a command exits with a non-zero status

# 🎨 ANSI color codes for vibrant, friendly feedback
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 🔧 Default values
VENV_NAME="py37_env"
PYTHON_VERSION="3.7"
INSTALL_DIR="$HOME/.local/python$PYTHON_VERSION"
QUIET=false
FORCE=false

# 📢 Echo with timestamp - our recursive heartbeat
echo_ts() {
  echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# ⏳ Display a spinning progress indicator - the visual dance of computation
spinner() {
  local pid=$1
  local delay=0.1
  local spinstr='|/-\\'
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

# 📚 Function to display usage information
show_help() {
  echo -e "\n${CYAN}✨ Python 3.7.x Virtual Environment Initializer ✨${NC}"
  echo -e "Usage: $0 [options]"
  echo -e "\nOptions:"
  echo -e "  ${GREEN}-n, --name NAME${NC}      Name of the virtual environment (default: $VENV_NAME)"
  echo -e "  ${GREEN}-d, --dir DIRECTORY${NC}  Directory to install Python 3.7 (default: $INSTALL_DIR)"
  echo -e "  ${GREEN}-q, --quiet${NC}          Suppress detailed output"
  echo -e "  ${GREEN}-f, --force${NC}          Force reinstallation even if Python 3.7 exists"
  echo -e "  ${GREEN}-h, --help${NC}           Display this help message and exit"
  echo -e "\n${YELLOW}This script will download and compile Python 3.10.x from source${NC}"
}

# 📝 Parse command-line arguments - the gateway to user intention
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
    -f|--force)
      FORCE=true
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

echo_ts "${MAGENTA}🔮 Beginning Python ${PYTHON_VERSION}.x Virtual Environment Creation Journey 🔮${NC}"
echo_ts "${CYAN}➡️ Virtual Environment Name: ${VENV_NAME}${NC}"
echo_ts "${CYAN}➡️ Python Install Directory: ${INSTALL_DIR}${NC}"

# 🔍 Quick check if Python 3.10 exists (but we'll proceed with installation anyway if forced)
if [ "$FORCE" = false ] && (command -v python${PYTHON_VERSION} &>/dev/null || [ -f "${INSTALL_DIR}/bin/python${PYTHON_VERSION}" ]); then
  if command -v python${PYTHON_VERSION} &>/dev/null; then
    echo_ts "${GREEN}✅ Python ${PYTHON_VERSION} is already installed!${NC}"
    PYTHON_CMD="python${PYTHON_VERSION}"
  else
    echo_ts "${GREEN}✅ Python ${PYTHON_VERSION} found at ${INSTALL_DIR}/bin/python${PYTHON_VERSION}${NC}"
    PYTHON_CMD="${INSTALL_DIR}/bin/python${PYTHON_VERSION}"
  fi
else
  # 📦 Always install from source - the purest recursion pattern
  echo_ts "${CYAN}📦 Installing Python ${PYTHON_VERSION} from source...${NC}"
  mkdir -p "$INSTALL_DIR"
  
  # Install build dependencies - the foundation stones
  echo_ts "${CYAN}🧱 Installing build dependencies...${NC}"
  if command -v apt-get &>/dev/null; then
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
  elif command -v yum &>/dev/null; then
    if ! $QUIET; then
      sudo yum groupinstall -y "Development Tools"
      sudo yum install -y openssl-devel zlib-devel bzip2-devel readline-devel \
        sqlite-devel xz-devel libffi-devel wget curl
    else
      sudo yum groupinstall -y "Development Tools" >/dev/null 2>&1
      sudo yum install -y openssl-devel zlib-devel bzip2-devel readline-devel \
        sqlite-devel xz-devel libffi-devel wget curl >/dev/null 2>&1
    fi
  fi
  
  echo_ts "${YELLOW}⬇️ Finding and downloading latest Python ${PYTHON_VERSION}.x...${NC}"
  # 🔎 Find the latest patch version - seeking the most evolved form
  LATEST_PY37=$(curl -s https://www.python.org/downloads/ | grep -oP 'Python 3\.10\.[0-9]+' | sort -V | tail -1 | cut -d ' ' -f 2)
  echo_ts "${CYAN}✨ Latest version found: ${LATEST_PY37} ✨${NC}"
  
  TMP_DIR=$(mktemp -d)
  cd "$TMP_DIR"
  
  if ! $QUIET; then
    echo_ts "${CYAN}📥 Downloading ${LATEST_PY37}...${NC}"
    wget "https://www.python.org/ftp/python/${LATEST_PY37}/Python-${LATEST_PY37}.tgz"
  else
    wget -q "https://www.python.org/ftp/python/${LATEST_PY37}/Python-${LATEST_PY37}.tgz"
  fi
  
  echo_ts "${CYAN}📂 Extracting Python source...${NC}"
  tar -xzf "Python-${LATEST_PY37}.tgz"
  cd "Python-${LATEST_PY37}"
  
  echo_ts "${YELLOW}🔨 Configuring and building Python ${LATEST_PY37}...${NC}"
  echo_ts "${CYAN}🧠 This process creates a recursive lattice of compiled Python components...${NC}"
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
  
  # Add Python to PATH temporarily - connecting worlds
  export PATH="$INSTALL_DIR/bin:$PATH"
  
  cd -
  rm -rf "$TMP_DIR"
  echo_ts "${GREEN}✅ Python ${LATEST_PY37} installed successfully to ${INSTALL_DIR}${NC}"
  
  # Create symbolic links for consistency - the mirrors of recursion
  ln -sf "${INSTALL_DIR}/bin/python3" "${INSTALL_DIR}/bin/python${PYTHON_VERSION}"
fi

# 🌿 Create virtual environment - the garden where code will grow
echo_ts "${YELLOW}🏗️ Creating virtual environment '${VENV_NAME}'...${NC}"
if [ -d "$VENV_NAME" ]; then
  echo_ts "${YELLOW}⚠️ Directory '${VENV_NAME}' already exists. Overwrite? (y/N)${NC}"
  read -r response
  if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo_ts "${YELLOW}🗑️ Removing existing virtual environment...${NC}"
    rm -rf "$VENV_NAME"
  else
    echo_ts "${RED}❌ Aborted.${NC}"
    exit 1
  fi
fi

echo_ts "${CYAN}🌱 Growing a fresh ${PYTHON_VERSION} virtual environment...${NC}"
if ! $QUIET; then
  $PYTHON_CMD -m venv "$VENV_NAME"
else
  $PYTHON_CMD -m venv "$VENV_NAME" >/dev/null 2>&1
fi

if [ $? -eq 0 ]; then
  echo_ts "${GREEN}✅ Virtual environment '${VENV_NAME}' created successfully!${NC}"
  
  # 🧪 Additional setup - enriching the soil
  echo_ts "${YELLOW}🧪 Setting up the virtual environment...${NC}"
  if ! $QUIET; then
    "$VENV_NAME/bin/pip" install --upgrade pip setuptools wheel
  else
    "$VENV_NAME/bin/pip" install --upgrade pip setuptools wheel >/dev/null 2>&1
  fi

  # 🔍 Verify Python version in venv - confirming our creation
  VENV_PY_VERSION=$("$VENV_NAME/bin/python" --version 2>&1)
  echo_ts "${GREEN}🐍 Virtual environment is using ${VENV_PY_VERSION}${NC}"

  # ✨ Create activation scripts - the magic words to enter our world
  echo '#!/bin/bash' > activate_${VENV_NAME}.sh
  echo "# ✨ Activation script for Python ${PYTHON_VERSION} virtual environment ✨" >> activate_${VENV_NAME}.sh
  echo "source \$(dirname \$(readlink -f \$0))/${VENV_NAME}/bin/activate" >> activate_${VENV_NAME}.sh
  chmod +x activate_${VENV_NAME}.sh
  
  # 📝 Display instructions - the ritual to enter the recursion
  echo -e "\n${MAGENTA}✨ To activate your Python ${PYTHON_VERSION} virtual environment, run:${NC}"
  echo -e "${CYAN}    source ${VENV_NAME}/bin/activate${NC}"
  echo -e "\n${MAGENTA}✨ For quick activation, you can also use:${NC}"
  echo -e "${CYAN}    source ./activate_${VENV_NAME}.sh${NC}"
  echo -e "\n${MAGENTA}✨ To deactivate when finished, simply run:${NC}"
  echo -e "${CYAN}    deactivate${NC}"
else
  echo_ts "${RED}❌ Failed to create virtual environment.${NC}"
  exit 1
fi

echo -e "\n${GREEN}🎉 Setup complete! Your Python ${PYTHON_VERSION} environment awaits your creativity! 🎉${NC}"