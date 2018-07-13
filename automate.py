import getpass
import PyPDF2
import re
import io
import smtplib
import sys
import os.path as op
import math
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import tkinter
from tkinter.filedialog import askopenfilename

def pdfparser(data):

    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()

    fp.close()
    return data


def extractMail(pdf, pgnum):
    str = pdfparser(pdf)
    match = re.findall(r'[\w\.-]+@[\w\.-]+', str)
    print(match)
    try:
        return match[0]
    except IndexError:
        print("No e-mail address found in group ", pgnum)


def PDFsplit(pdf, gmail_user, subject, message, group):
    pdfFileObj = open(pdf, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    numPages = pdfReader.numPages
    start = 0
    end = group
    i = 0
    while i < numPages:
        i += group
        temp = i / group
        pdfWriter = PyPDF2.PdfFileWriter()
        outputpdf = pdf.split('.pdf')[0] + str(temp) + '.pdf'
        try: 
            for page in range(start, end):
                pdfWriter.addPage(pdfReader.getPage(page))
            with open(outputpdf, "wb") as f:
                pdfWriter.write(f)
            mail = extractMail(outputpdf, temp)
            if mail:
                files = []
                send = input("Enter X to send / ANY other key to skip: ")
                if send == 'x' or send == 'X':
                    files.append(op.abspath(outputpdf))
                    send_mail(gmail_user, mail, subject, message, files)
            start = end
            end += group
        except IndexError:
            end = numPages
            with open(outputpdf, "wb") as f:
                pdfWriter.write(f)
            mail = extractMail(outputpdf, temp)
            if mail:
                files = []
                send = input("Enter X to send / ANY other key to skip: ")
                if send == 'x' or send == 'X':
                    files.append(op.abspath(outputpdf))
                    send_mail(gmail_user, mail, subject, message, files)
    pdfFileObj.close()

def send_mail(send_from, send_to, subject, message, files=[]):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    if not len(files) == 0:
        for path in files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(op.basename(path)))
            msg.attach(part)

    smtpserver.sendmail(send_from, send_to, msg.as_string())


gmail_user = input("USERNAME: ")
gmail_pwd = getpass.getpass("PASSWORD: ")
try:
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
except smtplib.SMTPAuthenticationError:
    print("Wrong E-mail / Password. \n")
    q = input("Press ENTER to quit")
    sys.exit()
subject = input("Enter common SUBJECT: \n")
message = input("Enter common MESSAGE: \n")
#pathToPdf = input("Enter full path to PDF: ")
print("OPEN PDF FILE\n")
tkinter.Tk().withdraw()
pathToPdf = askopenfilename()
group = int(input("Enter number of pages to be grouped while splitting: "))
PDFsplit(pathToPdf, gmail_user, subject, message, group)
ex = input("Press ENTER to quit")
