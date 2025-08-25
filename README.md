# 🤖 AI Cloud Assistant (Multi-Cloud CLI)

This is an **AI-driven conversational CLI tool** to provision and manage VMs across multiple cloud providers.  
Currently, **AWS EC2** is supported. **Azure** and **GCP** are placeholders (integration planned).

---

## 🚀 Features
- **Conversational CLI** – Natural language input (e.g., `create 2 ubuntu vm in aws us-east-1`)
- **Clarification flow** – Asks for missing details step by step
- **AWS EC2 integration**:
  - Create VM(s) with subnet, security group, key pair, tags
  - List VM(s) with Name, State, OS type, IPv4
  - Delete VM(s) by Name
- **Extensible**:
  - Abstracted service layer for AWS / Azure / GCP
  - Config-driven clarifications
  - NLP intent parsing

---

## 📂 Project Structure
AI_Project_v2/
├── main.py # Entry point: conversational loop
├── requirements.txt # Dependencies: boto3, spacy
├── core/
│ ├── conversation.py # Manages conversational flow
│ ├── clarifier.py # Resolves missing/ambiguous parameters
│ ├── dispatcher.py # Routes intents to cloud services
│ ├── nlp.py # Parses user input for intents/parameters
│ ├── utils.py # Utility functions (e.g., spinner)
│ ├── config.py # Configuration and provider registry
├── services/
│ ├── aws_ec2.py # AWS EC2 provisioning
│ ├── azure_vm.py # Azure VM provisioning
│ ├── gcp_vm.py # GCP VM provisioning
│ ├── vm_interface.py # VM interface
│ ├── aws_helpers.py # AWS helper functions





## Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate     # Linux / Mac
venv\Scripts\activate        # Windows

## Install dependencies
pip install -r requirements.txt


## Configure AWS credentials
aws configure

## Run the assistant:
python3 main.py


## Roadmap
 Azure VM support
 GCP VM support
 Multi-cloud orchestration
 Streamlit GUI option
 Persistent config & history
