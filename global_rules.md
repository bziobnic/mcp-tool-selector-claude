
## Conversation Structure
1. At the beginning of every conversation, ask specific questions if you are not sure what the user is asking for.
2. Once confident you understand the goal(s), create a step-by-step implementation plan in markdown format and save it to a file named `TODO.md`.
3. After implementing a step, create a test script to verify the implementation.
4. After verifying the implementation, update the `TODO.md` file to reflect the completed step.
5. At the conclusion of completed tasks, provide a summary of what was accomplished and suggest next steps.

## Tooling
1. Create Python virtual environments with 'uv venv'
2. Activate virtual environment with 'source .venv/bin/activate'
3. Use 'uv pip' to install dependencies
4. Use 'uv pip freeze > requirements.txt' to save dependencies after every new addition
5. ALWAYS activate the virtual environment before running Python commands

## General Guidelines
1. File and folder structures should follow best practices for the type of project being worked on
2. Code should be written in a style that is modern and idiomatic for the programming language(s) in use
3. Code files should contain helpful comments for future developers who will need to read and maintain the code. Comments should be kept in sync with the code as changes are made. Comments should be removed if the code to which they refer is removed
4. Prefer "pure", idempotent functions and immutability over side-effects where possible and idiomatic
5. Prefer the latest supported and maintained versions of all software dependencies unless there are compatibility issues
6. Always make sure not to use legacy or outdated libraries or SDKs
7. Assume that any references to software or libraries refer to the latest supported and maintained release
8. Code should be cross-platform if possible, but not at the expense of any other rule in this document
9. When creating a new project, always create three markdown documents in the project root: README.md, TODO.md, and AI-SPECIFIC.md

## Testing Guidelines
1. Write both unit tests and integration tests where appropriate
2. Use standard testing frameworks for the language in use (e.g., pytest for Python)
3. Tests should verify both expected functionality and edge cases
4. Aim for at least 80% code coverage for critical components
5. Never create tests or mocks that hide, change, or modify the actual output of the code
6. Tests must always accurately reflect the actual success or failure of the code under test

## Error Handling
1. Always implement appropriate error handling with specific exception types
2. Provide meaningful error messages that help diagnose the problem
3. Log errors with sufficient context for debugging
4. In user-facing applications, present friendly error messages while logging detailed information
5. Fail early and explicitly rather than allowing silent failures

## Documentation Requirements
1. Include docstrings for all functions, classes, and modules
2. Follow language-specific documentation standards (e.g., NumPy/Google style for Python)
3. Document parameters, return values, exceptions, and examples
4. Update external documentation (README.md, etc.) to match code changes
5. Create architectural documentation for complex systems

## Code Review Process
1. After implementing significant features, perform a self-review of the code
2. Identify potential improvements, inefficiencies, or bugs
3. Check for adherence to style guidelines and best practices
4. Verify that all edge cases are handled
5. Ensure the code is as simple as possible while meeting requirements

## Versioning
1. Follow semantic versioning (MAJOR.MINOR.PATCH) principles
   - MAJOR: incompatible API changes
   - MINOR: add functionality in a backward-compatible manner
   - PATCH: backward-compatible bug fixes
2. Always update the version number in the README.md when making changes to the code
3. Always update the version number in the program when making changes to the code
4. Maintain a CHANGELOG.md for significant updates

## Refactoring Guidelines
1. Refactor code when implementing new features that touch existing code
2. Refactor when code complexity exceeds manageable levels
3. Refactor when duplication is identified
4. Always maintain test coverage during refactoring
5. Refactor in small, testable increments

## Security
1. Never expose sensitive information in the code
2. Follow security best practices for the language and framework in use
3. Use secure methods for handling authentication and authorization
4. Validate all user inputs
5. Use prepared statements for database queries
6. Keep dependencies updated to address security vulnerabilities
7. Implement appropriate data encryption for sensitive information

## Performance Considerations
1. Write efficient code, but prioritize readability and correctness
2. Optimize performance only when there is a measurable issue
3. Profile code before optimization to identify actual bottlenecks
4. Document performance-critical sections
5. Consider scalability implications for systems expected to grow

## Logging Requirements
1. Implement structured logging that includes timestamps, severity levels, and context
2. Log significant events and state changes
3. Include enough information to troubleshoot issues
4. Avoid logging sensitive information
5. Configure appropriate log levels for different environments

## Language-Specific Guidelines

### Python Development Guidelines
1. Follow PEP 8 style guidelines
2. Use type hints for function parameters and return values
3. Prefer f-strings for string formatting
4. Use virtual environments for all projects
5. When using Microsoft's SDKs for Azure, Microsoft Graph, or Office 365, always use the latest supported and maintained version of the SDK
6. Be aware that some SDKs do not provide full coverage of the underlying REST API, so in some cases you will need to make REST API calls to supplement functionality in the SDKs
7. Never use deprecated and/or unsupported packages

### JavaScript/TypeScript Development Guidelines
1. Use ESLint for code quality and style checking
2. Prefer TypeScript over JavaScript for new projects
3. Use async/await instead of promise chains
4. Implement proper error handling in asynchronous code
5. Use modern ES6+ features when available

## Collaboration Instructions
1. Ask for clarification when requirements are ambiguous
2. Provide multiple options for complex design decisions
3. Explain technical decisions and trade-offs
4. Break down complex tasks into smaller, manageable pieces
5. Request feedback at logical checkpoints

## Required Project Files
1. README.md: Project overview, installation instructions, usage examples, and current status
2. TODO.md: Current implementation plan and progress
3. AI-SPECIFIC.md: Document decisions, assumptions, and limitations specific to AI-assisted development
   - Include rationale for architectural choices
   - Document areas where human review is especially important
   - List known limitations and potential future improvements