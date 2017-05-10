# -*- coding: utf-8 -*-

# 파싱된 데이터 처리(DB입출력/이메일발송/파일입출력 등)

from __future__ import unicode_literals
import json
import codecs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = codecs.open('EventAlarm.json', 'a', encoding='utf-8')

    def send_mail(self, title, message, id):

        gmailUser = 'your_gmail_id'
        gmailPassword = 'your_gmail_pw'
        recipient = 'recipient_mail'

        html = """\
                <html>
                  <head></head>
                  <body>
                    <p>""" + title + """<br>
                       <a href="https://www.temp-url.net/Board/BoardView.aspx?system=Board&BoardType=Normal&FromOuterYN=N&fdid=5112&MsgId="""+id+"""&DateBarYN=Y">EVENT LINK</a>
                    </p>
                  </body>
                </html>
                """

        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = recipient
        msg['Subject'] = title
        msg.attach(MIMEText(html, 'html'))

        '''
        Go to this link and select Turn On
        https://www.google.com/settings/security/lesssecureapps
        '''
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipient, msg.as_string())
        mailServer.close()
        print("================ [send_mail] =================")

    def process_item(self, item, spider):
        for json_file in reversed(open("EventAlarm.json").readlines()):
            data =json.loads(json_file.decode("utf-8-sig"))
            if int(item['date'].replace(".", '')) < int(data['date'].replace(".", '')):
                break
            elif item['id'] == data['id']:
                break
            else:
                self.send_mail("event alarm", item['title'], item['id'])
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.file.write(line)
                break
        print("================ [process_item] =================")
        return item

    def spider_closed(self, spider):
        print("================ [spider_closed] =================")
        self.file.close()
