# 📞 Number OSINT Tool

A simple **Phone Number OSINT (Ethical, Passive)** tool written in Python.

### ✨ Features
- ✅ Validates phone number & extracts metadata locally (carrier, region, timezone, type, formats).  
- ✅ Optional enrichment with **NumVerify API** (if API key is set).  
- ✅ Mock Aadhaar lookup integration (demo).  
- ✅ Generates a **link pack** with Google dorks & major social platforms.  
- ✅ Lightweight and runs in **Kali Linux** & **Termux**.  

---

## 🚀 Installation & Usage

### 🔹 Kali Linux
```bash
# 1. Clone the repo
git clone https://github.com/hackersarmy2008-star/Number-osint-.git

# 2. Go inside folder
cd Number-osint-

# 3. Install dependencies
pip3 install phonenumbers requests

# 4. Make script executable
chmod +x number-osint.py

# 5. Run the tool
python3 number-osint.py

```
### 🔹android termux 
```bash
# 1. Update Termux
pkg update -y && pkg upgrade -y

# 2. Install Python & Git
pkg install python git -y

# 3. Clone the repo
git clone https://github.com/hackersarmy2008-star/Number-osint-.git

# 4. Go inside folder
cd Number-osint-

# 5. Install dependencies
pip install phonenumbers requests

# 6. Run the tool
python number-osint.py
```
stay ethical 
