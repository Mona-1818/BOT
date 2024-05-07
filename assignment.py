#libraries
import requests
import os
import time
import json
from typing import Final
from telegram import Update
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

#intial values
os.environ['PATH'] += //chrome driver path
TOKEN: Final = //token
BOT_USERNAME: Final = //bot name
EMAIL: Final =  //email
PASSWORD: Final = //password
COOKIES: Final = //cookie
try:
    driver = webdriver.Chrome() 
    driver.get('https://www.udio.com/')
    button = driver.find_element(by='xpath', value="/html/body/section/div[1]/div[2]/div[1]/div/div[2]/button[1]")
    button.click()
    time.sleep(5)
    button2 = driver.find_element(by='xpath', value='/html/body/div[7]/div[2]/div/div/div[4]/div/div/button[1]')
    button2.click()
    input_field = driver.find_element(by='xpath', value="/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input")
    input_field.send_keys(EMAIL)
    input_field.send_keys(Keys.ENTER)
    time.sleep(5)
    input_field1 = driver.find_element(by='xpath', value="/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")
    input_field1.send_keys(PASSWORD)
    input_field1.send_keys(Keys.ENTER)
    time.sleep(5)
except Exception as e:
    driver.quit()
    print(f"Unable to Login Try Again!!!")
  
#to start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome, \n I am your assintant Bot Vaishini\n Let's Dive in!!!")
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    """
    /start -> Welcome to the Vashini Bot
    /help -> All the commands 
    /login -> Details of Users
    /liked -> All the Liked Song By User
    /id <pass:id> -> Give Id to extracrt song details
    /trending -> top 5 Trending tracks
    /AutoCreate -> To create Song automatically with prompt
    /created -> All Song Created by User
    /logout -> to Logout
    """
    )
    
async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://www.udio.com/api/users/current"
        payload = ""
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "cookie": COOKIES,
            "priority": "u=1, i",
            "referer": "https://www.udio.com/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        response = requests.request("GET", url, data=payload, headers=headers)
        json_data = response.text
        data = json.loads(json_data)
        user = data.get('user')
        if user is None:
            await update.message.reply_text("Error: User data is missing in the response.")
            return
        user_id = user.get('id')
        full_name = user['user_metadata'].get('full_name', 'Not Available')
        email = user.get('email', 'Not Available')
        google_id = user['identities'][0].get('provider_id') if user.get('identities') else 'Not Available'
        await update.message.reply_text(
            f"""
            user_id = {user_id}
            full_name = {full_name}
            email = {email}
            google_id = {google_id}
            """
        )
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
        
async def liked_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://www.udio.com/api/songs/favorites"
        querystring = {"searchTerm":"","pageParam":"0","pageSize":"40"}
        payload = ""
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "cookie": COOKIES,
            "priority": "u=1, i",
            "referer": "https://www.udio.com/liked",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        json_data = response.text
        data = json.loads(json_data)
        text = ""
        for entry in data["data"]:
            text += f"""Id: {entry['id']}, title = {entry['title']}, artist = {entry['artist']}, created_at = {entry['created_at']} \n\n"""
        await update.message.reply_text(text)
    except KeyError as e:
        await update.message.reply_text(f"Error: {e} is missing in the response.")
    
async def trending_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://www.udio.com/api/songs/search"
        payload = {
            "searchQuery": {
                "sort": "cache_trending_score",
                "searchTerm": ""
            },
            "pageParam": 0,
            "pageSize": 5
        }
        headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "cookie": COOKIES,
        "origin": "https://www.udio.com",
        "priority": "u=1, i",
        "referer": "https://www.udio.com/",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
        response = requests.request("POST", url, json=payload, headers=headers)
        json_data = response.text
        data = json.loads(json_data)
        text = ""
        for song in data["data"]:
            text += f"""song_id = {song["id"]}, title = {song["title"]}, artist = {song["artist"]},likes = {song["likes"]},plays = {song["plays"]}, created_at = {song["created_at"]} \n"""
        await update.message.reply_text(text)
    except KeyError as e:
        await update.message.reply_text(f"Error: {e} is missing in the response.")
        
async def Id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = ' '.join(context.args)
    url = "https://www.udio.com/api/songs"
    querystring = {"songIds":id}
    payload = ""
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cookie": COOKIES,
        "priority": "u=1, i",
        "referer": "https://www.udio.com/search",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    json_data = response.text
    data = json.loads(json_data)
    first_song = data['songs'][0]
    await update.message.reply_text(
        f"""
        artist = {first_song['artist']}\ntitle = {first_song['title']}\ncreated_at = {first_song['created_at']}\nlyrics = {first_song['lyrics']}\nduration = {first_song['duration']}\n
        """
    )

async def created_Song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://www.udio.com/api/songs/me"
    querystring = {"likedOnly":"false","publishedOnly":"false","searchTerm":"","pageParam":"0","pageSize":"20"}
    payload = ""
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cookie": COOKIES,
        "priority": "u=1, i",
        "referer": "https://www.udio.com/my-creations",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    json_data = response.text
    data = json.loads(json_data)
    text = ""
    for i in range(len(data["data"])):
        song = data["data"][i]
        text += f"""song_id = {song["id"]}, title = {song["title"]}, artist = {song["artist"]}, likes = {song["likes"]}, plays = {song["plays"]}, created_at = {song["created_at"]}"""
    await update.message.reply_text(text)

async def create_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    url = "https://www.udio.com/api/generate-proxy"
    payload = {
        "prompt": prompt,
        "samplerOptions": {
            "seed": -1,
            "bypass_prompt_optimization": False
        },
        "captchaToken": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.hadwYXNza2V5xQVOxb8IBdfLJZoFBPAxYWrAOYBqng4KET1a_1hy42G5aLHtC4_InvUxE4svro1MoVzEt_TKT5NJjbyBnUnBntZSEUW9i_GwXrYfPbY0jKFa4D_XSFqR4gnXmfTIFXf6cUWrSkFmoDFBEdhDsFiL10A7XkPoTy-tNLYt0XMHnL3g-HojS_eBWSgpRk-0_OfQLbMzFgNlJfDmqUS5GO-3VYWdTScqsTiw6sIfY4uq-42RnRWmU-504ln1SHVBmSfr_FB1Wc0XTEEQo3v-RT7eHCeY_nUKJt7WZp1PbiL-GohHMqZWagkov_P5Rds5TriBoKs68ppkpfJpkf9kKpdwJS_gqJxZWe2C-Oa8g6_tmeCHuNhkYV_KWojZ-WD9win8aTZLLopaDbjQPOeYLNWKi6e0x4kQ3vwxEH6mv2urKeFf_W11ffDxhEae_Uef_o2anKPMcgjDzdOz9BVr4os08fxn0sA9fUgAULw0jrbCyVBDmazxQlOKwbJg0lD850m6DSfFSUs6DgfkhtKv75-WyqdDwNPUmvTyVJRLHg4x1MCA1_3okxCeQOI2Sa04jnnSrOJZ6tjQNCzwm06VjQ3Wnywlz5vuObvNJsWYdAW_546hivQgjU9mYP0GE7Tp8gezqhuNdRMqD37RYisFZ9h7N9Oa1jKaIhimc7-J15i6ZH88zANQl9Ey0-Iy8rhR4vNfYHbmpYqPZkEhSE0z8fFqP0VCgv8GTyFJfEki2XKyDJjp-qqHbs-76vGLMtpsY0jPjd7L94bVj9-pDprCAprVxcDZhVZlq0Neo8lRvx8CbTebCSvNE8_y2v1awiiD4UPIRj_qO21Zt15GiL34FD-0hRBHM7UX7xr_c1Vu3vGyH1eQFSCoWiP1TvdOCQcFoxEBsHoZaoKCP4qyF9p3CFyTrehrNvEE9Mu7fceZZWNPvXnz-fPXMYQfVnjFhaJl8wfongHMLrentqmD9donfDOB1FySu0NbCg_MckHasv5mgblVKUReq74l_uztr0uAKrcMnt-IuXUIWBDrsDTgo5EkN0CuPydI3Fpu23EUXByTicJOdvbq-2TaXaWZwSOwahmsL9UKnbLgGc7OKgbsGj36p6Z9ksFT23Fxwj3WoSWBoX1Me9pRHzc-Sn9uQm_xh2qMTMEhNzwVtWmF-P7y1fN_8-OrLSGlLD5yVC2CZncGYteNsjKf3jJyKdRV9k2MQwSrlv1LCjvdm2QSuduGDFCuMVwz63ai7EJLvrRsKPvLD1_NSp9wlgg1UbP2_fTHVP-CQiK4yW3pffZMUxsxsM966SKGdmCPNDu7eCmdang0R7s_sRhB2MJamX8urEJLLNl6r4-JtGz3PRu-C7ArAmvHWdvmDBlm0Tp1O3Ip1ErHK3BGQuRvHXG3UXhgMntiF5ikaIh3fdx-hN6QkcHFrzfmce5qSwoemH9MbPVyDEo0w4UZGQ9CQ8BLfgHzCV-sNOULcCtJ53jdxao6UBtEsTHlLrmTFeLsLYz5ckt7iyzSfBHnk-xXh0JS8UTLasU2ftLBP7ATnT4FeXYTbrZZQh_qZvIkOVN3pdDmXBf1XjqQzvruYvAwPRtbaGK9rQHeDSzVoJmh-bQ7u7nFZK09xsWdBnNrdsZ9XHtoa0DTcWGAC7QZRT_s_-IXmdId2T8yMLhlkO1zQtB_Qp33KZ-K6bOO6sNRAu67xPzLmIfnpSL6TWuac8CMgGeqwVuVMGWCQG0FRjR7aARCdaWgSEZ3g3D8cBYhtYDypMBzImw4tYh9MKzOpEC9KlmcTdDwkMZ9jfhcVlILEFUjf5SeiB8CbpQyeMajZXhwzmY5POyoc2hhcmRfaWTOD3Lqb6Jrcqc2Yzg1NjY5onBkAA.rJJySxXXad4nAeMOObK5c_6NKrGTrGNVNedHhE9KXJE"
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "cookie": COOKIES,
        "origin": "https://www.udio.com",
        "priority": "u=1, i",
        "referer": "https://www.udio.com/",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    data = response.text
    if not data:
        text = """status: 500, message: internal server error"""
    else:
        text = data
    await update.message.reply_text(text)

def handle_response(text:str)->str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'hey there'
    if 'how are you' in processed:
        return 'I am Good & you??'
    if 'I love Music' in processed:
        return 'Subscribe channel'
    return "I do not understand what you wrote......."
     
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str= update.message.chat.type
    text: str = update.message.text
    print(f'user({update.massage.chat.id})in {message_type}: "{text}"')
    
    if message_type =='group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()   
            response: str = handle_response(new_text)
        else:
            return 
    else:
        response: str = handle_response(text)
        
    print('Bot:', response)
    await update.message.reply_text(response)
 
async def logout_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    span_button = driver.find_element(by='xpath', value="/html/body/section/div[1]/div[2]/div[1]/div/div[2]/button[1]/span")
    span_button.click()
    time.sleep(5)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div/div[7]")))
    element.click()
    time.sleep(5)
    driver.quit()
    await update.message.reply_text("""Thanks For Using Vaishini BOT!!!""")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}') 

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('login', login_command))
    app.add_handler(CommandHandler('trending', trending_command))
    app.add_handler(CommandHandler('liked', liked_command))
    app.add_handler(CommandHandler('id', Id_command))
    app.add_handler(CommandHandler('autocreate', create_song))
    app.add_handler(CommandHandler('created', created_Song))
    app.add_handler(CommandHandler('logout', logout_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)
    print('polling......')
    app.run_polling(poll_interval=3)
    
