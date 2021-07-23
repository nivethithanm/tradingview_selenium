# Setup.py

#from typing import Awaitable
import random
import sqlite3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import asyncio
import warnings
import nest_asyncio

nest_asyncio.apply()

def do_query(path, q, args=None, commit=False):
    """
    do_query - Run a SQLite query, waiting for DB in necessary

    Args:
        path (str): path to DB file
        q (str): SQL query
        args (list): values for `?` placeholders in q
        commit (bool): whether or not to commit after running query
    Returns:
        list of lists: fetchall() for the query
    """
    if args is None:
        args = []
    for attempt in range(50):
        try:
            con = sqlite3.connect(path)
            cur = con.cursor()
            cur.execute(q, args)
            ans = cur.fetchall()
            if commit:
                con.commit()
            cur.close()
            con.close()
            del cur
            del con
            return ans
        except sqlite3.OperationalError:
            time.sleep(random.randint(10, 30))
            

warnings.filterwarnings("ignore")

class TelegramBot:
    def __init__(self, api_id, api_hash, phone):
        
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
    
    async def startClient(self):
        
        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)
        await self.client.connect()
        
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            await self.client.sign_in(self.phone,  input('Enter the code: '))
        
    async def getUsersList(self):
        groups = await self.getChannelsList()
        all_members = []
        for i in range(len(groups)):
            target_group=groups[i]
            target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)    
            print('Fetching Members...' + str(target_group.id))
            #print(all_members)
            all_participants = []
            try:
                all_participants = await self.client.get_participants(target_group, aggressive=True)
            except:
                continue
            #all_members.append(all_participants)
            
            for user in all_participants:
                    if user.username:
                        username= user.username
                    else:
                        username= ""
                    if user.first_name:
                        first_name= user.first_name
                    else:
                        first_name= ""
                    if user.last_name:
                        last_name= user.last_name
                    else:
                        last_name= ""
                    name= (first_name + ' ' + last_name).strip()
                    all_members.append([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
            
        print('Saving In file...')
        #print(all_members)
        
        with open("members.csv","w+",encoding='UTF-8') as f:
                writer = csv.writer(f,delimiter=",",lineterminator="\n")
                csv_dict = [row for row in csv.DictReader(f)]
                if len(csv_dict) == 0:
                    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
                for user in all_members:
                    writer.writerow(user)      
        
        print('Members saved successfully.')
        
        return all_members
     
    async def getChannelsList(self):
        chats = []
        last_date = None
        chunk_size = 200
        groups=[]
         
        result = await self.client(GetDialogsRequest(
                     offset_date=last_date,
                     offset_id=0,
                     offset_peer=InputPeerEmpty(),
                     limit=chunk_size,
                     hash = 0
                 ))
        chats.extend(result.chats)
        
        for chat in chats:
                try:
                    if chat.megagroup== True:
                        groups.append(chat)
                except:
                    continue
        
        input_file = 'groups.csv'
        with open(input_file,'w+',encoding='UTF-8') as f:
            writer = csv.writer(f,delimiter=",",lineterminator="\n")
            csv_dict = [row for row in csv.DictReader(f)]
            if len(csv_dict) == 0:
                writer.writerow(['group name','group id', 'access hash'])
            for group in groups:
                if group.title:
                    groupname = group.title
                else:
                    groupname = ""
                if group.id:
                    group_id = group.id
                else:
                    group_id = ""
                if group.access_hash:
                    access_hash = group.access_hash
                else:
                    access_hash = ""
                writer.writerow([groupname,group_id,access_hash])   
   
        return groups
        
    async def addMembers(self,group_id, group_access_hash):
        
        #users = self.getUsersList()

        users = []
        
        input_file = 'members2.csv'
        with open(input_file, 'r+', encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)
        
        target_group_entity = InputPeerChannel(group_id,group_access_hash)
        
        print(users)
        n = 0
        for user in users:
            n += 1
            if n % 50 == 0:
                time.sleep(900)
            try:
                print ("Adding {}".format(user['id']))
                if user['username'] == "":
                        continue
                user_to_add = self.client.get_input_entity(user['username'])
                self.client(InviteToChannelRequest(target_group_entity,[user_to_add]))
                print("Waiting for 60-180 Seconds...")
                time.sleep(random.randrange(60, 180))
            except PeerFloodError:
                print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
            except UserPrivacyRestrictedError:
                print("The user's privacy settings do not allow you to do this. Skipping.")
            except:
                traceback.print_exc()
                print("Unexpected Error")
                continue
                
async def telebot():
    # Access variables Definition
    api_id = 2420653
    api_hash = 'cf6d7d2c4b0c95e7ffe555079871e579'
    phone = '+918124992738'

    # Group id
    #group_id = GROUP_ID 
    #group_access_hash = 'GROUP_HASH'

    # Function Calls
    telegrambot = TelegramBot(api_id, api_hash, phone)
    await telegrambot.startClient()
    await telegrambot.getChannelsList()
    #await telegrambot.getUsersList()
    #await telegrambot.addMembers(group_id, group_access_hash)

loop = asyncio.get_event_loop()
loop.run_until_complete(telebot())
#loop.close()
