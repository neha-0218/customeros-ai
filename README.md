# CustomerOS AI
### Customer Success Intelligence Platform with AI Insights, Product Analytics, and Business Intelligence

## Live Demo

**Application URL**

https://customeros-ai-4l18.onrender.com/login/

**Demo Credentials**

```text
Username: priya_pm
Password: demo1234
```

# CustomerOS AI
### Customer Success Intelligence Platform with AI Insights, Product Analytics, and Business Intelligence

[![Django](https://img.shields.io/badge/Django-5.x-green)]()
[![DRF](https://img.shields.io/badge/Django_REST_Framework-API-red)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)]()
[![Power_BI](https://img.shields.io/badge/Power_BI-Analytics-yellow)]()
[![Render](https://img.shields.io/badge/Render-Deployed-purple)]()

---


# Overview

CustomerOS AI is an end-to-end Customer Success and Product Intelligence platform built to help SaaS organizations monitor customer health, identify churn risks, prioritize product improvements, analyze customer feedback, and generate AI-powered recommendations.

The platform combines operational workflows, AI-assisted decision support, REST APIs, and business intelligence dashboards into a single system.

The project was designed around three core business questions:

1. Which customers are at risk and how much revenue is exposed?
2. What are customers asking for and are we delivering it?
3. Is the AI delivering valuable insights effectively?

---

# Project Status

### Core Platform

 Authentication & Role-Based Access Control

 Customer Account Management

 Customer Health Monitoring

 Risk Flag Management

 Feedback Management

 Feature Request Management

 Ticket Management

---

### AI Features

 AI Insights Engine

 AI Copilot Assistant

 Churn Risk Explanations

 Feature Demand Analysis

 Insight Acceptance Tracking

---

### Analytics

 Customer Health Dashboard

 Feature Demand Dashboard

 AI Intelligence Dashboard

 Power BI Reporting

---

### APIs

 Django REST Framework

 Pagination

 Nested Serializers

 Filtering

 JSON API Responses

---

### Deployment

 PostgreSQL

 Render Deployment

 Production Environment

---

### Future Enhancements

 Predictive Churn Modeling

 Advanced Sentiment Analysis

 RAG-Based Knowledge Retrieval

 Customer Journey Analytics

 Real-Time Event Tracking

---

# Key Features

## Customer Success

Monitor customer health and proactively identify churn risks.

Features:

- Customer Accounts
- Revenue Tracking
- Health Scores
- Risk Tiers
- Health Snapshots
- Revenue-at-Risk Analysis

---

## Product Intelligence

Capture customer feedback and translate it into roadmap decisions.

Features:

- Feature Requests
- Customer Voting
- Feedback Themes
- Ticket Categorization
- Product Prioritization

---

## AI Intelligence

Generate insights using large language models and support decision-making workflows.

Features:

- AI Recommendations
- Churn Risk Insights
- Feature Demand Analysis
- AI Copilot Assistant
- Insight Acceptance Tracking
- AI Performance Monitoring

---

# Power BI Dashboards

The analytics layer is built around three executive dashboards.

---

## 1. Customer Health Overview

### Business Question

> Which customers are at risk and how much recurring revenue is exposed?

### Metrics

- Total MRR
- MRR At Risk
- Customer Health Scores
- Risk Tier Distribution
- Component Score Breakdown

### Business Value

Enables Customer Success teams to identify at-risk customers early and prioritize retention efforts before churn occurs.

### Dashboard

![Customer Health Dashboard](screenshots/customer-health.png)

---

## 2. Feature Demand Analysis

### Business Question

> What are customers asking for and are we delivering it?

### Metrics

- Feature Requests by Vote Count
- Feature Pipeline Status
- Feature Shipped Rate
- Support Ticket Categories
- Feedback Themes

### Business Value

Provides a structured framework for prioritizing product investments based on measurable customer demand.

### Dashboard

![Feature Demand Dashboard](screenshots/feature-demand.png)

---

## 3. AI Intelligence Dashboard

### Business Question

> Is the AI generating useful insights efficiently?

### Metrics

- AI Acceptance Rate
- Total AI Insights
- Insight Status Distribution
- Insights by Type
- Average AI Response Time

### Business Value

Measures AI quality, user trust, and model performance.

### Dashboard

![AI Intelligence Dashboard](screenshots/ai-dashboard.png)

---

# REST API

The platform exposes business data through Django REST Framework APIs.

## Available Endpoints

```text
/api/v1/accounts/
/api/v1/feedback/
/api/v1/tickets/
/api/v1/health/
/api/v1/risk-flags/
/api/v1/ai-insights/
```

---

## Example Response

### Accounts API

```http
GET /api/v1/accounts/
```

```json
{"id":"c0972ffc-93da-4856-b56a-b8d7bd8f820c","name":"Gringotts FinTech","industry":"Retail","plan_tier":"growth","mrr":"13777.00","contract_renewal_date":"2027-02-14","is_active":true,"organization_name":"Acme SaaS Inc","health_score":{"composite_score":68.8,"risk_tier":"moderate"},"created_at":"2026-07-04T03:52:51.187601Z"},
```

### AI Insights API

```http
GET /api/v1/ai-insights/
```

```json
{
      "id": "1ae6566d-a97d-415e-a037-9071761646f7",
      "insight_type": "copilot_answer",
      "status": "generated",
      "customer_account": null,
      "customer_account_name": null,
      "response_text": "**At-Risk Accounts:**\n\nBased on the context, the following accounts are most at risk this week:\n\n1. **Pied Piper**: With a composite score of 53.4, which is below the healthy threshold, and a MRR of $5858.00, this account is considered At-Risk.\n2. **Oscorp Digital**: With a composite score of 43.7, which is also below the healthy threshold, and a MRR of $3818.00, this account is considered At-Risk.\n3. **LexCorp Cloud**: With a composite score of 54.3, which is below the healthy threshold, and a MRR of $10320.00, this account is considered At-Risk.\n\n**Key Insights:**\n\n* All three accounts have a composite score below the healthy threshold, indicating potential issues with their usage or adoption.\n* Pied Piper and Oscorp Digital have lower MRRs compared to LexCorp Cloud, which may indicate smaller or more vulnerable customer bases.\n\n**Recommendations:**\n\n* Prioritize outreach and support to these At-Risk accounts to address any potential issues and prevent churn.\n* Review account-specific data to identify root causes of their at-risk status and develop targeted strategies for improvement.\n* Consider offering additional support or resources to help these accounts achieve a healthier score and reduce their risk of churn.",
      "model_used": "meta-llama/llama-3-8b-instruct",
      "latency_ms": 9265,
      "rejection_reason": "",
      "created_at": "2026-07-04T04:43:44.272082Z"
    },
```

---

# System Architecture

```text
Users
 │
 ▼
CustomerOS AI Platform
 │
 ├── Authentication & RBAC
 ├── Customer Accounts
 ├── Health Engine
 ├── Risk Flags
 ├── Feedback Management
 ├── Feature Requests
 ├── Ticket Management
 ├── AI Insights Engine
 └── AI Copilot
         │
         ▼
      OpenRouter
         │
         ▼
      Llama Models

PostgreSQL Database
         │
         ▼
       Power BI
```

---

# Technology Stack

## Backend

- Python
- Django
- Django REST Framework

## Database

- PostgreSQL

## Frontend

- Django Templates
- Bootstrap

## AI Layer

- OpenRouter
- Llama 3 Models

## Analytics

- Power BI

## Deployment

- Render

## Version Control

- Git
- GitHub

---

# What This Project Demonstrates

## For Product Manager / AI Product Manager Roles

End-to-end product thinking—from customer problems and KPI definition through customer health monitoring, feedback analysis, AI-assisted prioritization, and roadmap visibility. Every major module is tied to a measurable business outcome.

## For Data Analyst Roles

A multi-module PostgreSQL data model, REST APIs with nested serialization, and Power BI dashboards tracking business KPIs including MRR at risk, customer health, AI acceptance rate, feature demand, and support trends.

## For AI Product Manager Roles

A working AI layer powered by OpenRouter and Llama models that generates churn-risk explanations, feature demand insights, AI recommendations, and natural language interactions through an AI Copilot.

---

# Known Limitations

## Sentiment Analysis

Current demo data contains synthetic sentiment scores generated for testing and dashboard validation.

Example:

```text
"The new analytics view is exactly what we needed."
sentiment_score = -0.5
```

These scores do not currently originate from a production NLP sentiment model.

Future iterations will include automated sentiment analysis using a dedicated NLP pipeline.

---

## Demo Data

Some records were generated for demonstration and testing purposes.

Examples include:

- Sample customers
- Sample AI insights
- Dashboard seed data

These records exist to demonstrate workflows and reporting capabilities.

---

# Local Setup

## Clone Repository

```bash
git clone https://github.com/Neha-0212/customeros-ai.git
cd customeros-ai
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key

DEBUG=True

DATABASE_URL=your_database_url

OPENROUTER_API_KEY=your_api_key
```

---

## Run Migrations

```bash
python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Start Development Server

```bash
python manage.py runserver
```

Application will be available at:

```text
http://127.0.0.1:8000
```

---

# Screenshots

Create a folder:

```text
screenshots/
├── customer-health.jpg
├── feature-demand.jpg
└── ai-dashboard.jpg
```


---

# Future Roadmap

### Analytics

- Predictive Churn Scoring
- Customer Journey Analytics
- Product Adoption Tracking

### AI

- Sentiment Analysis Pipeline
- Retrieval-Augmented Generation (RAG)
- AI Feedback Loop Training

### Platform

- Event Tracking
- Real-Time Notifications
- Advanced Reporting

---

# Author

**Neha** — aspiring Product Manager / AI Product Manager focused on customer intelligence, analytics, and AI-powered product systems.

GitHub: https://github.com/Neha-0212

LinkedIn: https://linkedin.com/in/neha-kanaki

---

If you found this project interesting, consider giving the repository a ⭐.
