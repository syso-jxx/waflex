import smtplib
from email.mime.text import MIMEText
import string 
import random 

class MyMail:
    def mysendmail(self, recvEmail, title):

        smtpName = "smtp.gmail.com" #smtp 서버 주소
        smtpPort = 587 #smtp 포트 번호
        
        sendEmail = "email"
        password = "password"
        
        _LENGTH = 8 # 8자리 
        # 숫자 + 대소문자 + 특수문자
        
        alpha_s = string.ascii_lowercase
        alpha_b = string.ascii_uppercase
        digit = string.digits
        temp = ['~','!','@','#','$','%','^','*']
        
        # 랜덤한 문자열 생성 
        result = alpha_s[random.randrange(0, 26)] + alpha_s[random.randrange(0, 26)]
        result += alpha_b[random.randrange(0, 26)] + alpha_b[random.randrange(0, 26)]
        result += digit[random.randrange(0, 10)] + digit[random.randrange(0, 10)]
        result += temp[random.randrange(len(temp))] + temp[random.randrange(len(temp))]
        
        text = "인증하실 번호는 " +result+" 입니다."
        msg = MIMEText(text) #MIMEText(text , _charset = "utf8")
        
        msg['Subject'] = title
        msg['From'] = sendEmail
        msg['To'] = recvEmail
        print(msg.as_string())
        
        s=smtplib.SMTP( smtpName , smtpPort ) #메일 서버 연결
        s.starttls() #TLS 보안 처리
        s.login( sendEmail , password ) #로그인
        s.sendmail( sendEmail, recvEmail, msg.as_string() ) #메일 전송, 문자열로 변환하여 보냅니다.
        s.close() #smtp 서버 연결을 종료합니다.
        
        return result



