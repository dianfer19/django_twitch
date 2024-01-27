import email

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from imapclient import IMAPClient

from automatizacion.models import Prueba, Mail


def leer_bandeja():
    print('leyendo bandeja de entrada')
    HOST = settings.EMAIL_HOST  # Ajusta esto para tu servidor IMAP
    USERNAME = settings.EMAIL_HOST_USER
    PASSWORD = settings.EMAIL_HOST_PASSWORD

    with IMAPClient(HOST) as client:
        client.login(USERNAME, PASSWORD)
        client.select_folder('INBOX', readonly=False)

        # Buscar correos no leídos
        messages = client.search(['UNSEEN'])
        print('_____________________________________________________________')
        for msg_id, data in client.fetch(messages, ['ENVELOPE', 'RFC822']).items():
            envelope = data[b'ENVELOPE']
            print('De:', envelope.from_)
            print('Asunto:', envelope.subject.decode())

            # Obtener el cuerpo del mensaje
            email_message = email.message_from_bytes(data[b'RFC822'])
            for part in email_message.walk():
                if part.get_content_type() == 'text/plain':
                    vo = Mail()
                    vo.de = envelope.from_
                    vo.asunto = envelope.subject.decode()
                    vo.cuerpo = str(part.get_payload(decode=True).decode())
                    vo.save()
                    print('Cuerpo:', vo.cuerpo)
            client.add_flags(msg_id, [b'\\Seen'])


def start():
    scheduler = BackgroundScheduler(timezone="America/Guayaquil")
    try:
        scheduler.remove_all_jobs()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(func=leer_bandeja, trigger="interval", seconds=40,
                          id="leer_bandeja")
        scheduler.print_jobs()
        scheduler.start()
    except Exception as e:
        print("Deteniendo los jobs" + str(e))
