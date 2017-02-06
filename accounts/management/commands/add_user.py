from django.core.management.base import BaseCommand
from accounts.models import MyUser
from allauth.account.models import EmailAddress

DEFAULT_USER = [
    'dnsp55514@hanmail.net',
    'wowcar7777@naver.com',
    'bbo_ran_choi@naver.com',
    'bhraaaaa@naver.com',
    'sahasaha_@daum.net',
    'ooojinsum@naver.com',
    'pahooo90@naver.com',
    'hgqg09081@naver.com',
    'jhl60003@naver.com',
    'leedoha__125@naver.com',
    'tajunhello@gmail.com',
    'eej890830@hanmail.net',
    'hhh11789@nate.com',
    'dlguswls123@naver.com',
    'youyoungyou@naver.com',
    'ohsong1551@gmail.com',
    'mimitripking@naver.com',
    'jajosa_591@naver.com',
    '1029104@naver.com',
    'baehyerilove@naver.com',
    'junnmom_likes@naver.com',
    'sarangggun92@gmail.com',
    'ahahaha2211@gmail.com',
    'alsgpchdd@naver.com',
    'rrlawoalsvvv87@daum.net',
    'thekingbeauty@naver.com',
    'hihogamji@gmail.com',
    'yeondewrara@naver.com',
    'mijangior@naver.com',
    'kim_sunghoaa@naver.com',
    'jejusonja678@naver.com',
    'mi__randa@naver.com',
    'fireballone2@naver.com',
    'hyunjin45823@naver.com',
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in DEFAULT_USER:
            if not MyUser.objects.filter(email=user).exists():
                my_user = MyUser.objects.create_user(user, "qwqw1212")

                email_conform = EmailAddress.objects.create(
                    user=my_user,
                    email=user
                )
                email_conform.verified = True
                email_conform.primary = True
                email_conform.save()
