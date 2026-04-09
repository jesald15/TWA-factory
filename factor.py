import json
import os
import subprocess
import shutil

# --- STYLING CONSTANTS ---
HEADER = """
  _______       _____       _________   ________________  ______  __
 /_  __/ |     / /   |     / ____/   | / ____/_  __/ __ \/ __ \ \/ /
  / /  | | /| / / /| |    / /_  / /| |/ /     / / / / / / /_/ /\  / 
 / /   | |/ |/ / ___ |   / __/ / ___ / /___  / / / /_/ / _, _/ / /  
/_/    |__/|__/_/  |_|  /_/   /_/  |_\____/ /_/  \____/_/ |_| /_/   
                                                                    
"""

INSTRUCTIONS = """
----------------------------------------------------------------------------
                       🚀 TWA FACTORY SETUP & USAGE
----------------------------------------------------------------------------
1. PRE-FLIGHT CHECK:
   - Ensure 'icon.png' is in this folder (Must be 512x512).
   - Asset Server MUST be running: `python -m http.server 8081`
   - Keystore location: /home/jes/Documents/Projects/BubbleWrap/android.keystore
   - Keystore Password: [ 123456 ] (Used for both store and alias)

2. DEPLOYMENT (ADB):
   - First time install:  `adb install app-release-signed.apk`
   - Update existing app: `adb install -r app-release-signed.apk`
   - Troubleshooting: If incremental fails, the script uses Streamed Install.

3. CLEANING:
   - Every build wipes 'app/', 'web-build/', and 'twa-manifest.json'
     to ensure zero terminal prompts.
----------------------------------------------------------------------------
"""

def clean_workspace():
    """Nuclear wipe of old build metadata to prevent terminal prompts."""
    print("\n[*] TWA Factory: Sanitizing workspace...")
    targets = ['app', 'web-build', 'twa-manifest.json', 'manifest-checksum.txt']
    for t in targets:
        path = os.path.join(os.getcwd(), t)
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            else:
                os.remove(path)
    print("[*] Success: Workspace is clean.")

def run_factory():
    os.system('clear')
    print(HEADER)
    print(INSTRUCTIONS)
    
    # 1. User Input
    print("\n[+] STARTING NEW BUILD ENGINE...")
    app_name = input("  ? App Name       : ").strip()
    domain = input("  ? Domain (URL)   : ").strip().replace("https://", "").replace("http://", "")
    theme_color = input("  ? Theme Color    : ").strip() or "#000000"
    
    # Auto-generate package ID
    clean_name = "".join(filter(str.isalnum, app_name.lower()))
    package_id = f"com.jes.twa.{clean_name}"

    # 2. Cleanup
    clean_workspace()

    # 3. Create the TWA Manifest
    manifest = {
        "packageId": package_id,
        "host": domain,
        "name": app_name,
        "launcherName": app_name,
        "display": "standalone",
        "themeColor": theme_color,
        "backgroundColor": "#000000",
        "startUrl": "/",
        "appVersion": "1",
        "appVersionCode": 1,
        "signingKey": {
            "path": "/home/jes/Documents/Projects/BubbleWrap/android.keystore",
            "alias": "android"
        },
        "iconUrl": "http://127.0.0.1:8081/icon.png",
        "webManifestUrl": "http://127.0.0.1:8081/manifest.json",
        "fullScopeUrl": f"https://{domain}/",
        "minSdkVersion": 21,
        "orientation": "any",
        "displayOverride": ["fullscreen", "minimal-ui"]
    }

    with open('twa-manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    # 4. The Build Execution
    env = os.environ.copy()
    env["ANDROID_SDK_ROOT"] = "/home/jes/.bubblewrap/android_sdk"
    env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0" 

    try:
        print(f"\n[*] INITIALIZING: {app_name}")
        # Initialize
        subprocess.run([
            "bubblewrap", "init", 
            "--manifest=http://127.0.0.1:8081/manifest.json", 
            "--yes"
        ], env=env, check=True)
        
        print(f"\n[*] COMPILING APK (Be ready to enter passwords)...")
        # Build
        subprocess.run(["bubblewrap", "build", "--skipPwaValidation", "--yes"], env=env, check=True)
        
        print("\n" + "="*60)
        print(f"  ✅ SUCCESS: {app_name.upper()} IS READY!")
        print(f"  📁 PATH: {os.getcwd()}/app-release-signed.apk")
        print(f"  📲 RUN: adb install app-release-signed.apk")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ FACTORY ERROR: Build failed.")
        print(f"Details: {e}")

if __name__ == "__main__":
    run_factory()