#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.

This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import constants as keys

import time
import datetime
import requests
import database

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def stock_price(ticket_tag):
    URL = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticket}.SA?modules=price".format(ticket=ticket_tag)
    print(URL)
    headers = {'User-Agent': 'Python'}
    response = requests.get(URL, headers=headers)
    result_json = response.json()
    price = result_json['quoteSummary']['result'][0]['price']['regularMarketPrice']['raw']
    # timestamp = result_json['quoteSummary']['result'][0]['price']['regularMarketTime']
    # timehuman = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(timestamp))
    # print(result_json)
    return price

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /set <seconds> <stock_code> to set a timer to receive the stock price')


def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    '''wday = datetime.datetime.today().weekday()
    hour = datetime.datetime.today().hour
    if ((wday < 5) & (hour > 12) & (hour < 20)):'''
    job = context.job
    print(job.context[0], job.context[1])
    message = "The price of {stock} is {price}".format(stock=job.context[1], price=stock_price(job.context[1]))
    context.bot.send_message(job.context[0], text=message )


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""    
    chat_id = update.message.chat_id    
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return
        stock_tag = context.args[1]

        print(stock_tag)
        #job_removed = remove_job_if_exists(str(chat_id), context)
        #context.job_queue.run_once(alarm, due, context=[chat_id, stock_tag], name=str(chat_id))
        context.job_queue.run_repeating(alarm, due, context=[chat_id, stock_tag], name=str(chat_id)+str(stock_tag))


        text = 'Timer successfully set!'
        #if job_removed:
        #    text += ' Old one was removed.'
        #update.message.reply_text(text)

        ''' Store the alarm in the database '''
        alarmentry = {
            'chat_id': str(chat_id),
            'stock': str(stock_tag),
            'interval': str(due)    
        }
        result = database.insert_alarm(alarmentry)
        if (result):
            update.message.reply_text('Success! Your alarm is registered!')
        else:
            logger.error("Erro inserting the alarm in the database.")

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds> <stock>')


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    '''TODO: here we need to connec in the database and remove all alarms from thi chat_id'''
    try:
        chat_id = update.message.chat_id
        stock_tag = context.args[0]
        alarms = database.get_alarms(chat_id, stock_tag)
        number_of_active_alarms = alarms.count()
        if number_of_active_alarms > 0:
            name = str(chat_id) + str(stock_tag)
            job_removed = remove_job_if_exists(name, context)
            result = database.delete_alarms(chat_id, stock_tag)
            if job_removed and result.deleted_count == number_of_active_alarms:
                update.message.reply_text('I successfully cancelled ' + str(number_of_active_alarms) + ' alarms!')
            else:
                update.message.reply_text('Problem cancelling alarms. Try again!')
        else:
            update.message.reply_text("I did not find any alarms with the stock " + stock_tag + ".")
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /unset <stock>')

def list(update: Update, context: CallbackContext) -> None:
    """List all active alarms for the user"""
    try:
        chat_id = update.message.chat_id
        alarms = database.get_alarms(chat_id)
        number_of_active_alarms = alarms.count()
        if (number_of_active_alarms > 0):
            message = "Here is the list of alarms you have:\n\nSTOCK\tINTERVAL\n"
            for dbalarm in alarms:
                message += dbalarm["stock"] + "\t"
                message += dbalarm["interval"] + "\n"
            print(message)
            update.message.reply_text(message)
        else:
            update.message.reply_text("There is no alarms registered for you.")
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /list')

def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(keys.API_KEY)

    # Connect to DB to recriate all alarms
    alarms = database.get_all_alarms()
    for dbalarm in alarms:
        chat_id = int(dbalarm["chat_id"])
        stock = dbalarm["stock"]
        interval = int(dbalarm["interval"])
        updater.job_queue.run_repeating(alarm, interval, context=[chat_id, stock], name=str(chat_id))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("set", set_timer))
    dispatcher.add_handler(CommandHandler("unset", unset))
    dispatcher.add_handler(CommandHandler("list", list))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()