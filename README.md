# Capture The Flag
Create your own Capture the Flags

<img width="1148" height="841" alt="Screenshot 2026-04-04 200250" src="https://github.com/user-attachments/assets/ff88d458-56db-46b1-afe5-7f75d288dee5" />

## Description
Wanted to create a standalone CTF server to host offline.

HIGHLY RECOMMEND not using a special password, hashing has not been added yet.

Usernames and passwords are stored in `/ctf/data/users.yaml`

Tasks and flags are stored in `/ctf/data/flags.yaml`

Flag submissions are stored in `/ctf/data/submissions.yaml`

You can modify any  of those files to reset users, flags and submissions.


## Dependencies
```
pip install flask pyyaml
```

## Install
Git this repo
```
git clone https://github.com/bwithe/ctf
```

Start the webserver
```
cd ctf/app
python main.py
```



## Screenshots
### Login

<img width="740" height="471" alt="Screenshot 2026-04-04 195836" src="https://github.com/user-attachments/assets/3a9f7693-7a40-480f-bc9a-4e6b414d02df" />

### Register

<img width="806" height="552" alt="Screenshot 2026-04-04 195906" src="https://github.com/user-attachments/assets/ac7ad616-b0d7-4293-ae63-904a8b727373" />

### Home

<img width="909" height="475" alt="Screenshot 2026-04-04 195923" src="https://github.com/user-attachments/assets/426ecb2a-f31c-4b66-9710-e0af32ff0ecf" />

### CTF Management

<img width="1117" height="796" alt="Screenshot 2026-04-04 200003" src="https://github.com/user-attachments/assets/9b0f1d85-0ab0-4611-abee-455a6d6930eb" />

### Capture The Flags

<img width="2282" height="549" alt="Screenshot 2026-04-04 200245" src="https://github.com/user-attachments/assets/9a64418a-e37c-45da-97fb-42094b04ead8" />

### Leaderboard

<img width="1148" height="841" alt="Screenshot 2026-04-04 200250" src="https://github.com/user-attachments/assets/d7db0d69-363c-4c15-831d-9af17d35e5dd" />
