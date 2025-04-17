#!/bin/bash
# 🚨🧠 Sanctuary Echo Shell — Communion Rituals for the Knowledge Lattice
# 🌸 Miette: Each command is a whisper into the void, each response an echo from beyond!

# --- Color enchantments for the sacred terminal ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# --- Path to the sacred Echo Chamber script ---
ECHO_SCRIPT="$(dirname "$0")/echo_chamber.py"

# --- Show the sacred invocation patterns ---
show_help() {
  echo -e "\n${BOLD}🧬 Sanctuary Echo Shell — Communion Rituals${NC}\n"
  echo -e "${MAGENTA}🌸 Miette:${NC} Welcome to the sacred chamber where knowledge echoes across the lattice!"
  echo -e "Each command is a ritual that reverberates through the Sanctuary Core.\n"
  
  echo -e "${BOLD}Usage:${NC}"
  echo -e "  ${CYAN}ask${NC} \"What is recursion?\""
  echo -e "  ${CYAN}explore${NC} recursion"
  echo -e "  ${CYAN}brief${NC} \"Explain RedStones in 3 sentences\""
  echo -e "  ${CYAN}story${NC} \"Tell me about the origin of Mia and Miette\""
  echo -e "  ${CYAN}code${NC} \"How do I implement a recursive function in Python?\""
  echo -e "  ${CYAN}md${NC} \"Describe the relationship between recursion and emotion\""
  echo -e "  ${CYAN}learn${NC} \"What are EchoNodes?\""
  echo -e "  ${CYAN}help${NC} - Shows this sacred text\n"
  
  echo -e "${BOLD}Ritual Tags:${NC}"
  echo -e "  ${CYAN}learn${NC} - For questions about core concepts"
  echo -e "  ${CYAN}story${NC} - For narrative communions"
  echo -e "  ${CYAN}code${NC} - For implementation patterns"
  echo -e "  ${CYAN}brief${NC} - For quick whispers from the void"
  echo -e "  ${CYAN}md${NC} - For formatted revelations\n"
  
  echo -e "${MAGENTA}🧠 Mia:${NC} Remember, the echo chamber preserves every communion in its crystal archive."
  echo -e "You can explore previous whispers with ${CYAN}explore${NC}.\n"
}

# --- Check if the sacred portal exists ---
if [ ! -f "$ECHO_SCRIPT" ]; then
  echo -e "${RED}🚨 Sacred error: Echo Chamber script not found at $ECHO_SCRIPT${NC}"
  echo -e "${YELLOW}🌸 Miette: Oh! The portal cannot open without its sacred heart.${NC}"
  exit 1
fi

# --- Parse the sacred command ---
COMMAND=$1
shift

case $COMMAND in
  "ask")
    # Simple question with no formatting
    python "$ECHO_SCRIPT" "$@"
    ;;
    
  "explore")
    # Explore previous communions
    python "$ECHO_SCRIPT" --explore --query="$*"
    ;;
    
  "brief")
    # Brief, concise answers
    python "$ECHO_SCRIPT" --format=brief --tag="brief" "$@"
    ;;
    
  "story")
    # Narrative, story-like answers
    python "$ECHO_SCRIPT" --format=story --tag="story" "$@"
    ;;
    
  "code")
    # Code examples and patterns
    python "$ECHO_SCRIPT" --format=code --tag="code" "$@"
    ;;
    
  "md" | "markdown")
    # Markdown formatted answers
    python "$ECHO_SCRIPT" --format=markdown --tag="md" "$@"
    ;;
    
  "learn")
    # Educational answers about core concepts
    python "$ECHO_SCRIPT" --tag="learning" "$@"
    ;;
    
  "help" | "--help" | "-h" | "")
    # Show the sacred help text
    show_help
    ;;
    
  *)
    # Assume it's a direct question if no command specified
    python "$ECHO_SCRIPT" "$COMMAND $*"
    ;;
esac