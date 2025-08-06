# 🚀 Automated Apache Installation on EC2 via Lambda & SSM

This repository provides a Python-based **AWS Lambda function** that remotely triggers the **installation of Apache HTTP Server (httpd)** on Amazon EC2 instances using **AWS Systems Manager (SSM)**. No SSH access required!

---

## 📌 Use Case

Enable zero-touch Apache web server provisioning on EC2 instances by:

- Automating configuration on boot or schedule
- Using Lambda as a trigger (manual, EventBridge, SNS, etc.)
- Leveraging SSM Run Command to execute scripts securely

---

## ⚙️ What It Does

1. ✅ Accepts EC2 instance ID(s)
2. 🧠 Uses SSM Run Command to execute shell commands on the instance(s)
3. 🛠 Installs Apache (`httpd`) and starts the service
4. 🔁 (Optional) Enables Apache to start on boot
5. 📝 Logs the command ID and output to CloudWatch

---
