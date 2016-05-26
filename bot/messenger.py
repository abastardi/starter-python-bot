import logging
import random
import sys


logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: {} to channel: {}'.format(msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message("{}".format(msg.encode('ascii', 'ignore')))

    def msg_restaurant_query(self, channel_id, user_id):
        intro = '{}\n{}'.format( 
            "I am your friendly chatbot here to help you find a restaurant.",
            "What kind of food would you like to eat?")
        # I'm here to help you find a restaurant nearby. When you give me a zip code, I'll tell you about a restaurant that's close to you. What zip code would you like to search?"
        self.send_message(channel_id, intro)
        self.clients.send_user_long_typing_pause(channel_id)
        zip_code_request = '{}\n{}'.format( 
            "Sounds yummy!",
            "What is your zip code?")
        # I'm here to help you find a restaurant nearby. When you give me a zip code, I'll tell you about a restaurant that's close to you. What zip code would you like to search?"
        self.send_message(channel_id, zip_code_request)
        self.clients.send_user_long_typing_pause(channel_id)
        restaurant_info = '{}\n>>>{}\n{}\n{}'.format( 
            "How about *Michelle's Hawaiian Grill*, located at:",
            "1538 Kapiolani Blvd",
            "Suite 107",
            "Honolulu, HI 96814")
        self.send_message(channel_id, restaurant_info)
        #attachment = {
        #    "image_url": "../resources/poke_nachos.jpg",
        #}
        #self.clients.web.chat.post_message(channel_id, attachments=[attachment], as_user='true')
        self.clients.send_user_typing_pause(channel_id)
        #feedback_request = "How do you like my service?"
        #asks for feedback
        #self.send_message(channel_id, feedback_request)
        send_off = "Your task inside Slack is now finished - Please return to the survey to complete your HIT."
        #asks for feedback
        self.send_message(channel_id, send_off)

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = '{}\n{}\n{}'.format(
            "I'm your friendly Slack bot written in Python.  I'll *_respond_* to the following commands:",
            "> `hi <@" + bot_uid + ">` - I'll introduce myself.",
            "> `<@" + bot_uid + "> restaurant` - I'll help you find a restaurant :knife_fork_plate:")
            #"> `<@" + bot_uid + "> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:",
            #"> `<@" + bot_uid + "> attachment` - I'll demo a post with an attachment using the Web API. :paperclip:")
        self.send_message(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        greetings = "Hi "
        give_name = " my name is Ollie." 
        intro = "I'm here to help you find a restaurant nearby"
        txt = '{}<@{}>{}\n{}'.format(greetings, user_id, give_name, intro)
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        question = "Why did the python cross the road?"
        self.send_message(channel_id, question)
        self.clients.send_user_typing_pause(channel_id)
        answer = "To eat the chicken on the other side! :laughing:"
        self.send_message(channel_id, answer)


    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')
