# 🚀 TWA Factory v1.0

  _______       _____       _________   ________________  ______  __
 /_  __/ |     / /   |     / ____/   | / ____/_  __/ __ \/ __ \ \/ /
  / /  | | /| / / /| |    / /_  / /| |/ /     / / / / / / /_/ /\  / 
 / /   | |/ |/ / ___ |   / __/ / ___ / /___  / / / /_/ / _, _/ / /  
/_/    |__/|__/_/  |_|  /_/   /_/  |_\____/ /_/  \____/_/ |_| /_/   
                                                                    


A high-speed, terminal-based Android TWA (Trusted Web Activity) APK builder designed for Arch Linux. This tool automates the `bubblewrap` CLI to generate signed APKs from any URL with zero interactive prompts during the build process.

## 🛠️ System Requirements
- **Tools**: `bubblewrap`, `jdk-openjdk`, `android-sdk`
- **Python**: 3.x (with `Pillow` for icon validation)

## 📋 Pre-Flight Instructions
Before running the factory, ensure the following are ready in the root directory:

1.  **Icon**: Place an `icon.png` in this folder. It **MUST** be exactly `512x512`.
2.  **Asset Server**: Bubblewrap needs to verify your PWA assets during initialization. Open a separate terminal and run:
    ```bash
    python -m http.server 8081
    ```

## 🚀 Usage

Run the interactive wizard:
```bash
python factor.py

The wizard will ask for:

App Name: The display name of your app.

Domain: The target URL (e.g., www.youtube.com).

Theme Color: Hex code for the status bar (e.g., #0F0F0F).

# Deployment (ADB)
Once the build is complete, your signed APK (app-release-signed.apk) will be in the root folder.

Install on device:

Bash
# For a fresh install
adb install app-release-signed.apk

# To update an existing version
adb install -r app-release-signed.apk
🧹 Features
Zero-Footprint: Automatically wipes app/ and temporary metadata before every build to prevent "checksum" or "version" prompts.

SSL Bypass: Includes a built-in fix for local issuer certificate errors often found in Node/Arch environments.

Automated Manifesting: Generates the twa-manifest.json dynamically based on your input.

---

### Pro-Tip for your GitHub Repo:
If you want to add that **ASCII Heading** specifically to the top of the README, you can wrap it in a code block like this:

```text
```text

s