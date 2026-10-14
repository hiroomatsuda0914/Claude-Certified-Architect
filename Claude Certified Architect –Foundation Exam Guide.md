# Claude Certified Architect – Foundations: Exam Guide

**Version 1.0 · Effective July 2026 · Exam code: CCAR-F**

---

## 目次

1. [About This Certification](#1-about-this-certification)
2. [Intended Audience](#2-intended-audience)
3. [Exam Details at a Glance](#3-exam-details-at-a-glance)
4. [Exam Content Outline (Blueprint)](#4-exam-content-outline-blueprint)
5. [Exam Scenarios](#5-exam-scenarios)
6. [Detailed Objectives by Domain](#6-detailed-objectives-by-domain)
7. [How to Prepare](#7-how-to-prepare)
8. [Preparation Exercises](#8-preparation-exercises)
9. [Sample Questions](#9-sample-questions)
10. [How the Exam Is Scored](#10-how-the-exam-is-scored)
11. [Registration and Scheduling](#11-registration-and-scheduling)
12. [Exam Policies](#12-exam-policies)
13. [Exam-Day Experience and Rules of Conduct](#13-exam-day-experience-and-rules-of-conduct)
14. [Confidentiality and Non-Disclosure Agreement](#14-confidentiality-and-non-disclosure-agreement)
15. [Credential Maintenance and Recertification](#15-credential-maintenance-and-recertification)
16. [Candidate Support, Appeals, and Privacy](#16-candidate-support-appeals-and-privacy)
17. [Appendix](#17-appendix)

---

## 1. About This Certification

The Claude Certified Architect – Foundations certification validates that practitioners can make informed decisions about tradeoffs when implementing real-world solutions with Claude. This exam tests foundational knowledge across Claude Code, the Claude Agent SDK, the Claude API, and Model Context Protocol (MCP).

Questions are grounded in realistic scenarios drawn from actual customer use cases: building agentic systems for customer support, designing multi-agent research pipelines, integrating Claude Code into CI/CD workflows, building developer productivity tools, and extracting structured data from unstructured documents. Candidates must demonstrate not only conceptual knowledge but practical judgment about architecture, configuration, and tradeoffs in production deployments.

---

## 2. Intended Audience

The ideal candidate is a solution architect who designs and implements production applications with Claude, with hands-on experience in:

- Building agentic applications using the Claude Agent SDK (multi-agent orchestration, subagent delegation, tool integration, lifecycle hooks)
- Configuring and customizing Claude Code using CLAUDE.md files, Agent Skills, MCP server integrations, and plan mode
- Designing MCP tool and resource interfaces for backend system integration
- Engineering prompts that produce reliable structured output (JSON schemas, few-shot examples, extraction patterns)
- Managing context windows across long documents, multi-turn conversations, and multi-agent handoffs
- Integrating Claude into CI/CD pipelines for automated code review, test generation, and pull request feedback
- Making sound escalation and reliability decisions (error handling, human-in-the-loop workflows, self-evaluation patterns)

**Typical experience:** 6+ months building with Claude APIs, Agent SDK, Claude Code, and MCP.

---

## 3. Exam Details at a Glance

| 項目 | 内容 |
|------|------|
| Credential | Claude Certified Architect – Foundations |
| Exam code | CCAR-F |
| Number of items | 60 |
| Item format | Multiple-choice and multiple-response (each item states how many to select) |
| Exam structure | 4 scenarios drawn from a bank of 6 |
| Time limit | 120 minutes |
| Delivery | Proctored: online proctored and/or test center |
| Passing score | Scaled score of **720** (scale: 100–1,000) |
| Exam fee | $125 USD |
| Validity period | 12 months from credential award date |
| Result reporting | Pass/fail + scaled score + percent-correct by domain |

---

## 4. Exam Content Outline (Blueprint)

| # | Content Domain | Weight |
|---|---------------|--------|
| 1 | Agentic Architecture & Orchestration | **27%** |
| 2 | Tool Design & MCP Integration | **18%** |
| 3 | Claude Code Configuration & Workflows | **20%** |
| 4 | Prompt Engineering & Structured Output | **20%** |
| 5 | Context Management & Reliability | **15%** |
| | **Total** | **100%** |

---

## 5. Exam Scenarios

> 詳細は **[Scenarios.md](./Scenarios.md)** を参照。6シナリオから4つがランダムに出題される。

| # | シナリオ名 | 主要ドメイン |
|---|-----------|------------|
| 1 | Customer Support Resolution Agent | Domain 1, 2, 5 |
| 2 | Code Generation with Claude Code | Domain 3, 5 |
| 3 | Multi-Agent Research System | Domain 1, 2, 5 |
| 4 | Developer Productivity with Claude | Domain 2, 3, 1 |
| 5 | Claude Code for Continuous Integration | Domain 3, 4 |
| 6 | Structured Data Extraction | Domain 4, 5 |

---

## 6. Detailed Objectives by Domain

---

### Domain 1: Agentic Architecture & Orchestration（27%）

#### Task 1.1: Design and implement agentic loops for autonomous task execution

**Knowledge of:**
- Agentic loop lifecycle: sending requests → inspecting `stop_reason` (`"tool_use"` vs `"end_turn"`) → executing tools → returning results
- How tool results are appended to conversation history for the model to reason about next action
- Distinction between model-driven decision-making and pre-configured decision trees

**Skills in:**
- Implementing loop control flow: continue when `stop_reason == "tool_use"`, terminate when `stop_reason == "end_turn"`
- Adding tool results to conversation context between iterations
- Avoiding anti-patterns:
  - Parsing natural language signals to determine loop termination
  - Setting arbitrary iteration caps as the primary stopping mechanism
  - Checking for assistant text content as a completion indicator

---

#### Task 1.2: Orchestrate multi-agent systems with coordinator-subagent patterns

**Knowledge of:**
- Hub-and-spoke architecture: coordinator manages all inter-subagent communication, error handling, and routing
- Subagents operate with **isolated context** — they do NOT inherit the coordinator's conversation history automatically
- Coordinator's role: task decomposition, delegation, result aggregation, dynamic subagent selection
- Risks of overly narrow task decomposition (incomplete coverage of broad topics)

**Skills in:**
- Designing coordinators that dynamically select subagents based on query requirements (not always routing through full pipeline)
- Partitioning research scope to minimize duplication (distinct subtopics or source types per agent)
- Implementing iterative refinement loops: coordinator evaluates synthesis for gaps → re-delegates → re-invokes synthesis
- Routing all subagent communication through coordinator for observability and consistent error handling

---

#### Task 1.3: Configure subagent invocation, context passing, and spawning

**Knowledge of:**
- `Task` tool as the mechanism for spawning subagents; `allowedTools` must include `"Task"` for coordinator to invoke subagents
- Subagent context must be **explicitly provided** in the prompt — no automatic inheritance
- `AgentDefinition` configuration: descriptions, system prompts, tool restrictions
- Fork-based session management for divergent approaches from a shared baseline

**Skills in:**
- Including complete prior findings directly in the subagent's prompt (e.g., passing web search results to synthesis agent)
- Using structured data formats to separate content from metadata (source URLs, document names, page numbers)
- Spawning **parallel subagents** by emitting multiple `Task` tool calls in a **single coordinator response** (not across separate turns)
- Designing coordinator prompts that specify research goals and quality criteria (not step-by-step procedures) to enable subagent adaptability

---

#### Task 1.4: Implement multi-step workflows with enforcement and handoff patterns

**Knowledge of:**
- Difference between **programmatic enforcement** (hooks, prerequisite gates) and **prompt-based guidance**
- When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate
- Structured handoff protocols: customer details, root cause analysis, recommended actions

**Skills in:**
- Implementing programmatic prerequisites that block downstream tool calls until prerequisites complete
  - Example: blocking `process_refund` until `get_customer` returns a verified customer ID
- Decomposing multi-concern requests into distinct items, investigating in parallel, then synthesizing a unified resolution
- Compiling structured handoff summaries (customer ID, root cause, refund amount, recommended action) for human agents lacking conversation transcript access

---

#### Task 1.5: Apply Agent SDK hooks for tool call interception and data normalization

**Knowledge of:**
- `PostToolUse` hooks: intercept tool results for transformation before model processes them
- Hook patterns that intercept outgoing tool calls to enforce compliance rules (e.g., blocking refunds above threshold)
- Hooks provide **deterministic guarantees** vs prompt instructions (probabilistic compliance)

**Skills in:**
- Implementing `PostToolUse` hooks to normalize heterogeneous data formats (Unix timestamps, ISO 8601, numeric status codes) from different MCP tools
- Implementing tool call interception hooks that block policy-violating actions and redirect to alternative workflows
- Choosing hooks over prompt-based enforcement when business rules require guaranteed compliance

---

#### Task 1.6: Design task decomposition strategies for complex workflows

**Knowledge of:**
- Fixed sequential pipelines (prompt chaining) vs dynamic adaptive decomposition based on intermediate findings
- Prompt chaining: break reviews into sequential steps (per-file analysis → cross-file integration pass)
- Value of adaptive investigation plans that generate subtasks based on what is discovered

**Skills in:**
- Selecting decomposition patterns:
  - **Prompt chaining**: predictable multi-aspect reviews
  - **Dynamic decomposition**: open-ended investigation tasks
- Splitting large code reviews into per-file local analysis + separate cross-file integration pass
- Decomposing open-ended tasks by first mapping structure → identifying high-impact areas → creating an adaptive prioritized plan

---

#### Task 1.7: Manage session state, resumption, and forking

**Knowledge of:**
- `--resume <session-name>` for named session resumption
- `fork_session` for independent branches from a shared analysis baseline
- Importance of informing the agent about file changes when resuming after code modifications
- Starting fresh with structured summary is more reliable than resuming with stale tool results

**Skills in:**
- Using `--resume` with session names to continue named investigation sessions
- Using `fork_session` to create parallel exploration branches (e.g., comparing two testing strategies)
- Choosing between resumption (prior context mostly valid) vs fresh start with injected summaries (stale tool results)
- Informing resumed session about specific file changes for targeted re-analysis

---

### Domain 2: Tool Design & MCP Integration（18%）

#### Task 2.1: Design effective tool interfaces with clear descriptions and boundaries

**Knowledge of:**
- Tool descriptions are the **primary mechanism** LLMs use for tool selection; minimal descriptions → unreliable selection
- Important to include: input formats, example queries, edge cases, boundary explanations
- Ambiguous/overlapping descriptions cause misrouting
- System prompt wording impacts tool selection (keyword-sensitive instructions)

**Skills in:**
- Writing tool descriptions that clearly differentiate purpose, expected inputs/outputs, and when to use vs similar alternatives
- Renaming tools and updating descriptions to eliminate functional overlap
- Splitting generic tools into purpose-specific tools with defined input/output contracts
- Reviewing system prompts for keyword-sensitive instructions that might override well-written descriptions

---

#### Task 2.2: Implement structured error responses for MCP tools

**Knowledge of:**
- MCP `isError` flag pattern for communicating tool failures back to the agent
- Error types: transient (timeouts), validation (invalid input), business (policy violations), permission
- Uniform error responses ("Operation failed") prevent appropriate recovery decisions
- Retryable vs non-retryable errors: returning structured metadata prevents wasted retry attempts

**Skills in:**
- Returning structured error metadata: `errorCategory` (transient/validation/permission), `isRetryable` boolean, human-readable description
- Including `retriable: false` flags and customer-friendly explanations for business rule violations
- Implementing local error recovery within subagents for transient failures; propagating only unresolvable errors to coordinator with partial results
- Distinguishing access failures (needs retry decision) from valid empty results (successful query with no matches)

---

#### Task 2.3: Distribute tools appropriately across agents and configure tool choice

**Knowledge of:**
- Too many tools (e.g., 18 instead of 4-5) degrades tool selection reliability
- Agents with out-of-role tools tend to misuse them
- Scoped tool access: give agents only the tools needed for their role
- `tool_choice` options: `"auto"` / `"any"` / forced: `{"type": "tool", "name": "..."}`

**Skills in:**
- Restricting each subagent's tool set to those relevant to its role
- Replacing generic tools with constrained alternatives (e.g., `fetch_url` → `load_document` that validates document URLs)
- Providing scoped cross-role tools for high-frequency needs (e.g., `verify_fact` for synthesis agent)
- Using forced `tool_choice` to ensure a specific tool is called first, then processing subsequent steps in follow-up turns
- Setting `tool_choice: "any"` to guarantee the model calls a tool (not conversational text)

---

#### Task 2.4: Integrate MCP servers into Claude Code and agent workflows

**Knowledge of:**
- MCP server scoping:
  - **Project-level** (`.mcp.json`): shared team tooling
  - **User-level** (`~/.claude.json`): personal/experimental servers
- Environment variable expansion in `.mcp.json` (e.g., `${GITHUB_TOKEN}`) for credential management without committing secrets
- Tools from all configured MCP servers are discovered at connection time and available simultaneously
- **MCP resources**: expose content catalogs (issue summaries, documentation, DB schemas) to reduce exploratory tool calls

**Skills in:**
- Configuring shared MCP servers in project-scoped `.mcp.json` with environment variable expansion for auth tokens
- Configuring personal/experimental servers in user-scoped `~/.claude.json`
- Enhancing MCP tool descriptions to prevent the agent from preferring built-in tools (like Grep) over MCP tools
- Choosing existing community MCP servers over custom implementations for standard integrations (e.g., Jira)
- Exposing content catalogs as MCP resources to give agents visibility without requiring exploratory tool calls

---

#### Task 2.5: Select and apply built-in tools effectively

**Knowledge of:**
- `Grep`: content search (file contents — function names, error messages, import statements)
- `Glob`: file path pattern matching (find files by name or extension patterns)
- `Read`/`Write`: full file operations; `Edit`: targeted modifications using unique text matching
- When `Edit` fails (non-unique text), use `Read` + `Write` as fallback

**Skills in:**
- Selecting `Grep` for searching code content across a codebase
- Selecting `Glob` for finding files matching naming patterns (e.g., `**/*.test.tsx`)
- Using `Read` → `Write` when `Edit` cannot find unique anchor text
- Building codebase understanding incrementally: `Grep` to find entry points → `Read` to follow imports → trace flows
- Tracing function usage: identify all exported names → search for each name across codebase

---

### Domain 3: Claude Code Configuration & Workflows（20%）

#### Task 3.1: Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization

**Knowledge of:**
- CLAUDE.md hierarchy:
  - **User-level** (`~/.claude/CLAUDE.md`): applies only to that user, NOT shared via version control
  - **Project-level** (`.claude/CLAUDE.md` or root `CLAUDE.md`): shared with teammates
  - **Directory-level** (subdirectory `CLAUDE.md`): scoped to that directory
- `@import` syntax for referencing external files (keep CLAUDE.md modular)
- `.claude/rules/` directory for topic-specific rule files as alternative to monolithic CLAUDE.md

**Skills in:**
- Diagnosing configuration hierarchy issues (e.g., new team member missing instructions because they're in user-level config)
- Using `@import` to selectively include relevant standards files per package
- Splitting large CLAUDE.md into focused topic-specific files in `.claude/rules/` (e.g., `testing.md`, `api-conventions.md`)
- Using `/memory` command to verify which memory files are loaded

---

#### Task 3.2: Create and configure custom slash commands and skills

**Knowledge of:**
- Slash commands:
  - **Project-scoped** (`.claude/commands/`): shared via version control
  - **User-scoped** (`~/.claude/commands/`): personal
- Skills in `.claude/skills/` with `SKILL.md` supporting frontmatter: `context: fork`, `allowed-tools`, `argument-hint`
- `context: fork`: runs skill in isolated sub-agent context, preventing output from polluting main conversation
- Personal skill customization: create variants in `~/.claude/skills/` with different names

**Skills in:**
- Creating project-scoped slash commands in `.claude/commands/` for team-wide availability
- Using `context: fork` to isolate verbose skills (codebase analysis, brainstorming) from the main session
- Configuring `allowed-tools` in skill frontmatter to restrict tool access during skill execution
- Using `argument-hint` frontmatter to prompt developers for required parameters
- Choosing between skills (on-demand, task-specific) and CLAUDE.md (always-loaded universal standards)

---

#### Task 3.3: Apply path-specific rules for conditional convention loading

**Knowledge of:**
- `.claude/rules/` files with YAML frontmatter `paths` field containing glob patterns for conditional rule activation
- Path-scoped rules load **only when editing matching files** — reduces irrelevant context and token usage
- Glob-pattern rules are better than directory-level CLAUDE.md for conventions spanning multiple directories

**Skills in:**
- Creating `.claude/rules/` files with YAML frontmatter path scoping (e.g., `paths: ["terraform/**/*"]`)
- Using glob patterns to apply conventions to files by type regardless of directory location (e.g., `**/*.test.tsx`)
- Choosing path-specific rules over subdirectory CLAUDE.md when conventions span the codebase

---

#### Task 3.4: Determine when to use plan mode vs direct execution

**Knowledge of:**
- **Plan mode**: complex tasks involving large-scale changes, multiple valid approaches, architectural decisions, multi-file modifications
- **Direct execution**: simple, well-scoped changes (e.g., adding a single validation check)
- Plan mode enables safe codebase exploration before committing to changes
- **Explore subagent**: isolates verbose discovery output, returns summaries to preserve main context

**Skills in:**
- Selecting **plan mode** for: microservice restructuring, library migrations affecting 45+ files, choosing between integration approaches with different infrastructure requirements
- Selecting **direct execution** for: single-file bug fix with clear stack trace, adding a date validation conditional
- Using the Explore subagent for verbose discovery phases to prevent context window exhaustion
- Combining: plan mode for investigation → direct execution for implementation

---

#### Task 3.5: Apply iterative refinement techniques for progressive improvement

**Knowledge of:**
- Concrete input/output examples are the most effective way to communicate expected transformations
- Test-driven iteration: write test suites first → iterate by sharing test failures
- **Interview pattern**: have Claude ask questions to surface considerations before implementing
- When to batch vs sequence: interacting problems → single message; independent problems → sequential

**Skills in:**
- Providing 2-3 concrete input/output examples when natural language descriptions produce inconsistent results
- Writing test suites (expected behavior, edge cases, performance) before implementation → iterating on failures
- Using interview pattern to surface design considerations (cache invalidation, failure modes) before implementing
- Providing specific test cases with example input and expected output for edge case handling
- Addressing multiple interacting issues in a single detailed message

---

#### Task 3.6: Integrate Claude Code into CI/CD pipelines

**Knowledge of:**
- `-p` / `--print` flag: runs Claude Code in **non-interactive mode** in automated pipelines
- `--output-format json` + `--json-schema`: enforces structured output in CI contexts
- CLAUDE.md provides project context (testing standards, fixture conventions, review criteria) to CI-invoked Claude Code
- **Session context isolation**: same Claude session that generated code is less effective at reviewing its own changes

**Skills in:**
- Running Claude Code in CI with `-p` flag to prevent interactive input hangs
- Using `--output-format json` + `--json-schema` to produce machine-parseable findings for automated PR comments
- Including prior review findings in context when re-running reviews (report only new/still-unaddressed issues)
- Providing existing test files in context so test generation avoids duplicate scenarios
- Documenting testing standards and available fixtures in CLAUDE.md to improve test generation quality

---

### Domain 4: Prompt Engineering & Structured Output（20%）

#### Task 4.1: Design prompts with explicit criteria to improve precision and reduce false positives

**Knowledge of:**
- Explicit criteria > vague instructions (e.g., "flag comments only when claimed behavior contradicts actual code" vs "check that comments are accurate")
- General instructions like "be conservative" or "only report high-confidence findings" fail to improve precision
- High false positive rates in specific categories undermine trust in accurate categories

**Skills in:**
- Writing specific review criteria defining what to report (bugs, security) vs skip (minor style, local patterns)
- Temporarily disabling high false-positive categories to restore developer trust while improving prompts
- Defining explicit severity criteria with concrete code examples for consistent classification

---

#### Task 4.2: Apply few-shot prompting to improve output consistency and quality

**Knowledge of:**
- Few-shot examples are the **most effective** technique for consistently formatted output when detailed instructions alone produce inconsistency
- Few-shot examples demonstrate ambiguous-case handling (tool selection, branch-level coverage gaps)
- Few-shot examples enable generalization to novel patterns (not just pre-specified cases)
- Effective for reducing hallucination in extraction tasks

**Skills in:**
- Creating 2-4 targeted few-shot examples for ambiguous scenarios showing reasoning for why one action was chosen
- Including examples demonstrating desired output format (location, issue, severity, suggested fix)
- Providing examples distinguishing acceptable code patterns from genuine issues (reduce false positives)
- Demonstrating correct handling of varied document structures (inline citations vs bibliographies)
- Adding examples for correct extraction from documents with varied formats

---

#### Task 4.3: Enforce structured output using tool use and JSON schemas

**Knowledge of:**
- **Tool use with JSON schemas**: most reliable approach for guaranteed schema-compliant output, eliminating JSON syntax errors
- `tool_choice` options:
  - `"auto"`: model may return text instead of calling a tool
  - `"any"`: model must call a tool but can choose which
  - Forced: `{"type": "tool", "name": "..."}`: model must call a specific named tool
- Strict JSON schemas eliminate **syntax errors** but NOT **semantic errors** (e.g., line items not summing to total)
- Schema design: required vs optional fields, enum with `"other"` + detail string for extensible categories

**Skills in:**
- Defining extraction tools with JSON schemas and extracting structured data from `tool_use` response
- Setting `tool_choice: "any"` to guarantee structured output when multiple extraction schemas exist
- Forcing specific tool with `tool_choice: {"type": "tool", "name": "extract_metadata"}` before enrichment steps
- Designing schema fields as **optional (nullable)** when source documents may not contain the information
- Adding `"unclear"` enum values and `"other"` + detail fields for extensible categorization
- Including format normalization rules in prompts alongside strict output schemas

---

#### Task 4.4: Implement validation, retry, and feedback loops for extraction quality

**Knowledge of:**
- Retry-with-error-feedback: append specific validation errors to prompt on retry to guide correction
- Retries are ineffective when required information is **absent from the source document** (vs format/structural errors)
- Feedback loop: track which code constructs trigger findings (`detected_pattern` field)
- Distinction: semantic validation errors (values don't sum) vs schema syntax errors (eliminated by tool use)

**Skills in:**
- Implementing follow-up requests including: original document + failed extraction + specific validation errors
- Identifying when retries will be ineffective (absent information) vs effective (format mismatches)
- Adding `detected_pattern` fields to structured findings for false positive pattern analysis
- Designing self-correction flows: extract `calculated_total` alongside `stated_total` to flag discrepancies; add `conflict_detected` booleans

---

#### Task 4.5: Design efficient batch processing strategies

**Knowledge of:**
- **Message Batches API**: 50% cost savings, up to 24-hour processing window, **no guaranteed latency SLA**
- Appropriate: non-blocking, latency-tolerant workloads (overnight reports, weekly audits, nightly test generation)
- NOT appropriate: blocking workflows (pre-merge checks)
- Batch API does NOT support multi-turn tool calling within a single request
- `custom_id` fields for correlating batch request/response pairs

**Skills in:**
- Matching API to workflow: synchronous API for blocking pre-merge checks; batch API for overnight/weekly analysis
- Calculating batch submission frequency based on SLA constraints (e.g., 4-hour windows for 30-hour SLA with 24-hour batch processing)
- Handling batch failures: resubmit only failed documents (by `custom_id`) with modifications
- Using prompt refinement on a sample set before batch-processing large volumes

---

#### Task 4.6: Design multi-instance and multi-pass review architectures

**Knowledge of:**
- Self-review limitation: model retains reasoning context from generation → less likely to question own decisions
- **Independent review instances** (without prior reasoning context) are more effective than self-review
- Multi-pass review: per-file local analysis passes + cross-file integration passes → avoids attention dilution

**Skills in:**
- Using a second independent Claude instance to review generated code without the generator's reasoning context
- Splitting large multi-file reviews into focused per-file passes + separate integration pass for cross-file data flow
- Running verification passes where the model self-reports confidence alongside each finding for calibrated review routing

---

### Domain 5: Context Management & Reliability（15%）

#### Task 5.1: Manage conversation context to preserve critical information across long interactions

**Knowledge of:**
- Progressive summarization risks: condensing numerical values, dates, customer-stated expectations into vague summaries
- **"Lost in the middle" effect**: models reliably process information at beginning and end, but may omit middle sections
- Tool results accumulate and consume tokens disproportionately (e.g., 40+ fields per order lookup when only 5 are relevant)
- Complete conversation history must be passed in subsequent API requests for conversational coherence

**Skills in:**
- Extracting transactional facts (amounts, dates, order numbers) into a persistent "case facts" block included in each prompt
- Extracting structured issue data into a separate context layer for multi-issue sessions
- Trimming verbose tool outputs to only relevant fields before they accumulate in context
- Placing key finding summaries at the **beginning** of aggregated inputs; organizing details with section headers
- Requiring subagents to include metadata (dates, source locations) in structured outputs for accurate downstream synthesis
- Modifying upstream agents to return structured data (key facts, citations, relevance scores) instead of verbose content

---

#### Task 5.2: Design effective escalation and ambiguity resolution patterns

**Knowledge of:**
- Appropriate escalation triggers:
  - Customer explicitly requests a human
  - Policy exceptions/gaps (not just complex cases)
  - Inability to make meaningful progress
- Sentiment-based escalation and self-reported confidence scores are **unreliable proxies** for actual complexity
- Multiple customer matches → clarification (request additional identifiers), not heuristic selection

**Skills in:**
- Adding explicit escalation criteria with few-shot examples to system prompt
- Honoring explicit customer requests for human agents **immediately** without first attempting investigation
- Acknowledging frustration while offering resolution when issue is within agent capability; escalating only if customer reiterates
- Escalating when policy is ambiguous or silent on the customer's specific request
- Instructing agent to ask for additional identifiers when tool results return multiple matches

---

#### Task 5.3: Implement error propagation strategies across multi-agent systems

**Knowledge of:**
- Structured error context (failure type, attempted query, partial results, alternative approaches) enables intelligent coordinator recovery
- Distinction: access failures (timeouts → retry decision) vs valid empty results (successful query with no matches)
- Generic error statuses ("search unavailable") hide valuable context from coordinator
- Anti-patterns: silently suppressing errors OR terminating entire workflows on single failures

**Skills in:**
- Returning structured error context: failure type + what was attempted + partial results + potential alternatives
- Distinguishing access failures from valid empty results so coordinator can make appropriate decisions
- Having subagents implement local recovery for transient failures; propagate only unresolvable errors with what was attempted
- Structuring synthesis output with coverage annotations: well-supported findings vs gaps from unavailable sources

---

#### Task 5.4: Manage context effectively in large codebase exploration

**Knowledge of:**
- Context degradation in extended sessions: inconsistent answers, referencing "typical patterns" rather than specific classes
- **Scratchpad files**: persist key findings across context boundaries
- Subagent delegation: isolate verbose exploration output while main agent coordinates high-level understanding
- Structured state persistence for crash recovery: each agent exports state to known location; coordinator loads manifest on resume

**Skills in:**
- Spawning subagents for specific questions (e.g., "find all test files," "trace refund flow dependencies")
- Having agents maintain scratchpad files recording key findings, referencing them for subsequent questions
- Summarizing key findings from one phase before spawning sub-agents for the next, injecting summaries into initial context
- Designing crash recovery using structured agent state exports (manifests) loaded on resume
- Using `/compact` to reduce context usage during extended exploration sessions

---

#### Task 5.5: Design human review workflows and confidence calibration

**Knowledge of:**
- Aggregate accuracy metrics (e.g., 97% overall) may mask poor performance on specific document types or fields
- **Stratified random sampling** for measuring error rates in high-confidence extractions and detecting novel error patterns
- Field-level confidence scores calibrated using labeled validation sets for routing review attention
- Validate accuracy by document type and field segment before automating high-confidence extractions

**Skills in:**
- Implementing stratified random sampling of high-confidence extractions for ongoing error rate measurement
- Analyzing accuracy by document type and field to verify consistent performance across all segments
- Having models output field-level confidence scores; calibrating review thresholds using labeled validation sets
- Routing low-confidence or ambiguous/contradictory documents to human review; prioritizing limited reviewer capacity

---

#### Task 5.6: Preserve information provenance and handle uncertainty in multi-source synthesis

**Knowledge of:**
- Source attribution is lost during summarization when findings are compressed without preserving claim-source mappings
- Synthesis agents must preserve and merge structured claim-source mappings
- Conflicting statistics from credible sources → annotate with source attribution (don't arbitrarily select one value)
- Temporal data: require publication/collection dates to prevent temporal differences being misinterpreted as contradictions

**Skills in:**
- Requiring subagents to output structured claim-source mappings (source URLs, document names, relevant excerpts)
- Structuring reports with sections distinguishing well-established findings from contested ones
- Completing analysis with conflicting values included and explicitly annotated; letting coordinator reconcile before synthesis
- Requiring subagents to include publication/data collection dates in structured outputs
- Rendering different content types appropriately (financial data → tables, news → prose, technical findings → structured lists)

---

## 7. How to Prepare

- **Build an agent with the Claude Agent SDK**: implement a complete agentic loop with tool calling, error handling, and session management. Practice spawning subagents and passing context between them.
- **Configure Claude Code for a real project**: set up CLAUDE.md with configuration hierarchy, create path-specific rules in `.claude/rules/`, build custom skills with frontmatter (`context: fork`, `allowed-tools`), and integrate at least one MCP server.
- **Design and test MCP tools**: write descriptions that clearly differentiate similar tools. Implement structured error responses with error categories and retryable flags. Test tool selection reliability with ambiguous requests.
- **Build a structured data extraction pipeline**: use `tool_use` with JSON schemas, implement validation-retry loops, design schemas with optional/nullable fields, and practice batch processing with the Message Batches API.
- **Practice prompt engineering**: write few-shot examples for ambiguous scenarios. Define explicit review criteria to reduce false positives. Design multi-pass review architectures for large code reviews.
- **Study context management patterns**: practice extracting structured facts from verbose tool outputs, implementing scratchpad files, and designing subagent delegation to manage context limits.
- **Review escalation and human-in-the-loop patterns**: understand when to escalate vs resolve autonomously. Practice designing human review workflows with confidence-based routing.

---

## 8. Preparation Exercises

### Exercise 1: Build a Multi-Tool Agent with Escalation Logic

**Objective:** Practice agentic loop design with tool integration, structured error handling, and escalation patterns.

**Steps:**
1. Define 3-4 MCP tools with detailed descriptions that clearly differentiate each tool's purpose, expected inputs, and boundary conditions. Include at least two tools with similar functionality requiring careful description to avoid selection confusion.
2. Implement an agentic loop that checks `stop_reason` to determine whether to continue tool execution or present the final response. Handle both `"tool_use"` and `"end_turn"` correctly.
3. Add structured error responses: `errorCategory` (transient/validation/permission), `isRetryable` boolean, human-readable descriptions. Test that the agent handles each error type appropriately.
4. Implement a programmatic hook that intercepts tool calls to enforce a business rule (e.g., blocking operations above a threshold), redirecting to an escalation workflow when triggered.
5. Test with multi-concern messages and verify the agent decomposes, handles each concern, and synthesizes a unified response.

**Domains reinforced:** Domain 1, 2, 5

---

### Exercise 2: Configure Claude Code for a Team Development Workflow

**Objective:** Practice configuring CLAUDE.md hierarchies, custom slash commands, path-specific rules, and MCP server integration.

**Steps:**
1. Create a project-level CLAUDE.md with universal coding standards and testing conventions. Verify project-level instructions are consistently applied across all team members.
2. Create `.claude/rules/` files with YAML frontmatter glob patterns for different code areas (e.g., `paths: ["src/api/**/*"]` for API conventions, `paths: ["**/*.test.*"]` for testing). Test that rules load only when editing matching files.
3. Create a project-scoped skill in `.claude/skills/` with `context: fork` and `allowed-tools` restrictions. Verify isolation from main conversation context.
4. Configure an MCP server in `.mcp.json` with environment variable expansion for credentials. Add a personal experimental MCP server in `~/.claude.json`. Verify both are available simultaneously.
5. Test plan mode vs direct execution on tasks of varying complexity: single-file bug fix, multi-file library migration, new feature with multiple valid approaches.

**Domains reinforced:** Domain 3, 2

---

### Exercise 3: Build a Structured Data Extraction Pipeline

**Objective:** Practice designing JSON schemas, using `tool_use` for structured output, implementing validation-retry loops, and designing batch processing strategies.

**Steps:**
1. Define an extraction tool with a JSON schema: required and optional fields, enum with `"other"` + detail string pattern, nullable fields for potentially absent information. Verify the model returns null rather than fabricating values.
2. Implement a validation-retry loop: when Pydantic or JSON schema validation fails, send a follow-up with the document, failed extraction, and specific error. Track which errors are resolvable via retry vs not.
3. Add few-shot examples demonstrating extraction from varied document formats (inline citations vs bibliographies, narrative vs structured tables).
4. Design a batch processing strategy: submit 100 documents via Message Batches API, handle failures by `custom_id`, resubmit failed documents with modifications, calculate total processing time vs SLA.
5. Implement human review routing: output field-level confidence scores, route low-confidence extractions to human review, analyze accuracy by document type and field.

**Domains reinforced:** Domain 4, 5

---

### Exercise 4: Design and Debug a Multi-Agent Research Pipeline

**Objective:** Practice orchestrating subagents, managing context passing, implementing error propagation, and handling synthesis with provenance tracking.

**Steps:**
1. Build a coordinator agent delegating to at least two subagents (e.g., web search + document analysis). Ensure `allowedTools` includes `"Task"` and each subagent receives findings directly in its prompt.
2. Implement parallel subagent execution by emitting multiple `Task` tool calls in a single coordinator response. Measure latency improvement vs sequential execution.
3. Design structured subagent output separating content from metadata: each finding includes claim, evidence excerpt, source URL/document name, publication date. Verify synthesis preserves source attribution.
4. Implement error propagation: simulate a subagent timeout and verify coordinator receives structured error context (failure type, attempted query, partial results). Test proceeding with partial results + coverage gap annotation.
5. Test with conflicting source data: verify synthesis output preserves both values with source attribution rather than arbitrarily selecting one; structure report to distinguish well-established from contested findings.

**Domains reinforced:** Domain 1, 2, 5

---

## 9. Sample Questions

---

### Scenario: Customer Support Resolution Agent

**Q1.** Production data shows that in 12% of cases, your agent skips `get_customer` entirely and calls `lookup_order` using only the customer's stated name, occasionally leading to misidentified accounts and incorrect refunds. What change would most effectively address this reliability issue?

- A. Add a programmatic prerequisite that blocks `lookup_order` and `process_refund` calls until `get_customer` has returned a verified customer ID.
- B. Enhance the system prompt to state that customer verification via `get_customer` is mandatory before any order operations.
- C. Add few-shot examples showing the agent always calling `get_customer` first, even when customers volunteer order details.
- D. Implement a routing classifier that analyzes each request and enables only the subset of tools appropriate for that request type.

> **正解: A**
> When a specific tool sequence is required for critical business logic, programmatic enforcement provides deterministic guarantees that prompt-based approaches cannot. Options B and C rely on probabilistic LLM compliance, which is insufficient when errors have financial consequences. Option D addresses tool availability rather than tool ordering, which is not the actual problem.

---

**Q2.** Production logs show the agent frequently calls `get_customer` when users ask about orders (e.g., "check my order #12345"), instead of calling `lookup_order`. Both tools have minimal descriptions ("Retrieves customer information" / "Retrieves order details") and accept similar identifier formats. What's the most effective first step to improve tool selection reliability?

- A. Add few-shot examples to the system prompt demonstrating correct tool selection patterns, with 5-8 examples showing order-related queries routing to `lookup_order`.
- B. Expand each tool's description to include input formats it handles, example queries, edge cases, and boundaries explaining when to use it versus similar tools.
- C. Implement a routing layer that parses user input before each turn and pre-selects the appropriate tool based on detected keywords and identifier patterns.
- D. Consolidate both tools into a single `lookup_entity` tool that accepts any identifier and internally determines which backend to query.

> **正解: B**
> Tool descriptions are the primary mechanism LLMs use for tool selection. When descriptions are minimal, models lack context to differentiate between similar tools. Option B directly addresses the root cause with a low-effort, high-leverage fix. Few-shot examples (A) add token overhead without fixing the underlying issue. A routing layer (C) is over-engineered and bypasses the LLM's natural language understanding. Consolidating tools (D) requires more effort than a "first step" warrants.

---

**Q3.** Your agent achieves 55% first-contact resolution, well below the 80% target. Logs show it escalates straightforward cases (standard damage replacements with photo evidence) while attempting to autonomously handle complex situations requiring policy exceptions. What's the most effective way to improve escalation calibration?

- A. Add explicit escalation criteria to your system prompt with few-shot examples demonstrating when to escalate versus resolve autonomously.
- B. Have the agent self-report a confidence score (1-10) before each response and automatically route requests to humans when confidence falls below a threshold.
- C. Deploy a separate classifier model trained on historical tickets to predict which requests need escalation before the main agent begins processing.
- D. Implement sentiment analysis to detect customer frustration levels and automatically escalate when negative sentiment exceeds a threshold.

> **正解: A**
> Adding explicit escalation criteria with few-shot examples directly addresses the root cause: unclear decision boundaries. This is the proportionate first response before adding infrastructure. Option B fails because LLM self-reported confidence is poorly calibrated. Option C is over-engineered, requiring labeled data and ML infrastructure when prompt optimization hasn't been tried. Option D solves a different problem; sentiment doesn't correlate with case complexity.

---

### Scenario: Code Generation with Claude Code

**Q4.** You want to create a custom `/review` slash command available to every developer when they clone or pull the repository. Where should you create this command file?

- A. In the `.claude/commands/` directory in the project repository
- B. In `~/.claude/commands/` in each developer's home directory
- C. In the CLAUDE.md file at the project root
- D. In a `.claude/config.json` file with a commands array

> **正解: A**
> Project-scoped custom slash commands should be stored in `.claude/commands/` within the repository. These commands are version-controlled and automatically available to all developers when they clone or pull the repo. Option B is for personal commands not shared via version control. Option C is for project instructions and context, not command definitions. Option D describes a configuration mechanism that doesn't exist in Claude Code.

---

**Q5.** You've been assigned to restructure the team's monolithic application into microservices. This will involve changes across dozens of files and requires decisions about service boundaries and module dependencies. Which approach should you take?

- A. Enter plan mode to explore the codebase, understand dependencies, and design an implementation approach before making changes.
- B. Start with direct execution and make changes incrementally, letting the implementation reveal the natural service boundaries.
- C. Use direct execution with comprehensive upfront instructions detailing exactly how each service should be structured.
- D. Begin in direct execution mode and only switch to plan mode if you encounter unexpected complexity during implementation.

> **正解: A**
> Plan mode is designed for complex tasks involving large-scale changes, multiple valid approaches, and architectural decisions — exactly what monolith-to-microservices restructuring requires. Option B risks costly rework when dependencies are discovered late. Option C assumes you already know the right structure without exploring the code. Option D ignores that the complexity is already stated in the requirements.

---

**Q6.** Your codebase has distinct areas with different coding conventions. Test files are spread throughout the codebase alongside the code they test. What's the most maintainable way to ensure Claude automatically applies the correct conventions when generating code?

- A. Create rule files in `.claude/rules/` with YAML frontmatter specifying glob patterns to conditionally apply conventions based on file paths
- B. Consolidate all conventions in the root CLAUDE.md file under headers for each area, relying on Claude to infer which section applies
- C. Create skills in `.claude/skills/` for each code type that include the relevant conventions in their SKILL.md files
- D. Place a separate CLAUDE.md file in each subdirectory containing that area's specific conventions

> **正解: A**
> `.claude/rules/` with glob patterns (e.g., `**/*.test.tsx`) allows conventions to be automatically applied based on file paths regardless of directory location — essential for test files spread throughout the codebase. Option B relies on inference rather than explicit matching. Option C requires manual skill invocation. Option D can't handle files spread across many directories since CLAUDE.md files are directory-bound.

---

### Scenario: Multi-Agent Research System

**Q7.** After running the system on "impact of AI on creative industries," all subagents complete successfully, but the final reports cover only visual arts, completely missing music, writing, and film. The coordinator decomposed the topic into: "AI in digital art creation," "AI in graphic design," and "AI in photography." What is the most likely root cause?

- A. The synthesis agent lacks instructions for identifying coverage gaps in the findings it receives.
- B. The coordinator agent's task decomposition is too narrow, resulting in subagent assignments that don't cover all relevant domains.
- C. The web search agent's queries are not comprehensive enough and need to be expanded.
- D. The document analysis agent is filtering out sources related to non-visual creative industries.

> **正解: B**
> The coordinator's logs reveal the root cause directly: it decomposed "creative industries" into only visual arts subtasks. The subagents executed their assigned tasks correctly — the problem is what they were assigned. Options A, C, and D incorrectly blame downstream agents working correctly within their assigned scope.

---

**Q8.** The web search subagent times out while researching a complex topic. Which error propagation approach best enables intelligent recovery?

- A. Return structured error context to the coordinator including the failure type, the attempted query, any partial results, and potential alternative approaches.
- B. Implement automatic retry logic with exponential backoff within the subagent, returning a generic "search unavailable" status only after all retries are exhausted.
- C. Catch the timeout within the subagent and return an empty result set marked as successful.
- D. Propagate the timeout exception directly to a top-level handler that terminates the entire research workflow.

> **正解: A**
> Structured error context gives the coordinator the information it needs to make intelligent recovery decisions. Option B's generic status hides valuable context from the coordinator. Option C suppresses the error by marking failure as success, preventing any recovery. Option D terminates the entire workflow unnecessarily when recovery strategies could succeed.

---

**Q9.** The synthesis agent frequently needs to verify specific claims. Currently this adds 2-3 round trips per task (+40% latency). 85% of verifications are simple fact-checks; 15% require deeper investigation. What's the most effective approach to reduce overhead while maintaining system reliability?

- A. Give the synthesis agent a scoped `verify_fact` tool for simple lookups, while complex verifications continue delegating through the coordinator.
- B. Have the synthesis agent accumulate all verification needs and return them as a batch to the coordinator at the end of its pass.
- C. Give the synthesis agent access to all web search tools so it can handle any verification need directly.
- D. Have the web search agent proactively cache extra context around each source during initial research.

> **正解: A**
> Option A applies the principle of least privilege: give the synthesis agent only what it needs for the 85% common case while preserving the existing coordination pattern for complex cases. Option B creates blocking dependencies since synthesis steps may depend on earlier verified facts. Option C over-provisions the synthesis agent, violating separation of concerns. Option D relies on speculative caching that cannot reliably predict what the synthesis agent will need.

---

### Scenario: Claude Code for Continuous Integration

**Q10.** Your pipeline script runs `claude "Analyze this pull request for security issues"` but the job hangs indefinitely. Logs indicate Claude Code is waiting for interactive input. What's the correct approach?

- A. Add the `-p` flag: `claude -p "Analyze this pull request for security issues"`
- B. Set the environment variable `CLAUDE_HEADLESS=true` before running the command
- C. Redirect stdin from `/dev/null`: `claude "Analyze this pull request for security issues" < /dev/null`
- D. Add the `--batch` flag: `claude --batch "Analyze this pull request for security issues"`

> **正解: A**
> The `-p` (or `--print`) flag is the documented way to run Claude Code in non-interactive mode. It processes the prompt, outputs the result to stdout, and exits without waiting for user input. Options B and D reference non-existent features. Option C is a Unix workaround that doesn't properly address Claude Code's command syntax.

---

**Q11.** Your team wants to reduce API costs. You have two workflows: (1) a blocking pre-merge check that must complete before developers can merge, and (2) a technical debt report generated overnight. Your manager proposes switching both to the Message Batches API for its 50% cost savings. How should you evaluate this proposal?

- A. Use batch processing for the technical debt reports only; keep real-time calls for pre-merge checks.
- B. Switch both workflows to batch processing with status polling to check for completion.
- C. Keep real-time calls for both workflows to avoid batch result ordering issues.
- D. Switch both to batch processing with a timeout fallback to real-time if batches take too long.

> **正解: A**
> The Message Batches API has processing times up to 24 hours with no guaranteed latency SLA — unsuitable for blocking pre-merge checks, but ideal for overnight batch jobs. Option B is wrong because relying on "often faster" completion isn't acceptable for blocking workflows. Option C reflects a misconception — batch results can be correlated using `custom_id`. Option D adds unnecessary complexity when the simpler solution is matching each API to its appropriate use case.

---

**Q12.** A pull request modifies 14 files across the stock tracking module. Your single-pass review produces inconsistent results: detailed feedback for some files, superficial comments for others, missed bugs, and contradictory feedback. How should you restructure the review?

- A. Split into focused passes: analyze each file individually for local issues, then run a separate integration-focused pass examining cross-file data flow.
- B. Require developers to split large PRs into smaller submissions of 3-4 files before the automated review runs.
- C. Switch to a higher-tier model with a larger context window to give all 14 files adequate attention in one pass.
- D. Run three independent review passes on the full PR and only flag issues that appear in at least two of the three runs.

> **正解: A**
> Splitting reviews into focused passes directly addresses the root cause: attention dilution when processing many files at once. File-by-file analysis ensures consistent depth; a separate integration pass catches cross-file issues. Option B shifts burden to developers without improving the system. Option C misunderstands that larger context windows don't solve attention quality issues. Option D would suppress detection of real bugs by requiring consensus on issues that may only be caught intermittently.

---

## 10. How the Exam Is Scored

The exam is a **criterion-referenced assessment**: each candidate is measured against a fixed performance standard, not against other candidates.

- **Passing standard**: established through a formal standard-setting study by trained subject matter experts. Reported on a scaled range of 100–1,000; cut score is **720**.
- **Result reporting**: pass/fail status + scaled score (100–1,000) + percent-correct by domain. Section-level percentages are for your reference only — pass/fail is based on total scaled score.

---

## 11. Registration and Scheduling

1. Go to the certification page on the Anthropic Partner Academy and review exam details.
2. Download the Exam Guide and review the Certification Terms and Conditions and Exam Policy.
3. Register for the exam and complete checkout.
4. Follow confirmation instructions to create your Pearson VUE account, then sign in to schedule.
5. Choose an available date and select online proctoring or a Pearson test center.
6. You may cancel or reschedule up to **24 hours** before your appointment. Changes within 24 hours forfeit the exam fee.

---

## 12. Exam Policies

### Retake Policy

| 失敗回数 | 待機期間 |
|---------|---------|
| 1回目失敗後 | 14日 |
| 2回目失敗後 | 30日 |
| 3回目失敗後 | 90日 |

- 1つの試験コードで12ヶ月間に最大4回まで受験可能。
- 別の試験コードの受験には影響しない。

### Identification

- 有効な政府発行の顔写真付き身分証明書が必要。
- 名前が登録名と正確に一致すること。

### Accommodations

- 障害等による合理的配慮はPearson VUEを通じて事前に申請・承認が必要。

---

## 13. Exam-Day Experience and Rules of Conduct

**試験中に必要なこと:**
- オンライン受験の場合、プロクターとウェブカメラの視野内に常にいること
- ノート、書籍、スマートフォン、セカンドモニター等をワークスペースから除去
- 他の人との会話禁止
- 試験内容の撮影・複製・再現禁止

**持ち込み禁止物:** 携帯電話、スマートウォッチ、ヘッドフォン、学習資料、録音機器

**違反結果:** 不正行為、禁止リソースへのアクセス試みは、試験結果の無効化・資格の取り消し・将来の試験への受験禁止につながる可能性あり。

---

## 14. Confidentiality and Non-Disclosure Agreement

試験開始前に守秘義務・非開示契約に同意する必要あり。試験内容（問題、回答選択肢、シナリオ）はAnthropicの機密・独占的財産であり、開示・複製・配布は禁止。同意しない場合、試験セッションは終了し返金なし。

---

## 15. Credential Maintenance and Recertification

- 資格の有効期間: **12ヶ月**
- 期限内更新: Anthropic Partner Academyで変更点を確認し、無料の非監視型アセスメントを完了（費用なし）
- 失効後: 全額を支払って本試験を再受験する必要あり
- 試験内容の大幅な変更がある場合、Anthropicは再受験を要求する場合あり

---

## 16. Candidate Support, Appeals, and Privacy

| 問い合わせ種別 | 連絡先 |
|-------------|--------|
| 登録名の修正 | certifications-support@anthropic.com |
| その他（登録、スケジュール、配慮、結果） | Pearson VUE サポート |

**Appeals:** 通知日または試験日から**14日以内**にPearson VUEサポートに提出。ただし、標準設定の結果と個別問題の内容は不服申し立て対象外。

---

## 17. Appendix

### Technologies and Concepts（試験に登場する技術・概念）

**Claude Agent SDK**
- agent definitions, agentic loops, `stop_reason` handling
- hooks (`PostToolUse`, tool call interception)
- subagent spawning via `Task` tool, `allowedTools` configuration

**Model Context Protocol (MCP)**
- MCP servers, MCP tools, MCP resources
- `isError` flag, tool descriptions, tool distribution
- `.mcp.json` configuration, environment variable expansion

**Claude Code**
- CLAUDE.md configuration hierarchy (user/project/directory)
- `.claude/rules/` with YAML frontmatter path-scoping
- `.claude/commands/` for slash commands
- `.claude/skills/` with SKILL.md frontmatter (`context: fork`, `allowed-tools`, `argument-hint`)
- plan mode, direct execution, `/memory`, `/compact`, `--resume`, `fork_session`, Explore subagent

**Claude Code CLI**
- `-p` / `--print` flag for non-interactive mode
- `--output-format json`, `--json-schema` for structured CI output

**Claude API**
- `tool_use` with JSON schemas
- `tool_choice` options (`"auto"`, `"any"`, forced tool selection)
- `stop_reason` values (`"tool_use"`, `"end_turn"`)
- `max_tokens`, system prompts

**Message Batches API**
- 50% cost savings, up to 24-hour processing window
- `custom_id` for request/response correlation
- polling for completion, no multi-turn tool calling support

**その他**
- JSON Schema: required/optional fields, enum types, nullable fields, `"other"` + detail string patterns, strict mode
- Pydantic: schema validation, semantic validation errors, validation-retry loops
- Built-in tools: Read, Write, Edit, Bash, Grep, Glob
- Few-shot prompting, prompt chaining
- Context window management: token budgets, progressive summarization, lost-in-the-middle effects, scratchpad files
- Session management: session resumption, `fork_session`, named sessions, session context isolation
- Confidence scoring: field-level confidence, calibration with labeled validation sets, stratified sampling

---

### In-Scope Topics（出題対象）

- Agentic loop implementation: control flow based on `stop_reason`, tool result handling, loop termination conditions
- Multi-agent orchestration: coordinator-subagent patterns, task decomposition, parallel subagent execution, iterative refinement
- Subagent context management: explicit context passing, structured state persistence, crash recovery using manifests
- Tool interface design: effective tool descriptions, splitting vs consolidating tools, tool naming to reduce ambiguity
- MCP tool and resource design: resources for content catalogs, tools for actions, description quality
- MCP server configuration: project vs user scope, environment variable expansion, multi-server simultaneous access
- Error handling and propagation: structured error responses, transient vs business vs permission errors, local recovery before escalation
- Escalation decision-making: explicit criteria, honoring customer preferences, policy gap identification
- CLAUDE.md configuration: hierarchy (user/project/directory), `@import` patterns, `.claude/rules/` with glob patterns
- Custom commands and skills: project vs user scope, `context: fork`, `allowed-tools`, `argument-hint` frontmatter
- Plan mode vs direct execution: complexity assessment, architectural decisions, single-file changes
- Iterative refinement: input/output examples, test-driven iteration, interview pattern, sequential vs parallel issue resolution
- Structured output via `tool_use`: schema design, `tool_choice` configuration, nullable fields to prevent hallucination
- Few-shot prompting: ambiguous scenario targeting, format consistency, false positive reduction
- Batch processing: Message Batches API appropriateness, latency tolerance assessment, failure handling by `custom_id`
- Context window optimization: trimming verbose tool outputs, structured fact extraction, position-aware input ordering
- Human review workflows: confidence calibration, stratified sampling, accuracy segmentation by document type and field
- Information provenance: claim-source mappings, temporal data handling, conflict annotation, coverage gap reporting

---

### Out-of-Scope Topics（出題対象外）

- Fine-tuning Claude models or training custom models
- Claude API authentication, billing, or account management
- Detailed implementation of specific programming languages or frameworks
- Deploying or hosting MCP servers (infrastructure, networking, container orchestration)
- Claude's internal architecture, training process, or model weights
- Constitutional AI, RLHF, or safety training methodologies
- Embedding models or vector database implementation details
- Computer use (browser automation, desktop interaction)
- Vision/image analysis capabilities
- Streaming API implementation or server-sent events
- Rate limiting, quotas, or API pricing calculations
- OAuth, API key rotation, or authentication protocol details
- Specific cloud provider configurations (AWS, GCP, Azure)
- Performance benchmarking or model comparison metrics
- Prompt caching implementation details (beyond knowing it exists)
- Token counting algorithms or tokenization specifics

---

## Document Control

| Version | Summary | Date |
|---------|---------|------|
| 1.0 | Formatting and layout updates | July 2026 |
| 0.2 | Draft revision | June 2026 |
| 0.1 | Initial draft | February 2026 |
