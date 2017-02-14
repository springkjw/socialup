from django.core.management.base import BaseCommand
from django.conf import settings
import MySQLdb


db = MySQLdb.connect(
    host=settings.DATABASES['default']['HOST'],
    user=settings.DATABASES['default']['USER'],
    passwd=settings.DATABASES['default']['PASSWORD'],
    db=settings.DATABASES['default']['NAME']
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        cur = db.cursor()
        cur.execute('SELECT CONCAT("ALTER TABLE ", TABLE_NAME," CONVERT TO CHARACTER SET utf8") AS ExecuteTheString FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA="ebdb" AND TABLE_TYPE="BASE TABLE"')

        for row in cur.fetchall():
            print(row[0])
            new_sql = row[0]
            cur2 = db.cursor()
            cur2.execute(new_sql)

        db.close()
