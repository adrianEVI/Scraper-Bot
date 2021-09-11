import os
import discord
import pandas as pd

#Create connection with Discord, this class is used to interact with the Discord WebSocket and API.
client = discord.Client()
guild = discord.Guild

@client.event
async def on_ready():
    print('\n\nWe have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('_scan'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith('_'):

        cmd = message.content.split()[0].replace("_","")

        if cmd == 'scan':

            data = pd.DataFrame(columns=['content', 'time', 'author'])
            channel = message.channel

            answer = discord.Embed(title="Creating your Message History Dataframe",
                                   description="Please Wait. The data will be sent to you privately once it's finished.",
                                   colour=0x1a7794) 

            limit=1000
            message_read=0
            await message.channel.send(embed=answer)

            def is_command (message):
                if len(msg.content) == 0:
                    return False
                elif msg.content.split()[0] == '_scan':
                    return True
                else:
                    return False
                
            async for msg in channel.history(limit=limit):       
                if msg.author != client.user:                           # a command or a message it sent, it will still read the
                    if not is_command(msg):                             # the total amount originally specified by the user.
                    
                        if msg.content!="":                             #check message content a string
                            data = data.append({'content': msg.content,
                                                'time': msg.created_at,
                                                'author': msg.author.name}, ignore_index=True)
                            message_read+=1
                    if len(data) == limit:
                        break
            
            
            #Filter of names
            users=data['author'].unique()
            n_users=data['author'].nunique()
            
            for i in range(n_users):
                data.loc[data["author"] == users[i], 'author'] = "user"+str(i+1)
                

            
            # Turning the pandas dataframe into a .csv file and sending it to the user
            file_location = f"{str(channel.guild.id) + '_' + str(channel.id)}.csv" # Determining file name and location
            data.to_csv(file_location, encoding="utf-8") # Saving the file as a .csv via pandas

            answer = discord.Embed(title="Here is your .CSV File",
                                   description=f"""Chat data.\n\n`Server` : **{message.guild.name}**\n`Channel` : **{channel.name}**\n`Messages Read` : **{message_read}**""",
                                   colour=0x1a7794) 

            await message.author.send(embed=answer)
            await message.author.send(file=discord.File(file_location, filename='data.csv')) # Sending the file
            os.remove(file_location) # Deleting the file
            
            
            
            
            # Turning the pandas dataframe into a .xlsx file and sending it to the user
            file_location = f"{str(channel.guild.id) + '_' + str(channel.id)}.xlsx" # Determining file name and location
            data.to_excel(file_location, encoding="utf-8") # Saving the file as a .xlsx via pandas

            answer = discord.Embed(title="Here is your EXCEL File",
                                   description=f"""Chat data.\n\n`Server` : **{message.guild.name}**\n`Channel` : **{channel.name}**\n`Messages Read` : **{message_read}**""",
                                   colour=0x1a7794) 

            await message.author.send(embed=answer)
            await message.author.send(file=discord.File(file_location, filename='data.xlsx')) # Sending the file
            os.remove(file_location) # Deleting the file
            

client.run('your-token-here')
