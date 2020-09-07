import time
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import ReplyKeyboardMarkup

class GoldenArches(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(GoldenArches, self).__init__(*args, **kwargs)
        self.indicator = 'Q1'
        self.response = {}

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        score = 0
        #Prompt user the questions
        if self.indicator == 'Q1':
            score = 0
            mark_up = ReplyKeyboardMarkup(keyboard=[['A: Less than 3 years'], ['B: 3–5 years'], ['C: 6–10 years'], ['D: 11 years or more']],
                                          one_time_keyboard=True)
            bot.sendMessage(chat_id, text='Thank you for taking the test! There are 7 questions in total. \n\nQ1. I plan to begin withdrawing money from my investments in: ?', reply_markup=mark_up)
            self.indicator = 'Q2'

        elif self.indicator == 'Q2':
            #handle the previous request, calculate and save the Time_Horizon_Score
            score = 0
            if msg['text'][0] == 'A':
                score = 1
            elif msg['text'][0] == 'B':
                score = 3
            elif msg['text'][0] == 'C':
                score = 7
            elif msg['text'][0] == 'D':
                score = 10
            self.response['Time_Horizon_Score'] = score
            mark_up = ReplyKeyboardMarkup(keyboard=[['A: Less than 2 years'], ['B: 2–5 years'],['C: 6–10 years'],['D: 11 years or more']],
                                          one_time_keyboard=True)
            bot.sendMessage(chat_id, 'Q2. Once I begin withdrawing funds from my investments, I plan to spend all of the funds in:', reply_markup=mark_up)
            self.indicator = 'Q3'

        elif self.indicator == 'Q3':
            if msg['text'][0] == 'A':
                score = 0
            elif msg['text'][0] == 'B':
                score = 1
            elif msg['text'][0] == 'C':
                score = 4
            elif msg['text'][0] == 'D':
                score = 8
            self.response['Time_Horizon_Score'] += score
            mark_up = ReplyKeyboardMarkup(keyboard=[['A: None'], ['B: Limited'],['C: Good'],['D: Extensive']],
                                          one_time_keyboard=True)
            bot.sendMessage(chat_id, text='Q3. I would describe my knowledge of investments as:', reply_markup=mark_up)
            self.indicator = 'Q4'

        elif self.indicator == 'Q4':
            if msg['text'][0] == 'A':
                score = 1
            elif msg['text'][0] == 'B':
                score = 3
            elif msg['text'][0] == 'C':
                score = 7
            elif msg['text'][0] == 'D':
                score = 10
            self.response['Risk_Tolerance_Score'] = score
            mark_up = ReplyKeyboardMarkup(keyboard=[['A: Most concerned about my investment losing value'], ['B: Equally concerned about my investment losing or gaining value '],['C: Most concerned about myinvestment gaining value']],
                                          one_time_keyboard=True)
            bot.sendMessage(chat_id, text='Q4. When I invest my money, I am:', reply_markup=mark_up)
            self.indicator = 'Q5'

        elif self.indicator == 'Q5':
            if msg['text'][0] == 'A':
                score = 0
            elif msg['text'][0] == 'B':
                score = 4
            elif msg['text'][0] == 'C':
                score = 8
            self.response['Risk_Tolerance_Score'] += score
            mark_up = ReplyKeyboardMarkup(keyboard=[['A: Bonds and/or bond funds'], ['B: Stocks and/or stock funds'],['C: International securities and/or international funds ']],
                                          one_time_keyboard=True)
            bot.sendMessage(chat_id, text='Q5. Select the investments you currently own :', reply_markup=mark_up)
            self.indicator = 'Q6'

        elif self.indicator == 'Q6':
            if msg['text'][0] == 'A':
                score = 3
            elif msg['text'][0] == 'B':
                score = 6
            elif msg['text'][0] == 'C':
                score = 8
            self.response['Risk_Tolerance_Score'] += score
            mark_up = ReplyKeyboardMarkup(keyboard=[['A: Sell all of my shares'], ['B: Sell some of my shares'],['C: Do nothing'],['D: Buy more shares']],
                                          one_time_keyboard=True)
            bot.sendMessage(chat_id, text='Q6. Imagine that in the past three months, the overall stock market lost 25% of its value. An individual stock investment you own also lost 25% of its value. What would you do?', reply_markup=mark_up)
            self.indicator = 'Q7'

        elif self.indicator == 'Q7':
            if msg['text'][0] == 'A':
                score = 0
            elif msg['text'][0] == 'B':
                score = 2
            elif msg['text'][0] == 'C':
                score = 5
            elif msg['text'][0] == 'D':
                score = 8
            self.response['Risk_Tolerance_Score'] += score
            mark_up = ReplyKeyboardMarkup(keyboard=[['A: Average annual return 7.2%, Best-case 16.3%, Worst-case -5.6%'], ['B: Average annual return 9.0%, Best-case 25.0%, Worst-case -12.1%'],['C: Average annual return 10.4%, Best-case 33.6%, Worst-case -18.2%'],['D: Average annual return 11.7%, Best-case 42.8%, Worst-case -24.0%'],['E: Average annual return 12.5%, Best-case 50.0%, Worst-case -28.2%']],
                                          one_time_keyboard=True)
            bot.sendMessage(chat_id, text='Q7. We’ve outlined the most likely best-case and worst-case annual returns of five hypothetical investment plans. Which range of possible outcomes is most acceptable to you?', reply_markup=mark_up)
            self.indicator = 'Q8'

        elif self.indicator == 'Q8':
            if msg['text'][0] == 'A':
                score = 0
            elif msg['text'][0] == 'B':
                score = 3
            elif msg['text'][0] == 'C':
                score = 6
            elif msg['text'][0] == 'D':
                score = 8
            elif msg['text'][0] == 'E':
                score = 10
            self.response['Risk_Tolerance_Score'] += score

            #Currently we have Time_Horizon_Score and Risk_Tolerance_Score
            #We need to categorise user's risk tolerance level according to these two score and risk tolerance matrix 

            #Extremely Low risk tolerance
            if self.response['Time_Horizon_Score']<3:
                self.response['Risk_Tolerance_Level'] = "Extremely Low. We do not suggest you to invest in equities market. Maybe cash investment could be a better option"
                self.response['Final_Score'] = "Not applicable."
            #Risk_Tolerance_Level: Conservative
            elif (self.response['Time_Horizon_Score']<=4 and self.response['Risk_Tolerance_Score']<=18) or \
                (self.response['Time_Horizon_Score']==5 and self.response['Risk_Tolerance_Score']<=15) or \
                    (self.response['Time_Horizon_Score']<=9 and self.response['Risk_Tolerance_Score']<=12) or \
                        (self.response['Time_Horizon_Score']<=12 and self.response['Risk_Tolerance_Score']<=11) or \
                            (self.response['Time_Horizon_Score']<=18 and self.response['Risk_Tolerance_Score']<=10):
                            self.response['Risk_Tolerance_Level'] = "Conservative"
                            self.response['Final_Score'] = "5"
            #Risk_Tolerance_Level: Moderately Conservative
            elif (self.response['Time_Horizon_Score']<=4 and self.response['Risk_Tolerance_Score']<=31) or \
                (self.response['Time_Horizon_Score']==5 and self.response['Risk_Tolerance_Score']<=24) or \
                    (self.response['Time_Horizon_Score']<=9 and self.response['Risk_Tolerance_Score']<=20) or \
                        (self.response['Time_Horizon_Score']<=12 and self.response['Risk_Tolerance_Score']<=18) or \
                            (self.response['Time_Horizon_Score']<=18 and self.response['Risk_Tolerance_Score']<=17):
                            self.response['Risk_Tolerance_Level'] = "Moderately Conservative"
                            self.response['Final_Score'] = "4"
            #Risk_Tolerance_Level: Moderate
            elif (self.response['Time_Horizon_Score']<=4 and self.response['Risk_Tolerance_Score']<=40) or \
                (self.response['Time_Horizon_Score']==5 and self.response['Risk_Tolerance_Score']<=35) or \
                    (self.response['Time_Horizon_Score']<=9 and self.response['Risk_Tolerance_Score']<=28) or \
                        (self.response['Time_Horizon_Score']<=12 and self.response['Risk_Tolerance_Score']<=26) or \
                            (self.response['Time_Horizon_Score']<=18 and self.response['Risk_Tolerance_Score']<=24):
                            self.response['Risk_Tolerance_Level'] = "Moderate"
                            self.response['Final_Score'] = "3"
            #Risk_Tolerance_Level: Moderately Aggressive
            elif (self.response['Time_Horizon_Score']==5 and self.response['Risk_Tolerance_Score']<=40) or \
                (self.response['Time_Horizon_Score']<=9 and self.response['Risk_Tolerance_Score']<=37) or \
                    (self.response['Time_Horizon_Score']<=12 and self.response['Risk_Tolerance_Score']<=34) or \
                        (self.response['Time_Horizon_Score']<=18 and self.response['Risk_Tolerance_Score']<=31):
                            self.response['Risk_Tolerance_Level'] = "Moderately Aggressive"
                            self.response['Final_Score'] = "2"
            #Risk_Tolerance_Level: Aggressive
            else:
                self.response['Risk_Tolerance_Level'] = "Aggressive"
                self.response['Final_Score'] = "1"

            #return the final result to user
            bot.sendMessage(chat_id, 'Thank you for taking the test.\nYour risk tolerance level is : '+str(self.response['Risk_Tolerance_Level'])+' !\nYour final score is : '+str(self.response['Final_Score'])+' !')
            #self.indicator = "Q1"

TOKEN = '1279765543:AAHPN_5QmYRW4qVCV1N0Uf-xf9J2KOOFAVA'

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, GoldenArches, timeout=60),
])
bot.setWebhook()
MessageLoop(bot).run_as_thread()

while 1:
    time.sleep(60)