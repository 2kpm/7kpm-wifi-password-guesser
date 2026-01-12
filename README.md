# 🔐 7KPM Wi-Fi Password Guesser (Educational)

> ⚠️ **Educational Use Only**  
> This project is designed **strictly for learning, lab environments, and cybersecurity education** (e.g., TryHackMe).  
> **Do NOT use this tool against real networks you do not own or have permission to test.**

---

## 📌 Project Description

**7KPM Wi-Fi Password Guesser** is a Python-based **educational password-guessing simulator**.  
It demonstrates how weak Wi-Fi passwords can be guessed in a **controlled lab environment**, helping learners understand cybersecurity concepts safely.

---

## 🎯 Purpose

This project helps learners understand:

- How password-guessing attacks work conceptually
- The importance of strong Wi-Fi passwords
- How wordlists and loops work in Python
- Handling success and failure logic in connection attempts

---

## 🧠 Features

- Scans nearby Wi-Fi networks (SSID, security type, signal strength)
- Displays networks in a clean terminal interface
- Lets user select a target network
- Iterates through a predefined password list
- Simulates connection attempts
- Stops when the correct password is found

> ⚠️ Real attack functionality is **not implemented** — this is an educational simulator.

---

## 🛠 Technologies Used

- Python 3
- Linux terminal / `nmcli` (for simulation)
- ASCII / Unicode terminal UI
- Wordlist-based guessing logic

---

## 🧪 Intended Environment

- ✔ TryHackMe / CTF-style labs  
- ✔ Local test networks you own  
- ✔ Simulated or mock environments  

❌ **Not for unauthorized Wi-Fi networks**

---

## 📂 Example Usage

```bash
python3 password_guesser.py



Terminal output example:


══════════════════════════════════════════════════
#  ★ SSID                           Sec      Signal
────────────────────────────────────────────────
 1 ★ HomeNetwork                     WPA2         0%
 2   LabWiFi                         Open        29%
 3   GuestNet                        WPA2         0%
══════════════════════════════════════════════════

⚖️ Legal & Ethical Disclaimer

This project is for educational purposes only.
Unauthorized access to networks is illegal. The author is not responsible for misuse.

✍️ Author

7KPM
Cybersecurity learner • Linux • Python
2026 Edition


6. **Intended environment** → prevents misuse  
7. **Example usage** → shows how to run it  
8. **Disclaimer / ethics** → legal safety  
9. **Author info** → branding / “7KPM” signature  

