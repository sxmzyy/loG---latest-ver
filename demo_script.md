# Android Forensic Tool - 6-Minute Pitch Script

## 🛠️ Pre-Pitch Setup
1. **Generate Data:** Run `python analysis/generate_sample_data.py`.
2. **Start Servers:** `python main.py` AND `powershell -File start-server.ps1`.
3. **Browser:** Open `http://127.0.0.1:8082` at 110% Zoom.

---

## 🎤 The Pitch (Total Time: ~6:00)

### 0:00 - 1:00 | 1. The Hook: "Data vs. Intelligence"
**"Good morning. I'm here to present the Android Forensic Tool.**

**Let's start with a problem every investigator faces: *Data Overload*.**
**Modern smartphones are black boxes containing terabytes of information. Standard forensic tools are great at dumping this data—they give you a 10,000-page PDF of raw logs. But they don't give you *answers*.**

**If you have 48 hours to solve a case, you don't have time to read 50,000 text messages. You need to know: *Who is the ringleader? Where is the money going? And who are they calling on WhatsApp?***

**[ACTION: Show Dashboard]**
**That is why we built this tool. It is not just an extractor; it is an Intelligence Platform. It forces the data to tell a story.**
**Here is the Dashboard. It’s your single pane of glass, giving you an immediate health check of the device and the case status."**

### 1:00 - 1:45 | 2. Acquisition (Seamless & Universal)
**[ACTION: Click 'Extract Logs' in Sidebar]**
**"First, let's talk about Acquisition.**
**We’ve heard that proprietary tools are expensive and hard to use. We wanted 'Plug-and-Play'.**
**Our tool uses universal ADB communication. You plug in *any* Android device, select your artifacts—Standard Logs or Deep System Dumps—and hit 'Start'.**

**Behind the scenes, we aren't just copying files. We are performing real-time parsing, stripping out system noise, and preparing the data for the intelligence engine."**

### 1:45 - 2:45 | 3. Log Analysis & The "Hidden" Data (VoIP)
**"Now, let's look at the data. Standard tools show you SMS and Cellular calls.**

**[ACTION: Click 'SMS Messages', then 'Call Logs']**
**We do that too, but we go deeper. We know criminals use VoIP—WhatsApp, Telegram, Signal—to hide.**

**[ACTION: Click 'Logcat Viewer' or mention 'Advanced Timeline']**
**Our parser creates a 'Unified Timeline'. It identifies VoIP calls by analyzing low-level system events.**
**For example, if I search for a WhatsApp call here, I don't just see a generic 'Data Usage' log. I see a specific tag: `Incoming Call (WhatsApp)`. We detect the explicit `VoipActivity` component from the system logs, proving a call took place even if the app tried to hide it."**

### 2:45 - 4:15 | 4. Forensic Intelligence (The Core Value)
**"This is where we leave the competition behind: *Forensic Intelligence*."**

#### A. Mule Hunter (Financial Fraud)
**[ACTION: Click 'Mule Hunter']**
**"Financial fraud is exploding. We built 'Mule Hunter' specifically for this.**
**Why call it 'Mule Hunter'? Money mules often use 'App Cloners' to run multiple instances of a banking app on one phone to launder money across different accounts.**
**Our logic scans for this specific signature: If we see greater than 5 banking apps AND the presence of 'Dual Space' software, we flag it as a 'Critical Risk'. Only a machine can spot this pattern instantly."**

#### B. Advanced Timeline (Ghost Gaps)
**[ACTION: Click 'Advanced Timeline']**
**"Next is the Timeline. We use 'Data Fusion' to merge every data source into one chronological stream.**
**But we also look for what is NOT there. We call them 'Ghost Gaps'.**
**If the timeline shows a blank space for 30 minutes, our algorithms flag it. Did the user turn the phone off? Did they wipe the logs? A gap is often as incriminating as a record."**

#### C. Social Link Graph (The Network)
**[ACTION: Click 'Social Link Graph']**
**"And finally, the Social Link Graph. We don't just give you a contact list.**
**We visualize the network.
*   **Nodes (Circles):** represent people. The **Size** isn't random; it represents 'Centrality'—mathematically, how important they are to the network.
*   **Edges (Lines):** represent the volume of communication.**

**You can instantly see the 'Key Person of Influence'. It might not be the person the suspect talks to the most, but the person who connects the suspect to the rest of a criminal group."**

### 4:15 - 5:15 | 5. Tools & Real-Time Monitoring
**"We also equip the investigator with tactical tools.**

**[ACTION: Click 'Privacy Profiler']**
**The 'Privacy Profiler' exposes spyware. We parse raw API calls—like `CameraService.connect`—to prove an app was recording video in the background.**

**[ACTION: Click 'Live Monitor']**
**And for live interrogations, we have the 'Live Monitor'. You can see device logs streaming in real-time. If the suspect receives a text message *during* the interview, you see it on your screen instantly."**

### 5:15 - 6:00 | 6. Integrity & Closing
**[ACTION: Click 'Legal Disclaimer']**
**"Finally, none of this matters if it doesn't hold up in court.**
**We built 'Chain of Custody' into the core. Every single file extracted is automatically hashed using SHA-256.**
**These hashes are stored in a tamper-proof metadata ledger (`evidence_metadata.json`). At any time, you can click 'Verify Hashes' to prove the evidence is untouched.**

**In summary: We are moving from 'Data Extraction' to 'Forensic Intelligence'. We help you solve the case in 4 hours, not 4 days.**

**Thank you."**
