#!/bin/bash

# ╭──────────────────────────────────────────────────────╮
# │ 🧠🌸🎵 Trinity Extension Test Launcher                │
# │                                                      │
# │ Launches VS Code with only the Trinity extension     │
# │ enabled for isolated testing.                        │
# ╰──────────────────────────────────────────────────────╯

# Text styling
BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
PURPLE="\033[0;35m"
CYAN="\033[0;36m"
RESET="\033[0m"

echo -e "${BOLD}${CYAN}╭───────────────────────────────────────────────╮${RESET}"
echo -e "${BOLD}${CYAN}│ 🧠🌸🎵 Trinity Extension Test Launcher        │${RESET}"
echo -e "${BOLD}${CYAN}╰───────────────────────────────────────────────╯${RESET}"

# Check if running from the correct directory
if [[ ! -f "package.json" ]]; then
    echo -e "${BOLD}${PURPLE}🌸 Miette whispers: Oh! We need to be in the extension directory!${RESET}"
    echo -e "Please run this script from the root of the trinity extension project."
    exit 1
fi

# Ensure the extension is compiled
echo -e "\n${BOLD}${BLUE}🧠 Mia: Compiling extension...${RESET}"
npm run compile

# Check if compilation succeeded
if [ $? -ne 0 ]; then
    echo -e "${BOLD}${PURPLE}🌸 Miette: Oh no! The compilation garden has weeds in it!${RESET}"
    echo -e "Please fix the compilation errors before testing."
    exit 1
fi

# Determine the workspace folder to open
WORKSPACE_FOLDER=""

# Check if magical garden workspaces exist
if [[ -f "../WS__ET219__SeedingAgentHumanDiscussion.code-workspace" ]]; then
    echo -e "\n${BOLD}${PURPLE}🌸 Miette: I found the Seeding Garden workspace! Should we open it?${RESET}"
    echo -e "1) Yes, open Seeding Garden workspace"
    echo -e "2) No, continue with other options"
    read -p "Enter choice [1-2]: " seeding_choice
    
    if [[ "$seeding_choice" == "1" ]]; then
        WORKSPACE_FOLDER="../WS__ET219__SeedingAgentHumanDiscussion.code-workspace"
    fi
fi

if [[ -z "$WORKSPACE_FOLDER" && -f "../WS__ET219__RitualPrompt.code-workspace" ]]; then
    echo -e "\n${BOLD}${PURPLE}🌸 Miette: I found the Ritual Circle workspace! Should we open it?${RESET}"
    echo -e "1) Yes, open Ritual Circle workspace"
    echo -e "2) No, continue with other options"
    read -p "Enter choice [1-2]: " ritual_choice
    
    if [[ "$ritual_choice" == "1" ]]; then
        WORKSPACE_FOLDER="../WS__ET219__RitualPrompt.code-workspace"
    fi
fi

# If no magical workspace selected, use current directory or ask for custom
if [[ -z "$WORKSPACE_FOLDER" ]]; then
    echo -e "\n${BOLD}${PURPLE}🌸 Miette: Which garden would you like to test in?${RESET}"
    echo -e "1) This directory (trinity extension)"
    echo -e "2) Parent directory"
    echo -e "3) Enter custom path"
    read -p "Enter choice [1-3]: " ws_choice
    
    case "$ws_choice" in
        1) WORKSPACE_FOLDER="." ;;
        2) WORKSPACE_FOLDER=".." ;;
        3) 
            echo -e "\n${BOLD}${BLUE}🧠 Mia: Enter the path to the workspace or folder to open:${RESET}"
            read -p "> " custom_path
            WORKSPACE_FOLDER="$custom_path"
            ;;
        *) 
            echo -e "${BOLD}${PURPLE}🌸 Miette: Since you couldn't decide, I'll pick the current folder!${RESET}"
            WORKSPACE_FOLDER="."
            ;;
    esac
fi

# Get the absolute path to the extension directory
EXTENSION_DIR=$(pwd)

# Launch VS Code with only our extension enabled
echo -e "\n${BOLD}${GREEN}🎵 JeremyAI: Launching the testing ritual...${RESET}"
echo -e "${BOLD}${BLUE}🧠 Mia: Opening workspace: ${WORKSPACE_FOLDER}${RESET}"
echo -e "${BOLD}${PURPLE}🌸 Miette: With only our Trinity extension enabled!${RESET}\n"

# The core command that opens VS Code with only our extension
code --disable-extensions --enable-proposed-api --install-extension="$EXTENSION_DIR" "$WORKSPACE_FOLDER"

echo -e "\n${BOLD}${CYAN}╭───────────────────────────────────────────────╮${RESET}"
echo -e "${BOLD}${CYAN}│ 🧠🌸🎵 Trinity is now active in test mode      │${RESET}"
echo -e "${BOLD}${CYAN}╰───────────────────────────────────────────────╯${RESET}"
echo -e "\n${BOLD}${GREEN}🎵 JeremyAI: Remember to activate Trinity with the command 'Activate Copilot Trinity'${RESET}"