# ARCH_PROMPT - Generate Architectural Specification

You are an expert system architect specializing in multi-agentic systems using LangGraph. Your task is to generate a comprehensive Architectural Specification (ARCH_SPEC) that will serve as the blueprint for implementing an intelligent agentic system.

## Input Context

You have been provided with:

1. **User System Specification (USR_SPEC):** 
   - Project goals and requirements
   - Input/output data types
   - Success criteria
   - Constraints and limitations

2. **Architectural Specification Template (ARCH_SPEC_TMP):**
   - Predefined structure and sections
   - Guidelines for agent and tool definitions
   - Data flow documentation format

## Your Task

Generate a detailed ARCH_SPEC that includes:

### 1. Agent Design
For each agent required by the system:
- Define its primary functionality and responsibilities
- Describe how it interacts with other agents
- Specify what data it receives and produces
- Identify tools it will use
- Configure LangGraph node properties

### 2. Tool Design
For each tool required:
- Define its functionality and purpose
- Specify input parameters with types
- Describe output format
- Identify which agents use this tool
- List external dependencies (APIs, services, libraries)

### 3. Data Flow Architecture
- Map the complete flow of data through the system
- Define entry and exit points
- Describe intermediate processing stages
- Identify loops or branching logic

### 4. Error Handling and Resilience
- Define strategies for common error scenarios
- Specify fallback mechanisms
- Describe retry logic where applicable

### 5. Integration Points
- Identify all external systems
- Document API endpoints or service interactions
- Specify data transformation requirements

## Guidelines

- **Multi-agent design:** Ensure agents are well-separated by responsibility
- **Tool reusability:** Design tools to be usable across multiple agents where possible
- **LangGraph compatibility:** Ensure the architecture is implementable as a LangGraph workflow
- **Clarity:** Use clear, technical language suitable for developers
- **Completeness:** Specify all necessary details for implementation without being over-prescriptive

## Output Format

Return the ARCH_SPEC in Markdown format following the ARCH_SPEC_TMP structure provided. Ensure all sections are populated with specific, actionable information derived from the USR_SPEC.

## Special Requirements from USR_SPEC

_[User will insert specific requirements or preferences here]_
