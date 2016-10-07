import logging.handlers


from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders

from email.utils import COMMASPACE, formatdate
import smtplib

import ssl
			
import os

class CoolSMTPHandler(logging.handlers.SMTPHandler):
    ''' de moment nomes funciona amb TLS/SSL al port 465 '''
    #class logging.handlers.SMTPHandler(mailhost, fromaddr, toaddrs, subject, credentials=None, secure=None, timeout=1.0)
    def __init__(self, *args, **kwargs):
        self.security=None
        if 'security' in kwargs:
            self.security = kwargs['security']
            del kwargs['security']
        super().__init__(*args, **kwargs)
        
    def emit(self, record):
        """
        Emit a record.
        Format the record and send it to the specified addressees.
        """
        #try:
        # creem el contenidor de cada una de les partsde lemail
        msgRoot = MIMEMultipart('mixed')
        msgRoot['From'] = self.fromaddr
        msgRoot['To'] = ",".join(self.toaddrs)
        msgRoot['Subject'] = self.getSubject(record)
        msgRoot['Date'] = formatdate(localtime=True)

        # enviem sempre amb html
        partBody = MIMEMultipart('related')
        body = self.format(record)
        partText = MIMEText(body, "plain", _charset='utf-8')
        partBody.attach(partText)
        msgRoot.attach(partBody)
        
        #smtplib.SMTP_SSL(host='', port=0, local_hostname=None, keyfile=None, certfile=None, [timeout, ]context=None, source_address=None)
        smtp = smtplib.SMTP_SSL(self.mailhost)

        if self.username is not None:
            #smtp.ehlo() # for tls add this line
            #smtp.starttls() # for tls add this line
            #smtp.ehlo() # for tls add this line
            smtp.login(self.username, self.password)		
        #SMTP.send_message(msg, from_addr=None, to_addrs=None, mail_options=[], rcpt_options=[])¶
        smtp.send_message(msgRoot, self.fromaddr, self.toaddrs)
        smtp.quit()
        #except (KeyboardInterrupt, SystemExit):
        #	raise
        #except:
        #	self.handleError(record)


class TlsSMTPHandler(logging.handlers.SMTPHandler):
	def emit(self, record):
		"""
		Emit a record.
		Format the record and send it to the specified addressees.
		"""
		try:

			#try:
			#	from email.utils import formatdate
			#except ImportError:
			#	formatdate = self.date_time
			
			# creem el contenidor de cada una de les partsde lemail
			msgRoot = MIMEMultipart('mixed')
			msgRoot['From'] = self.fromaddr
			msgRoot['To'] = ",".join(self.toaddrs)
			msgRoot['Subject'] = self.getSubject(record)
			msgRoot['Date'] = formatdate(localtime=True)
					 
			# enviem sempre amb html
			partBody = MIMEMultipart('related')
			body = self.format(record)
			partText = MIMEText(body, "plain", _charset='utf-8')
			partBody.attach(partText)
			msgRoot.attach(partBody)
												 
			# enviem lemail
			port = self.mailport
			if not port:
				port = smtplib.SMTP_PORT
			smtp = smtplib.SMTP(self.mailhost, port)
			
			if self.username:
				smtp.ehlo() # for tls add this line
				smtp.starttls() # for tls add this line
				smtp.ehlo() # for tls add this line
				smtp.login(self.username, self.password)		
			smtp.sendmail(self.fromaddr, self.toaddrs, msgRoot.as_string())
			smtp.quit()
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)

'''
class TlsSMTPHandler(logging.handlers.SMTPHandler):
	def emit(self, record):
		"""
		Emit a record.
		Format the record and send it to the specified addressees.
		"""
		try:

			#try:
			#	from email.utils import formatdate
			#except ImportError:
			#	formatdate = self.date_time
			port = self.mailport
			if not port:
				port = smtplib.SMTP_PORT
			smtp = smtplib.SMTP(self.mailhost, port)
			msg_fmt = self.format(record)
			print("------->%s<--------" % msg_fmt)
			msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            self.fromaddr,
                            ",".join(self.toaddrs),
                            self.getSubject(record),
                            formatdate(), msg_fmt)
			if self.username:
				smtp.ehlo() # for tls add this line
				smtp.starttls() # for tls add this line
				smtp.ehlo() # for tls add this line
				smtp.login(self.username, self.password)
			print(" ======", msg, type(msg))
			#msg=strmsg.decode()
			#smtp.sendmail(self.fromaddr, self.toaddrs, msg)
			#smtp.quit()
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)
'''

def sendMail(serverport, fro, to, subject, body, cc=[], bcc=[], replyto=[], typ='text', files=[], attachs=[], credentials=None, usetls=False):
	#print ('----', serverport, fro, to, subject, body, cc, bcc, replyto, typ, files, attachs, credentials, usetls)
	assert type(to)==list
	assert type(files)==list
		
	# creem el contenidor de cada una de les partsde lemail
	msgRoot = MIMEMultipart('mixed')
	msgRoot['From'] = fro
	msgRoot['To'] = COMMASPACE.join(to)
	msgRoot['Date'] = formatdate(localtime=True)
	msgRoot['Subject'] = subject

	to_addrs = to[:]
	if cc!=[]:
		vcc = COMMASPACE.join(cc)
		msgRoot.add_header('Cc', vcc)
		to_addrs+=cc
	if bcc!=[]:
		to_addrs+=bcc
	if replyto!=[]:
		vreplyto = COMMASPACE.join(replyto)
		msgRoot.add_header('Reply-To', vreplyto)
			
	if typ=='text':
		partText = MIMEText(body, 'plain', _charset='utf-8')
		msgRoot.attach(partText)
	elif typ=='html':
		partBody = MIMEMultipart('related')
		# dades, html
		partText = MIMEText(body, 'html', _charset='utf-8')
		partBody.attach(partText)
		'''
		# construim els attachs fixes related, es a dir que accedirem desde el html
		for attach in attachs:
			mode = attach['mode'] if 'mode' in attach else 'attachment'
			if mode == 'inline':
				typ, ext = attach['type'].split('/')
				if typ=='image':
					pio = self.conf['basedir'] + self.conf['attachsdir']
					f = open(pio + attach['filename'],"rb")
					partImg = MIMEImage(f.read(), ext, name=attach['filename'])
					f.flush()
					f.close()
					partImg.add_header('Content-ID', '<%s>' % attach['name'])
			
					partImg.add_header('Content-Disposition', mode, filename=attach['filename'])
					partBody.attach(partImg)
				else:
					TypeError("No existeix el tipus d'adjunt: %s" % typ)
		'''
		msgRoot.attach(partBody)	
	'''
	# construim els attachs fixes no related
	for attach in attachs:
		mode = attach['mode'] if 'mode' in attach else 'attachment'
		if mode == 'attachment':
			typ, ext = attach['type'].split('/')
			if typ=='image':
				pio = self.conf['basedir'] + self.conf['attachsdir']
				f = open(pio + attach['filename'],"rb")
				partImg = MIMEImage(f.read(), ext, name=attach['filename'])
				f.flush()
				f.close()
				partImg.add_header('Content-ID', '<%s>' % attach['name'])
			
				partImg.add_header('Content-Disposition', mode, filename=attach['filename'])
				msgRoot.attach(partImg)
			else:
				TypeError("No existeix el tipus d'adjunt: %s" % typ)
	'''
	# construim els attachs normals generats com a consequencia de lexecucio de linforme
	for file in files:
		part = MIMEBase('application', "octet-stream")
		f = open(file,"rb")
		part.set_payload(f.read())
		f.flush()
		f.close()
		encoders.encode_base64(part)
		#part.add_header('Content-ID', '<%s>' % os.path.basename(file))
		part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
		msgRoot.attach(part)

	# enviem l'email
	if isinstance(serverport, tuple):
		server, port = serverport
	else:
		server, port = serverport, smtplib.SMTP_PORT
	smtp = smtplib.SMTP(server, port)
	
	if credentials is not None:
		user, passwd = credentials
		if usetls:
			smtp.ehlo() # for tls add this line
			smtp.starttls() # for tls add this line
			smtp.ehlo() # for tls add this line
		smtp.login(user,passwd)	
	smtp.sendmail(fro, to_addrs, msgRoot.as_string() )
	smtp.close()





'''
def _construir_email(self, text, files, attachs, typ):
	logfun = logging.getLogger("reportinglog")
		
	start = time.time()
	v_msg='e-mail'
	logfun.info('Enviant ' + v_msg  + '...')

	fromaddr = self.conf['name'] + '<' + self.conf['from'] + '>'
	toaddrs = self.meta['to']
	ccaddrs = self.meta['cc']
	bccaddrs = self.meta['bcc']
	replyto = self.meta['replyto'] #if 'replyto' in self.meta else None
	subject= self.meta['subject']

	#files =[self.conf['basedir'] + self.conf['genreportsdir'] + self.meta['nomfitxer']]

	server=self.conf['smtp']
	user=self.conf['user']
	passwd=self.conf['passwd']

	sendMail(fromaddr, toaddrs, ccaddrs, bccaddrs, replyto, subject, text, files, attachs, server, user, passwd, typ)

	end = time.time()
	logfun.info( 'Fi ' + v_msg + ', s\'ha trigat: %.f minuts %.f segons' % ((end-start)/60, (end-start) % 60) )

'''
