# DevOps Workflow Project

## What This Project Does
- Processes financial transactions
- Runs on SQLite database
- Deployed via CI/CD pipeline
# Ledgerflow

**A Production-Grade Reference Implementation for Automated Financial Transaction Processing and Continuous Delivery**

---

## Preface

In the discipline of modern software engineering, the distance between a working prototype and a dependable production system is bridged not by code alone, but by the rigor of one's operational practices. **Ledgerflow** stands as a testament to that principle: a compact yet comprehensive demonstration of how a financial transaction processor—grounded in the reliability of SQLite—can be engineered, containerized, provisioned, and delivered through an unbroken chain of automated assurance.

This repository is intended for engineers, architects, and students of DevOps who wish to examine a complete, end-to-end workflow wherein every commit is treated as a candidate for production and every deployment is the product of verifiable automation.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architectural Philosophy](#architectural-philosophy)
3. [Technology Stack](#technology-stack)
4. [Repository Structure](#repository-structure)
5. [Getting Started](#getting-started)
6. [The CI/CD Pipeline](#the-cicd-pipeline)
7. [Branching Strategy](#branching-strategy)
8. [Containerization & Provisioning](#containerization--provisioning)
9. [Design Decisions & Rationale](#design-decisions--rationale)
10. [Contributing](#contributing)
11. [License](#license)

---

## Project Overview

Ledgerflow processes financial transactions against a SQLite datastore. Despite its modest footprint, the project is deliberately engineered to mirror the concerns of systems many orders of magnitude larger:

- **Deterministic transaction handling** with ACID guarantees inherited from SQLite.
- **Immutable build artifacts** produced via Docker.
- **Idempotent infrastructure provisioning** orchestrated by Ansible.
- **Continuous integration and delivery** executed through GitHub Actions on every push.
- **A disciplined branching model** that keeps `main` perpetually releasable.

The objective is not merely to *run* an application, but to demonstrate the full lifecycle of a service: from a developer's first commit to a verified, deployed artifact.

---

## Architectural Philosophy

Three convictions underpin this project:

> **1. Automation is not a convenience; it is a contract.**
> Every quality gate encoded in the pipeline is a promise to future maintainers that regressions will be caught before they reach production.

> **2. Simplicity is a feature.**
> SQLite was chosen deliberately. It eliminates the operational overhead of a database server while preserving transactional integrity—allowing the project's focus to remain squarely on delivery mechanics.

> **3. Reproducibility is non-negotiable.**
> The same commit, processed by the same pipeline, must yield the same artifact—on any machine, at any time.

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Application** | Python 3 | Core transaction processing logic |
| **Persistence** | SQLite | Embedded, ACID-compliant relational store |
| **Containerization** | Docker | Immutable, portable runtime artifacts |
| **Provisioning** | Ansible | Idempotent environment configuration |
| **Continuous Delivery** | GitHub Actions | Automated build, test, and deployment |
| **Version Control** | Git | Disciplined branching and release management |

---

## Repository Structure

## Technologies Used
- Python, SQLite
- Docker, Ansible
- GitHub Actions
- Git branching strategy

## How to Run
1. Clone the repo
2. Create virtual environment
3. Install dependencies
4. Run `python app/sqlite_app.py`

## CI/CD Pipeline
- Runs on every push
- Tests code quality
- Checks performance
