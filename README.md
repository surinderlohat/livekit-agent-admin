# LiveKit Agent Admin

A lightweight admin dashboard for managing **self-hosted LiveKit servers and AI agents**.

This tool provides a simple interface to manage SIP trunks, configure agent prompts, and monitor active calls when running your own LiveKit infrastructure.

The goal of this project is to provide a **minimal, open-source admin UI for the LiveKit community**.

---

# Features

* System prompt editor for AI agents
* SIP trunk management
* Active call monitoring
* Invite human participants to rooms
* Simple server-rendered UI
* Lightweight and easy to deploy

---

# Tech Stack

* Python
* FastAPI
* Jinja2 Templates
* Tailwind CSS

The project intentionally avoids heavy frontend frameworks and keeps the architecture simple.

---

# Installation

Clone the repository:

```
git clone https://github.com/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

Create virtual environment:

```
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the server:

```
uvicorn app.main:app --reload
```

Open:

```
http://localhost:8000
```

---

# Docker (Optional)

```
docker compose up --build
```

---

# Why This Project Exists

LiveKit Cloud provides a dashboard, but **self-hosted LiveKit deployments do not include a built-in admin interface**.

This project fills that gap by providing a simple dashboard for:

* managing SIP trunks
* configuring agent prompts
* monitoring calls
* interacting with LiveKit rooms

---

# Attribution Requirement

This project is open-source and free to use.

If you fork, redistribute, or build upon this project, **please keep the attribution to the original author**.

At minimum, please retain the following credit somewhere visible:

```
Created by Surinder Singh
https://github.com/surinderlohat
```

This helps support the continued development of the project.

---

# Contributing

Contributions are welcome.

If you improve the project, please open a pull request.

Please keep attribution to the original repository.

---

# License

This project is licensed under the Apache License 2.0.

Copyright (c) 2026 Surinder Singh

---

# Author

Created by **Surinder Singh**

GitHub Profile
https://github.com/surinderlohat

If this project helps you, please consider giving it a ⭐ on GitHub.
