# Jarvis: An AI Assistant with Collaborative Agents

This folder contains the Jarvis AI assistant implementation, which demonstrates the use of collaborative specialized agents to solve complex tasks.

## Overview

Jarvis uses a collaborative agent pattern where:

1. Multiple specialized agents work together on different aspects of a task:
   - **Coordinator (Main Agent)**: Manages the workflow and integrates results
   - **Researcher (Browser Agent)**: Gathers information from the web
   - **Engineer (SWE Agent)**: Plans and implements technical solutions

2. The workflow follows a defined sequence:
   - Task planning by coordinator
   - Information gathering by researcher
   - Implementation planning by engineer
   - Implementation of the solution
   - Final integration of all components

## Running Jarvis

To run Jarvis, make sure you have installed all the dependencies and simply run:

```bash
python examples/jarvis.py
```

When prompted, enter your task or question. Jarvis will:
1. Break it down into sub-tasks
2. Research relevant information
3. Plan and implement a solution
4. Integrate everything into a comprehensive response

## Example Tasks

Jarvis works best with tasks that require both research and technical implementation, such as:

- "Create a Python function to analyze sentiment in tweets"
- "Build a tool to convert CSV data to JSON format"
- "Design a basic web scraper for product information"
- "Implement a simple recommendation algorithm"

## Configuration

Jarvis uses the YAML configuration files in `config/prompts/` for agent prompts and behaviors, allowing for easy customization without code changes. 