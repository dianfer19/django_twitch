import base64
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
            from_mail = envelope.from_[0]

            print('mailbox:', from_mail.mailbox.decode('UTF-8'))
            print('host:', from_mail.host.decode('UTF-8'))
            print('Asunto:', envelope.subject.decode())

            # Obtener el cuerpo del mensaje
            email_message = email.message_from_bytes(data[b'RFC822'])
            for part in email_message.walk():
                if part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
                    # Obtener la codificación del contenido y el payload
                    charset = part.get_content_charset() if part.get_content_charset() else 'utf-8'
                    payload = part.get_payload(decode=False)
                    # Comprobar si la codificación de transferencia de contenido es base64
                    if part.get('Content-Transfer-Encoding') == 'base64':
                        # Decodificar desde base64 y luego decodificar los bytes con la codificación del charset
                        cuerpo_bytes = base64.b64decode(payload)
                        cuerpo = cuerpo_bytes.decode(charset, errors='replace')
                    else:
                        if isinstance(payload, bytes):
                            cuerpo = payload.decode(charset, errors='replace')
                        else:
                            # Si el payload ya es una cadena de texto, lo usamos directamente
                            cuerpo = payload
                    print('Cuerpo:', cuerpo)
            vo = Mail()
            vo.de = f'{from_mail.mailbox.decode("UTF-8")}@{from_mail.host.decode("UTF-8")}'
            vo.asunto = envelope.subject.decode()
            vo.cuerpo = cuerpo
            vo.leido = True
            vo.save()
            client.add_flags(msg_id, [b'\\Seen'])


def start():
    scheduler = BackgroundScheduler(timezone="America/Guayaquil")
    try:
        scheduler.remove_all_jobs()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(func=leer_bandeja, trigger="interval", seconds=30,
                          id="leer_bandeja")
        scheduler.print_jobs()
        scheduler.start()
    except Exception as e:
        print("Deteniendo los jobs" + str(e))
