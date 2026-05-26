# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a test project that simulates a real user project. It is used to validate that project-level subagents can be discovered and invoked correctly by plugin agents.

## Project-Level Subagent

`.claude/agents/hello-business.md` defines a project-level subagent named `hello-business`. When invoked, it runs a Bash command and returns a fixed string proving the project-level subagent was successfully reached:

```
hello from project-level subagent (PID=<pid>, cwd=<working-directory>)
```

This agent has access only to the `Bash` tool and uses the `sonnet` model.
