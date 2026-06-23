# HRMS-AI-Assistant

## Overview

HRMS-AI-Assistant is an AI-powered Human Resource Assistant that integrates Odoo ERP with Large Language Models using LangGraph. The system enables employees and managers to perform HR operations through natural language conversations.

The application combines AI Agents, Retrieval-Augmented Generation (RAG), FastAPI, ChromaDB, and Odoo APIs to automate HR processes such as leave management, employee information retrieval, and policy assistance.



## Key Features

### Employee Management Agent

* Retrieve employee information
* View employee profiles
* Search employee records

### Leave Management Agent

* Apply leave using natural language
* Leave approval workflow
* Human confirmation before execution

### Policy Assistant (RAG)

* Answer HR policy questions
* Document retrieval using ChromaDB
* Context-aware responses

### Multi-Agent Architecture

* Supervisor Agent for routing requests
* Specialized HR Agents
* Tool calling and workflow orchestration using LangGraph

### Session Memory

* Maintains conversation context
* Supports multi-turn interactions

---

## Technology Stack

### Backend

* Python
* FastAPI

### AI Frameworks

* LangGraph
* LangChain
* OpenAI

### Database

* PostgreSQL
* ChromaDB

### ERP Integration

* Odoo HR Module

### Deployment

* Docker
* AWS (Planned)

---

## System Architecture

```text
User
 │
 ▼
FastAPI API Layer
 │
 ▼
Supervisor Agent (LangGraph)
 │
 ├── Employee Agent
 │
 ├── Leave Agent
 │
 ├── Policy RAG Agent
 │
 └── Confirmation Agent
 │
 ▼
Tools Layer
 │
 ├── Odoo APIs
 ├── ChromaDB
 └── PostgreSQL
 │
 ▼
Response

## Project Structure

backend/
│
├── agents/
├── graph/
├── tools/
├── services/
├── api/
├── database/
├── chromadb/
└── main.py

## Future Enhancements

* Multi-Agent Supervisor Pattern
* Role-Based Access Control
* AWS Production Deployment
* Advanced Analytics Agent
* Employee Onboarding Agent
* Performance Review Agent


LangSmith Observability & Evaluation

Implemented LangSmith for monitoring, debugging, and evaluating the AI system.

Features
Prompt Versioning
Dataset Creation
Experiment Tracking
Tool Router Evaluation
LLM-as-a-Judge Evaluation
RAG Evaluation
Groundedness Analysis
Retrieval Relevance Analysis
Correctness Evaluation
Tracing & Debugging


<img width="1887" height="860" alt="image" src="https://github.com/user-attachments/assets/da33ee27-a9b0-4976-b4ed-07d71199a8e3" />


---

## Author

Monika BV

Aspiring AI Engineer | Python | FastAPI | LangGraph | AI Agents | RAG | ChromaDB | Odoo
