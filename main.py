import asyncio
import requests
from fastapi import FastAPI, Request
from pymongo import MongoClient as mc
import pytz
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import parsedatetime as pdt


app = FastAPI()

product_id = "51f345da-e52c-4444-a900-427e6c05db55"
token = "e544d376-d7a6-4a7e-ae49-c991317cb016"
phone_id = 33008
header = {"x-maytapi-key": token}
url = f"https://api.maytapi.com/api/{product_id}/{phone_id}/sendMessage"

king = mc("mongodb+srv://remindme:nUg9F1xlK2LPXA6z@cluster0.zhoempa.mongodb.net/")


def schedule_work(date_time_str, timezone, task, number):
    tasks = king.remindme.Scheduled_Tasks
    if ("in" in date_time_str.lower()):
        if ("minutes" in date_time_str.lower()):
            minutes = int(date_time_str.split(" ")[1])
            scheduled_time = int(datetime.now().timestamp())+(minutes*60)
            if (tasks.find_one({"_id": scheduled_time}) == None):
                tasks.insert_one(
                    {"_id": scheduled_time, "tasks": [[task, number]]})
            else:
                arr = tasks.find_one({"_id": scheduled_time})["tasks"]
                newarr = arr.append([task, number])
                tasks.update_one({"_id": scheduled_time}, {
                                 "$set": {"tasks": newarr}})
            return f"You got it boss!💥\nI will remind you *{(datetime.fromtimestamp(scheduled_time, pytz.timezone(timezone))).strftime('%Y-%m-%d %H:%M:%S %Z')}* to *{task}*."

        if ("hours" in date_time_str.lower()):
            hours = int(date_time_str.split(" ")[1])
            scheduled_time = int(datetime.now().timestamp())+(hours*60*60)
            if (not tasks.find_one({"_id": scheduled_time}) == None):
                arr = tasks.find_one({"_id": scheduled_time})["tasks"]
                newarr = arr.append([task, number])
                tasks.update_one({"_id": scheduled_time}, {
                                 "$set": {"tasks": newarr}})
            else:
                tasks.insert_one(
                    {"_id": scheduled_time, "tasks": [[task, number]]})
            return f"You got it boss!💥\nI will remind you *{(datetime.fromtimestamp(scheduled_time, pytz.timezone(timezone))).strftime('%Y-%m-%d %H:%M:%S %Z')}* to *{task}*."

        if ("days" in date_time_str.lower()):
            days = int(date_time_str.split(" ")[1])
            scheduled_time = int(datetime.now().timestamp())+(days*24*60*60)
            if (not tasks.find_one({"_id": scheduled_time}) == None):
                arr = tasks.find_one({"_id": scheduled_time})["tasks"]
                newarr = arr.append([task, number])
                tasks.update_one({"_id": scheduled_time}, {
                                 "$set": {"tasks": newarr}})
            else:
                tasks.insert_one(
                    {"_id": scheduled_time, "tasks": [[task, number]]})
            return f"You got it boss!💥\nI will remind you *{(datetime.fromtimestamp(scheduled_time, pytz.timezone(timezone))).strftime('%Y-%m-%d %H:%M:%S %Z')}* to *{task}*."
        else:
            return "Wrong Input!! \ntry again or type *help* to see the guide"

    elif ("on" in date_time_str.lower()):
        prompt = date_time_str
        cal = pdt.Calendar()

        # Parse the input prompt into a datetime object
        parsed_time, parse_status = cal.parse(prompt)

        if parse_status == 0:
            return "Wrong Input!! \ntry again or type *help* to see the guide"

        if parsed_time:
            # Create a timezone object
            tz = pytz.timezone(timezone)

            # Convert the parsed datetime to a Unix timestamp
            localized_datetime = tz.localize(datetime(*parsed_time[:6]))
            unix_timestamp = int(localized_datetime.timestamp())
            if (not tasks.find_one({"_id": unix_timestamp}) == None):
                arr = tasks.find_one({"_id": unix_timestamp})["tasks"]
                newarr = arr.append([task, number])
                tasks.update_one({"_id": unix_timestamp}, {
                                 "$set": {"tasks": newarr}})
            else:
                tasks.insert_one(
                    {"_id": unix_timestamp, "tasks": [[task, number]]})
            return f"You got it boss!💥\nI will remind you *{(datetime.fromtimestamp(unix_timestamp, pytz.timezone(timezone))).strftime('%Y-%m-%d %H:%M:%S %Z')}* to *{task}*."
        else:
            return "Wrong Input!! \ntry again or type *help* to see the guide"

    elif ("at" in date_time_str.lower()):
        tz = pytz.timezone(timezone)

        try:
            time_str = prompt.split("at")[1].strip()
            time_obj = datetime.strptime(time_str, "%I:%M%p")
        except ValueError:
            return ("Wrong Input!! \ntry again or type *help* to see the guide")

        current_date = datetime.now(tz).date()

        localized_datetime = tz.localize(datetime(
            current_date.year, current_date.month, current_date.day, time_obj.hour, time_obj.minute))

        unix_timestamp = int(localized_datetime.timestamp())
        if (not tasks.find_one({"_id": unix_timestamp}) == None):
            arr = tasks.find_one({"_id": unix_timestamp})["tasks"]
            newarr = arr.append([task, number])
            tasks.update_one({"_id": unix_timestamp}, {
                             "$set": {"tasks": newarr}})
        else:
            tasks.insert_one(
                {"_id": unix_timestamp, "tasks": [[task, number]]})
        return f"You got it boss!💥\nI will remind you *{(datetime.fromtimestamp(unix_timestamp, pytz.timezone(timezone))).strftime('%Y-%m-%d %H:%M:%S %Z')}* to *{task}*."

    else:
        date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        unix_timestamps = {}
        tz = pytz.timezone(timezone)
        localized_datetime = tz.localize(date_time_obj)
        unix_timestamp = int(localized_datetime.timestamp())
        unix_timestamps[timezone] = unix_timestamp

        print(f"time now : ", int(datetime.now().timestamp()))
        try:
            if (unix_timestamp > int(datetime.now().timestamp())):
                if (not tasks.find_one({"_id": unix_timestamp}) == None):
                    arr = tasks.find_one({"_id": unix_timestamp})["tasks"]
                    newarr = arr.append([task, number])
                    tasks.update_one({"_id": unix_timestamp}, {
                                     "$set": {"tasks": newarr}})
                else:
                    tasks.insert_one(
                        {"_id": unix_timestamp, "tasks": [[task, number]]})
                return f"You got it boss!💥\nI will remind you *{(datetime.fromtimestamp(unix_timestamp, pytz.timezone(timezone))).strftime('%Y-%m-%d %H:%M:%S %Z')}* to *{task}*."
            else:
                return ("Wrong Input!! \ntry again or type *help* to see the guide")
        except:
            return ("Wrong Input!! \ntry again or type *help* to see the guide")


def get_timezone(city, country):
    try:
        geolocator = Nominatim(user_agent="timezone_finder")
        location = geolocator.geocode(f"{city}, {country}", exactly_one=True)

        if location:
            latitude, longitude = location.latitude, location.longitude
            tf = TimezoneFinder()
            time_zone_str = tf.timezone_at(lng=longitude, lat=latitude)

            if time_zone_str:
                time_zone = pytz.timezone(time_zone_str)
                return [time_zone, True]
            else:
                return ["Time zone not found for the given city and country.", False]
        else:
            return ["Location not found for the given city and country.", False]
    except (pytz.UnknownTimeZoneError, AttributeError):
        return ["Invalid city or country", False]


async def sendmessage(msg, number):
    mobilezone = king.remindme.mobilezone
    sctasks = king.remindme.Scheduled_Tasks
    greet = {
        "to_number": number,
        "type": "text",
        "message": '''Hi 🙋‍♂️\nwelcome to our reminder bot !!✨✨

Send me a message with your *task* 📝: e.g. _Buy milk_
I will ask you for the *date* 📅 and *time* ⏰: e.g. _at 3pm_

I will then remind 🔔 you at *3pm* to *Buy milk*.

*Keywords* to message:
⌚ *set*: to set your timezone
📋 *menu*: see keywords to use
ℹ *help*: see sample times to set
📺 *tutorial*: see the tutorial on video
🪙 *balance*: check your balance


_By sending us a message, you agree to opt-in to RemindMe Bot_''',
        "skip_filter": True
    }
    help = {
        "to_number": number,
        "type": "text",
        "message": "Type *help* to get details about its 🗣️commands and 🗒️guide on how to use this bot",
        "skip_filter": True
    }
    info = {
        "to_number": number,
        "type": "text",
        "message": '''⌚ *Set* your timezone once and only change if your timezone changes or daylight savings change your time.

⚠To set a reminder, you first message the bot with the 'content' of the reminder - the action/verb.

🤖Try to be specific - remember the bot is learning as you use it!

ℹTips:
- Separate your message into a *Task* itself (an action)
- Then respond with the time
- For example, send a message saying - Wash my cloths
- The bot will respond asking for when to remind you
- You respond with a time - in 30 minutes

📋Sample answers to the tasks:
- call mom
- watch football
- do assignment

⚠After sending a message (any message) that is *not* a one-word keyword, you will be asked: 📅⏰: What date and time would you like me to remind you about *task* ?

🤖Try to be specific - remember the bot is learning as you use it!

⚠Avoid unspecific Date and Times:
- if you don't add am/pm then it is assumed to be 24 hours format
- 2 months: when in 2 months? do you mean *in* 2 months?
- words that have ranges: e.g. later, morning, night

⚠Avoid words that denote number in your Time:
e.g. two, three, ten

There are 2 components to the answer:
📅Date: if there is no mention it assumes *today*
e.g. today, Monday, next Monday, 31 July, 31 July 2025

⏰Time: if there is no mention then it assumes mid-day (12pm/12:00)
e.g. 8am, 15:00 

↔Combining them both:
e.g. on 30 July 2025 at 11:59

📋Sample answers - note the words in *bold*:
- *in* a minute/hour/day
- *at* 3pm/15:30
- *on* Monday/Tuesday at 09:00/9am''',
        "skip_filter": True
    }

    ask_tz = {
        "to_number": number,
        "type": "text",
        "message": "Before you set a reminder, I need to know what time zone you are in.\n🌍 To find your time zone, please reply with your *City, Country* e.g., Cape Town, South Africa",
        "skip_filter": True
    }

    if "hi" in msg.lower() or "hello" in msg.lower() or "hlo" in msg.lower():
        result = requests.post(url=url, headers=header, json=greet)
        if (result.status_code == 200):
            print("Greeting msg sent to ", number)
            result = requests.post(url=url, headers=header, json=help)
            if (result.status_code == 200):
                print("help command message sent to ", number)
                field = {"_id": number, "timezone": None, "credit":5}
                mobilezone.insert_one(field)
                mobilezone = king.remindme.mobilezone
                if (mobilezone.find_one({"_id": number})["timezone"] == None or msg.lower() == "set"):
                    print(mobilezone.find_one({"_id": number})["timezone"])
                    mobilezone.update_one(
                        {"_id": number}, {"$set": {"timezone": None}})
                    result = requests.post(
                        url=url, headers=header, json=ask_tz)
                    if (result.status_code == 200):
                        print("Asked for timezone to ", number)
                        mobilezone.update_one(
                            {"_id": number}, {"$set": {"timezone": "asked"}})
                return "done"

    if ((mobilezone.find_one({"_id": number}))["timezone"] == "asked"):
        cc = msg.split(",")
        found_timezone = get_timezone(cc[0], cc[1])
        if (found_timezone[1] == True):
            mobilezone.update_one(
                {"_id": number}, {"$set": {"timezone": str(found_timezone[0])}})
            response = {
                "to_number": number,
                "type": "text",
                "message": f"Timezone set to {found_timezone[0]}",
                "skip_filter": True
            }
            result = requests.post(url=url, headers=header, json=response)
            print("Timezone set for ", number)
        else:
            response = {
                "to_number": number,
                "type": "text",
                "message": found_timezone[0],
                "skip_filter": True
            }
            result = requests.post(url=url, headers=header, json=response)
        return "done"

    if (mobilezone.find_one({"_id": number})["timezone"] == None or msg.lower() == "set"):
        print(mobilezone.find_one({"_id": number})["timezone"])
        mobilezone.update_one({"_id": number}, {"$set": {"timezone": None}})
        result = requests.post(url=url, headers=header, json=ask_tz)
        if (result.status_code == 200):
            print("Asked for timezone to ", number)
            mobilezone.update_one(
                {"_id": number}, {"$set": {"timezone": "asked"}})
            return "done"

    if msg.lower() == "help":
        result = requests.post(url=url, headers=header, json=info)
        if (result.status_code == 200):
            print("Info msg sent to ", number)
        return "done"
    if msg.lower() == "menu":
        menu={
                "to_number": number,
                "type": "text",
                "message": '''⚠Message the key terms in *bold* if you want to perform the action:

⌚ *set*: change to your time (Default: GMT+2)

ℹ *help*:  get sample times that you may use to set reminders

📺 *tutorial*: see tutorial video

🪙 *balance*: get your Subscription Plan and Reminder Tokens balance

_(Note: Once you get a reminder confirmation there is no going back)_''',
                "skip_filter": True
            }
        result = requests.post(url=url, headers=header, json=menu)
        if (result.status_code == 200):
            print("Menu msg sent to ", number)
        return "done"
    
    if msg.lower() == "balance":
        balanceinfo={
                "to_number": number,
                "type": "text",
                "message": "Your Balance left is : "+str(mobilezone.find_one({"_id": number})["credit"])+" \n To get more credit contact admin",
                "skip_filter": True
            }
        result = requests.post(url=url, headers=header, json=balanceinfo)
        if (result.status_code == 200):
            print("Balance Info msg sent to ", number)
        return "done"
    if msg.lower() == "tutorial":
        balanceinfo={
                "to_number": number,
                "type": "text",
                "message": "To see the tutorial video follow the below link : \n ",
                "skip_filter": True
            }
        result = requests.post(url=url, headers=header, json=balanceinfo)
        if (result.status_code == 200):
            print("Balance Info msg sent to ", number)
        return "done"

    sctasks = king.remindme.Scheduled_Tasks
    if (not sctasks.find_one({"_id": number}) == None):
        if(mobilezone.find_one({"_id":number})["credit"]>=0):
            resp = schedule_work(msg, mobilezone.find_one({"_id": number})[
                                "timezone"], sctasks.find_one({"_id": number})["tasks"], number)
            scheduled_resp = {
                "to_number": number,
                "type": "text",
                "message": resp,
                "skip_filter": True
            }
            result = requests.post(url=url, headers=header, json=scheduled_resp)
            if (result.status_code == 200):
                print("task scheduled")
                sctasks.delete_one({"_id": number})
                mobilezone.update_one({"_id":number},{"$inc":{"_credit":-1}})
        else:
            scheduled_resp = {
                "to_number": number,
                "type": "text",
                "message": "Your Balance is no more left.\nContact the admin to get Balance.\nYou can send *balance* to check",
                "skip_filter": True
            }
            result = requests.post(url=url, headers=header, json=scheduled_resp)
            if (result.status_code == 200):
                print("task scheduled")
                sctasks.delete_one({"_id": number})
    else:
        task = {
            "to_number": number,
            "type": "text",
            "message": f"📅⏰: What date and time should I remind you about *{msg}*?",
            "skip_filter": True
        }

        result = requests.post(url=url, headers=header, json=task)
        if (result.status_code == 200):
            print("Asking for time to schedule")
            field = {"_id": number, "tasks": msg}
            sctasks.insert_one(field)


async def check_tasks():
    while True:
        tasks = king.remindme.Scheduled_Tasks
        cursor = tasks.find({}, {"_id": 1})
        timestamps = [document["_id"] for document in cursor]
        current_time = int(datetime.now().timestamp())
        for j in timestamps:
            if current_time >= j:
                sending_tasks = tasks.find_one({"_id": j})["tasks"]
                for i in sending_tasks:
                    sndmsg = {
                        "to_number": i[1],
                        "type": "text",
                        "message": f"🔔: *{i[0]}*",
                        "skip_filter": True
                    }
                    result = requests.post(
                        url=url, headers=header, json=sndmsg)
                    if (result.status_code == 200):
                        print("Alert sent for task to ", i[1])
            tasks.delete_one({"_id": j})

        await asyncio.sleep(20)


@app.post("/")
async def webhock(request: Request):
    data = await request.json()
    try:
        await sendmessage(data["message"]["text"], data["user"]["phone"])
    except:
        pass

task_scheduler_loop = asyncio.get_event_loop()
task_scheduler_loop.create_task(check_tasks())
