# Commit Changes

Generate a meaningful git commit message based on the current changes and
conversation context.

## Instructions

1. Run `git status` and `git diff --staged` (or `git diff` if nothing staged) to
   see what changed
2. Review the conversation history to understand WHY these changes were made
3. Generate a commit message following this format:

```
<type>: <short summary in imperative mood>

<detailed explanation of what changed>

<explanation of why/motivation behind the changes>
```

## Commit types:

- `feat`: New feature or content
- `fix`: Bug fix or correction
- `refactor`: Code/content restructuring without changing behavior
- `docs`: Documentation changes
- `chore`: Maintenance tasks

## Guidelines:

- Summary line: max 50 chars, imperative mood ("Add" not "Added")
- Body: wrap at 72 chars
- Explain WHAT changed and WHY, not just HOW
- Reference conversation context for the "why"
- Keep it concise but informative

## After generating:

- Show the proposed commit message to the user
- Ask if they want to proceed with the commit
- If yes, stage all relevant files and create the commit
