import os
import sys
#SCRIPT TO CREATE PROFILES, AFTER CREATING USERS
#FOR CREATING USERS UNCOMMENT THE CODE COMMENTRD AND VICEVERSA
os.environ['DJANGO_SETTINGS_MODULE'] = 'pichrr.settings'
import django
from django.contrib.auth.models import User
from user_profile.models import UserProfile


if __name__ == '__main__':
    django.setup()

usernames = ['theHulk', 'tonyStark', 'capt_America', 'Thor', 'blackWidow', 'hawkEye', 'loki', 'deadPool']
first_names = ['Bruce', 'Tony', 'Steve', 'Thor', 'Natasha', 'Clint', 'Loki', 'Wade' ]
last_names = ['Banner', 'Stark', 'Rogers', '', 'Romanoff', 'Barton', '', '']
gender = ['M', 'M', 'M', 'M', 'F', 'M', 'M', 'M']
intros = [  "I worked as a scientist on the gamma bomb project when I heroically saved a young man from exposure to a nuclear blast. Unfortunately, the exposure to gamma radiation changed Banner's cell structure, causing me to transform into a raging green monster (known as the Hulk) when I became angry.",
            "During a visit to the Persian Gulf to show off the latest Stark Industries weaponry, I was captured by the enemy and forced to build a new super weapon. Instead (with the assistance of renowned physicist and fellow prisoner Ho Yinsen) I crafted the first version of the now-famous powered battle armor",
            "In the early days of World War II, a covert military experiment turned me into America's first super-soldier: Captain America. During the war, I served as a symbol of freedom and America's most effective special operative. In the closing days of the war, I disappeared in an explosion over the North Atlantic and was presumed dead.",
            "I am the Norse god of thunder and the son of Odin All-Father, ruler of Asgard. I wield the mystic hammer Mjolnir, which allows me to fly and fire bolts of lightning. I was a founding member of the Avengers and frequently battles as one of their number",
            "I was a young Soviet citizen when my government chose to train me in espionage. During my time in the infamous Red Room Academy, I became the master spy known as the Black Widow.",
            "Inspired by the exploits of Iron Man, circus archer myself decided to put on a costume and fight crime as the super-hero Hawkeye. At first I was mistaken as a criminal, but i eventually gained the trust of the Avengers and has served on that team with distinction many times.",
            "I am the Norse god of mischief and evil and the adopted son of Odin All-Father, the ruler of Asgard. I am crafty, clever, and resourceful, using sorcery to achieve my intricate goals. I resent the glory and acclaim given to my adoptive brother.",
            "i was a test subject in the same Weapon X program that had previously given Wolverine his adamantium claws and skeleton, I received a healing factor that prevented my cancer from killing me"
          ]

for i in range(len(usernames)):
    user = User.objects.get(username=usernames[i])
    profile = UserProfile.objects.get(user=user)
    profile.first_name = first_names[i]
    profile.last_name = last_names[i]
    profile.intro = intros[i]
    profile.gender = gender[i]
    profile.save()