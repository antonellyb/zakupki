START=$(date +"%Y-%m-%d %H-%M-%S")
python3 /home/roveo/data/zakupki/py/update.py daily 2>&1 | tee -a /home/roveo/data/zakupki/log/daily_update.log | tee /home/roveo/data/zakupki/log/daily_email.log
END=$(date +"%Y-%m-%d %H-%M-%S")
sendemail -f leo.schwartz@icloud.com -t leo.schwartz@icloud.com -u "zakupki update report "$(date +"%Y-%m-%d %H:%M:%S") -m $"Daily update executed $START : $END.\n" -a /home/roveo/data/zakupki/log/email.log -s smtp.mail.me.com:587 -xu leo.schwartz@me.com -xp Triest15 -o tls=yes