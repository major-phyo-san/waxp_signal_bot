WAXP Signal Bot (Signal Only + Telegram Notify)

Run Bot
---------------------------------------------------------
1. Install Pydroid 3 (Android)
2. Open Terminal and run:
   pip install requests pandas ta schedule

3. Edit config.py -> Fill in your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
4. Run main.py to start the bot.
   It checks WAXP hourly and sends signal to Telegram.

Deploy Bot
---------------------------------------------------------
Virtual Environment

cd ~/working-dir

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

Doc
http://<your-server-ip>:5000/docs

Systemd service

sudo nano /etc/systemd/system/waxp-bot-runner.service

========
[Unit]
Description=Waxp Bot Run Service
After=network.target

[Service]
User=ubuntu
Group=ubuntu

OR
User=www-data
Group=www-data

WorkingDirectory=/path/to/working-dir
Environment="PATH=/path/to/working-dir/venv/bin"
ExecStart=/path/to/working-dir/venv/bin/python3 main.py

[Install]
WantedBy=multi-user.target

=========
sudo systemctl daemon-reload
sudo systemctl enable waxp-bot-runner
sudo systemctl start waxp-bot-runner