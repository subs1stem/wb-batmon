# wb-batmon

Module for integrating the BatMon system into the Wiren Board controller.

## 🛠 Installation

* **Step 1:** Clone the repository:

```bash
git clone https://github.com/subs1stem/wb-batmon.git /opt/wb-batmon
```

* **Step 2:** Run the installation script:

```bash
# Make the install.sh script executable
sudo chmod +x /opt/wb-batmon/install.sh

# Run the installation script
sudo /opt/wb-batmon/install.sh
```

* **Step 3:** Configure the .env file:

```bash
sudo nano /opt/wb-batmon/.env
```

* **Step 4:** Start service:

```bash
sudo systemctl start wb-batmon.service
```
