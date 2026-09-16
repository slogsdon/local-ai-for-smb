# Local AI for SMBs

> Applied research into when local AI is a practical, private, and economically compelling option for small and midsize businesses.

## Overview

AI is rapidly becoming accessible to businesses of every size, but most of the conversation around adoption assumes that inference happens somewhere else: a hosted model, cloud API, or managed AI platform.

Local AI creates another option.

Modern AI workstations and increasingly capable open models make it possible to run useful AI workloads directly on hardware controlled by the business. This potentially changes the economics, privacy characteristics, reliability, and architecture of applied AI.

For small and midsize businesses, however, the practical case is still unclear.

Local AI for SMBs is an independent applied research project exploring a simple question:

> When does running AI locally make more sense for an SMB than relying entirely on cloud AI services?

The goal is not to prove that local AI is universally better.

The goal is to identify where local, cloud, and hybrid AI architectures each make practical business sense and to produce reproducible examples that other developers and businesses can evaluate for themselves.

## Project Status

Status: Planning / Pre-research

This repository currently documents the intended research program.

Hardware, models, software, benchmarks, and reference implementations have not yet been selected or evaluated. The project will evolve as appropriate research hardware and resources become available.

No performance, cost, or capability claims should be inferred from the proposed experiments described here.

Initial work will focus on defining:

* representative SMB workloads;
* reproducible evaluation methodology;
* baseline cloud implementations;
* candidate local models and runtimes;
* benchmarking and observability tooling; and
* hardware requirements for meaningful local inference testing.

Research artifacts will be added to this repository as experiments are completed.

## Research Thesis

Local AI may be particularly interesting for SMB workloads where one or more of the following matter:

* sensitive business or customer information;
* predictable or high inference volume;
* recurring AI API costs;
* low-latency interaction;
* operation during limited internet connectivity;
* control over models and data;
* integration with internal systems;
* long-running agents or automation;
* specialized models;
* predictable infrastructure costs.

Those advantages also come with tradeoffs.

Local systems introduce hardware costs, maintenance, model management, power consumption, deployment complexity, security responsibilities, and finite compute capacity.

The project will therefore evaluate business outcomes and operational tradeoffs, not simply model performance.

## Research Questions

The project will investigate questions including:

### Capability

Can locally deployed models perform useful SMB tasks at a quality level that makes them operationally viable?

How much model capability is actually necessary for common business workflows?

### Economics

At what usage levels does owning local AI infrastructure become economically competitive with consumption-based cloud inference?

How do hardware acquisition, electricity, maintenance, model operations, and expected hardware lifetime affect total cost of ownership?

### Privacy

Which workflows materially benefit from keeping prompts, documents, customer information, or proprietary business data within infrastructure controlled by the business?

### Performance

What latency and throughput can reasonably be expected from workstation-class AI hardware?

When does local inference improve the user experience, and when does cloud infrastructure remain preferable?

### Operations

How difficult is it for a small technical team—or an SMB working with an IT provider—to deploy, maintain, secure, and monitor local AI?

### Architecture

Which workloads work best as:

Local → Cloud → Hybrid

rather than treating the deployment model as an all-or-nothing decision?

## Initial Use Cases

The research will center on realistic business workflows rather than synthetic inference benchmarks alone.

### 1. Private Company Knowledge Assistant

Build a retrieval-augmented assistant capable of answering questions across internal company information.

Potential data:

* policies;
* procedures;
* product documentation;
* contracts;
* support documentation;
* internal knowledge bases;
* sales material.

Research focus:

privacy · retrieval quality · latency · document volume · cost

### 2. Document Processing

Evaluate AI-assisted processing of common business documents.

Examples:

* invoices;
* purchase orders;
* contracts;
* forms;
* reports;
* correspondence.

Potential workflows include extraction, classification, summarization, validation, and routing.

Research focus:

accuracy · structured output · throughput · privacy · automation potential

### 3. Customer Support Assistant

Build an assistant capable of helping employees research and respond to customer questions using approved business knowledge.

The initial implementation will emphasize human-assisted workflows rather than fully autonomous customer communication.

Research focus:

response quality · retrieval · latency · hallucination risk · human oversight

### 4. Business Operations Agent

Explore an AI agent capable of coordinating routine operational tasks across business systems.

Potential tasks:

* researching information;
* preparing reports;
* categorizing requests;
* generating documents;
* updating internal systems;
* coordinating multi-step workflows.

Research focus:

tool use · reliability · long-running workloads · auditability · cost

### 5. Development & IT Assistant

Evaluate local models for software development and technical operations.

Potential tasks:

* code generation;
* code explanation;
* repository analysis;
* scripting;
* log analysis;
* troubleshooting;
* documentation.

Research focus:

code quality · context capacity · latency · privacy · developer productivity

### 6. Hybrid AI Router

Not every task needs the same model.

This experiment will investigate an architecture where requests can be routed between local and cloud models based on factors such as:

* task complexity;
* sensitivity;
* latency requirements;
* model capability;
* context size;
* cost.

For example:

```
                     ┌─> Local Model
User / Application ──┤
                     └─> Cloud Model
                           │
                     Complex / Specialized
                           Tasks
```

This may ultimately prove more practical for SMBs than either a completely local or completely cloud-based architecture.

Research focus:

routing strategy · quality · privacy · resilience · total cost

## Evaluation Framework

Each workload will be evaluated across a common set of dimensions.

| Dimension | Example Measurements |
|-----------|----------------------|
|Quality|Accuracy, task completion, human evaluation|
|Performance|Time to first token, tokens/sec, total task time|
|Capacity|Model size, context size, concurrent workloads|
|Reliability|Failure rate, consistency, recovery behavior|
|Privacy|Data leaving controlled infrastructure|
|Cost|Hardware, API usage, electricity, infrastructure|
|Operations|Setup, updates, monitoring, maintenance|
|Security|Data exposure, permissions, attack surface|
|Usability|Employee/developer experience|
|Business Value|Time saved, tasks automated, practical usefulness|

Individual experiments may introduce additional workload-specific measurements.

## Local vs. Cloud Cost Model

One of the primary research outputs will be a transparent total-cost model.

Rather than comparing only API token prices against hardware purchase price, the model will attempt to include:

```
Local AI
hardware acquisition
+ electricity
+ supporting infrastructure
+ administration
+ maintenance
+ expected hardware lifecycle
────────────────────────────
total local cost
Cloud AI
input tokens
+ output tokens
+ platform costs
+ supporting infrastructure
+ network requirements
────────────────────────────
total cloud cost
```

The objective is to estimate break-even ranges, not manufacture a single universal break-even point.

All assumptions used in published calculations will be documented.

## Experimental Approach

Where practical, each use case will follow the same basic process.

```
1. Define the business problem
        ↓
2. Establish a measurable task
        ↓
3. Build a cloud baseline
        ↓
4. Build a local implementation
        ↓
5. Measure quality + performance
        ↓
6. Measure operational requirements
        ↓
7. Model cost
        ↓
8. Compare local / cloud / hybrid
        ↓
9. Publish results + implementation
```

Experiments should be reproducible whenever licensing, data, and infrastructure constraints allow.

Synthetic or publicly available datasets will be preferred where publishing real business data would create privacy or licensing concerns.

## Planned Repository Structure

As the research progresses, the repository is expected to evolve toward:

```
local-ai-for-smbs/
│
├── README.md
│
├── docs/
│   ├── methodology/
│   ├── architecture/
│   └── findings/
│
├── benchmarks/
│   ├── inference/
│   ├── cost/
│   └── workloads/
│
├── examples/
│   ├── knowledge-assistant/
│   ├── document-processing/
│   ├── support-assistant/
│   ├── operations-agent/
│   ├── developer-assistant/
│   └── hybrid-router/
│
├── models/
│   └── evaluations/
│
└── tools/
    └── benchmark-harness/
```

The structure will change as practical implementation requirements become clearer.

## Planned Outputs

The project is intended to produce more than benchmark numbers.

Over time, expected outputs include:

1. Reference implementations - Reproducible examples demonstrating useful SMB AI workflows.
2. Benchmark data - Performance and workload measurements collected under documented conditions.
3. Architecture patterns - Reference architectures for local, cloud, and hybrid deployments.
4. Cost models - Transparent models businesses can modify using their own assumptions.
5. Implementation guides - Documentation covering deployment, configuration, security, and operational considerations.
6. Research findings - Written analysis explaining what worked, what did not, and where different architectures appear appropriate.
7. Decision framework - A practical framework for deciding whether a particular SMB workload belongs locally, in the cloud, or somewhere in between.

## Guiding Principles

### Business problems before benchmarks

A system capable of producing impressive benchmark numbers is not necessarily useful to a business.

Experiments should begin with a real operational problem and work backward to the technology.

### Reproducibility

Configurations, assumptions, prompts, datasets, and measurements should be documented whenever possible.

### No predetermined winner

Local inference is not assumed to be superior to cloud inference.

Negative results are useful results.

### Practical hardware

The research is primarily interested in hardware that could realistically be deployed by an SMB, consultant, managed service provider, or small technical team.

This is not intended to be a study of hyperscale AI infrastructure.

### Open models where practical

Openly available models and tooling will be preferred when they improve reproducibility and allow others to repeat experiments.

### Privacy by design

Experiments involving sensitive workloads should minimize unnecessary transmission or retention of business data.

### Human usefulness matters

A statistically faster model that produces worse business outcomes is not an improvement.

Human evaluation will therefore complement technical benchmarks where appropriate.

## Who This Research Is For

The project is intended to be useful to:

* small and midsize business owners;
* developers building AI-enabled business applications;
* technical product leaders;
* IT consultants;
* managed service providers;
* AI practitioners;
* software vendors serving SMBs; and
* hardware and infrastructure teams exploring edge and local AI.

Deep AI infrastructure expertise should not be required to understand the final findings.

One of the goals of the project is to translate rapidly evolving AI infrastructure into practical business decisions.

## Collaboration

This project is currently in its formative stage.

I’m interested in collaborating with researchers, developers, model creators, infrastructure providers, hardware manufacturers, software vendors, and SMB operators interested in practical local AI.

Particularly useful contributions include:

* representative SMB use cases;
* benchmark methodology;
* evaluation datasets;
* open models;
* inference tooling;
* hardware access;
* technical review;
* real-world operational requirements; and
* reproducible experiments.

Hardware access and other research support may be provided by third parties as the project develops. Any material support related to published research will be disclosed.

Support does not guarantee favorable findings.

## What Success Looks Like

The project succeeds if it can eventually answer a question like:

“I run or support a small business with this particular AI workload. Should I run it locally, use a cloud model, or combine the two—and what will each option actually require?”

with something better than:

“It depends.”

The answer should instead be supported by architectures, measurements, source code, cost assumptions, and practical experience that allow someone to make an informed decision.

## About

This is an independent, exploratory research project focused on practical AI adoption for small and midsize businesses.

The project is currently in the planning stage. Technologies, models, hardware platforms, research partners, and implementation details will evolve as experiments begin.