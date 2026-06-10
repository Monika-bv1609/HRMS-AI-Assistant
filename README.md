# ODOOHR-AI

## Overview

ODOOHR-AI is an AI-powered Human Resource Assistant that integrates Odoo ERP with Large Language Models using LangGraph. The system enables employees and managers to perform HR operations through natural language conversations.

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

---

## Author

Monika BV

Aspiring AI Engineer | Python | FastAPI | LangGraph | AI Agents | RAG | ChromaDB | Odoo
