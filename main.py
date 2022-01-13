import twitter
import time
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

consumer_key = ""
consumer_secret = ""
access_token_key = ""
access_token_secret = ""


hours_to_add = timedelta(hours=2)


api = twitter.Api(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token_key=access_token_key,
    access_token_secret=access_token_secret,
)


def send_an_error_mail(text):

    try:
        mail = ""
        msg = MIMEMultipart()
        msg["From"] = mail
        msg["To"] = mail
        msg["Subject"] = "ERREUR BOT"
        message = text
        msg.attach(MIMEText(message))
        mailserver = smtplib.SMTP("", 587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(mail, "")
        mailserver.sendmail(mail, mail, msg.as_string())
        mailserver.quit()
        print("Mail envoyé")
    except Exception as e:
        print(e)
        print("Envoie du mail a échoué.")


class Blague:
    text_to_search = ""
    text_to_write = ""
    media = ""
    last_tweet_responded_id = 0

    def __init__(self, res, text, m):
        self.text_to_search = res
        self.text_to_write = text
        self.media = m
        self.last_tweet_responded_id = 0

    def search_the_last_tweet_related(self):
        search_results = api.GetSearch(
            term=self.text_to_search, count=30, result_type="mixed", lang="fr"
        )  # On charge les 30 derniers tweets/retweets liés à la recherche. On prend 30 pr être large
        for search in search_results:
            if (
                search.retweeted_status == None and search.user.id != ""
            ):  # Pour être sûr qu'on ne prend pas en compte les retweets & les tweets qu'on a nous même fait
                return search

    def respond_to_a_tweet_and_retweet_the_answer(self, tweet):
        tweet = api.PostUpdate(
            "@" + tweet.user.screen_name + " " + self.text_to_write,
            in_reply_to_status_id=tweet.id,
            media=self.media,
        )
        # api.PostRetweet(tweet.id) #On retweet le tweet


#####################################################################


def main():

    # La règle des mots clés : si jamais les mots doivent être collés dans le recherche, reajouter "". Exemple : '"Mots collés" au lieu de "Mots collés"
    # OR : '(a OR B)' va chercher a ou b
    # "a b" va chercher A ET B mais pas collés

    millions = Blague(
        '"des millions"',
        "Des millions ? Vous savez déjà ce que ça fait un million, Larmina ?",
        "media/million.jpg",
    )
    arabo = Blague(
        "(arabo-musulman OR arabo-musulmans)", "Arabo... ?", "media/arabo.jpg"
    )
    dictature = Blague(
        "dictature",
        "Savez-vous seulement ce que c'est qu'une dictature ? Une dictature c'est quand les gens sont communistes, déjà. Qu'ils ont froid, avec des chapeaux gris et des chaussures à fermeture éclair. C'est ça une dictature.",
        "media/dictature.jpg",
    )
    chicha = Blague('(chicha OR narguilé OR "batard tu fumes")', "", "media/chicha.png")
    massage = Blague("massage (envie OR besoin)", "", "media/massage.mp4")
    arretez = Blague("arrêtez", "C'EST TOI ARRÊTEZ", "media/arretez.jpg")
    chauve = Blague("chauve -souris", "Chauve qui peut !", "media/chauve.jpg")
    # marginaux = Blague("(manifestation OR manif)", "Que veulent ces marginaux ?", "media/marginaux.jpg")
    noel = Blague(
        '"cadeau de noël" OR "cadeaux de noël" OR "bûche de noël" OR "guirelande de noël" OR "guirelandes de noël" OR "messe de noël"',
        "Il y a aussi les boules ...",
        "media/noel.jpg",
    )
    jacadi = Blague(
        '"je suis vegan" OR "je suis végétarien" OR "je suis végétarienne" OR "je suis vege" OR "je mange pas de porc"',
        "Ça fait un peu Jacadi a dit pas de charcuterie, vous trouvez pas ?",
        "media/jacadi.jpg",
    )
    lundi = Blague('"comment ça va ?"', "Comme un lundi !", "media/lundi.jpg")
    poissoniere = Blague(
        '"elle gueule"',
        "Elle gueule mon vieux, on dirait une poissonière de Ménilmontant",
        "media/poissoniere.jpg",
    )
    pere = Blague(
        '("marre de mon père" OR "mon père me saoule" OR "mon père me clc" OR "mon père me casse les couilles" OR "mon père est trop chiant" OR "mon père est chiant" OR "mon père clc" OR "mon père est casse-couille")',
        "",
        "media/pere.mp4",
    )
    chaleur = Blague(
        '("27 degrès" OR "28 degrès" OR "29 degrès" OR "30 degrès" OR "31 degrès" OR "32 degrès" OR "33 degrès" OR "34 degrès" OR "35 degrès" OR "36 degrès" OR "37 degrès" OR "38 degrès" OR "39 degrès" OR "40 degrès" OR "45 degrès" OR "50 degrès") lang:fr',
        "Quelle poutain chaleur",
        "media/chaleur.jpg",
    )

    blagues = [
        millions,
        dictature,
        arabo,
        chicha,
        massage,
        arretez,
        chauve,
        noel,
        jacadi,
        lundi,
        poissoniere,
        pere,
        chaleur,
    ]

    while True:

        random_time = random.randint(3600, 5400)
        has_this_blague_a_new_tweet_to_respond = False

        while has_this_blague_a_new_tweet_to_respond == False:

            blague = random.choice(blagues)

            tweet_found = blague.search_the_last_tweet_related()
            if tweet_found.id != blague.last_tweet_responded_id:
                print(
                    "Tweet trouvé pour cette recherche :  "
                    + blague.text_to_search
                    + " à "
                    + str(datetime.now() + hours_to_add)
                )
                has_this_blague_a_new_tweet_to_respond = True  # it breaks
            else:
                print(
                    "Tweet déjà répondu pour cette recherche : "
                    + blague.text_to_search
                    + " à "
                    + str(datetime.now() + hours_to_add)
                )

        try:

            if (
                datetime.now() + hours_to_add
            ).hour >= 8:  # Ici on évite les tweets soient envoyés la nuit : les tweets peuvent que être envoyés seulement après 8h
                blague.respond_to_a_tweet_and_retweet_the_answer(tweet_found)
                blague.last_tweet_responded_id = tweet_found.id
                print(
                    "Tweet envoyé, prochain dans : "
                    + str(random_time // 60)
                    + "min à "
                    + str(
                        (
                            datetime.now()
                            + timedelta(seconds=random_time)
                            + hours_to_add
                        ).strftime("%H:%M")
                    )
                )
            else:
                print(str(datetime.now() + hours_to_add))
                print(
                    "C'est la nuit, on envoie pas. Prochain essai dans "
                    + str(random_time // 60)
                    + "min à "
                    + str(
                        (
                            datetime.now()
                            + timedelta(seconds=random_time)
                            + hours_to_add
                        ).strftime("%H:%M")
                    )
                )

        except Exception as e:
            print(e)
            print(
                "ERROR avec la recherche :"
                + blague.text_to_search
                + str(datetime.now())
            )
            send_an_error_mail("Erreur avec le bot OSS. : " + str(e))

        time.sleep(random_time)


#############################################################################

main()
