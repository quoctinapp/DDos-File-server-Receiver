# DDos-File-server-Receiver

## How to Use It:

### Step 1: Clone the repository
Clone the project from GitHub using the following command:
```bash
git clone https://github.com/quoctinapp/DDos-File-server-Receiver.git
```

### Step 2: Install Required Packages
Navigate to the project directory and install the necessary dependencies:
```bash
pip install requests tqdm
```
Ensure the following modules are available in your environment:
```python
import requests
import random
import time
import ipaddress
import string
import threading
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os
import platform
```

### Step 3: Update the User-Agent File Path
Before running the program, update the user-agent file path in `ddos.py` at **line 91**:
Replace the existing path with the correct one.

**Example Placeholder:** `![Description](https://github.com/quoctinapp/DDos-File-server-Receiver/blob/main/Line_91.png?raw=true)`

### Step 4: Run the Program
Execute the script using:
```bash
python ddos.py
```
Enjoy using it!

