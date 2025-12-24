# 🔐 Security Policy

## Supported Versions

The following versions of **NagarNirman** are currently supported with security updates:

| Version | Supported |
| ------- | --------- |
| 1.x.x   | ✅ Yes     |
| < 1.0   | ❌ No      |

> Only the latest stable version is actively maintained and receives security updates.

---

## Reporting a Vulnerability

We take security issues seriously and appreciate responsible disclosure.

### 📩 How to Report

If you discover a security vulnerability, please report it using **one of the following methods**:

* 📧 Email: **[hello@nagar-nirman.org](mailto:hello@nagar-nirman.org)**
* 🐞 GitHub: Open a **private issue** or contact a maintainer directly

### 📝 What to Include

Please include:

* A clear description of the vulnerability
* Steps to reproduce the issue
* Potential impact (if known)
* Screenshots or logs (if applicable)

### ⏱️ Response Timeline

* **Initial response:** within 48 hours
* **Status update:** within 5 working days
* **Fix & patch:** depending on severity and complexity

### ✅ If Accepted

* The vulnerability will be investigated
* A fix will be released in a future update
* Credit may be given to the reporter (if desired)

### ❌ If Declined

* You will receive a clear explanation
* Suggestions or clarifications may be provided

---

## 🔒 Security Best Practices Used

* Session-based authentication
* Role-based access control (User / Admin)
* No hardcoded secrets in source code
* Safe JSON file handling
* Dependency management via `requirements.txt`

---

## 📌 Disclaimer

This project is currently designed for **academic and demonstration purposes**.
For production use, additional security layers such as encrypted databases, secure authentication providers, and server-side validation are recommended.

---
