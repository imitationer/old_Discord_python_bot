# -*- coding=utf-8 -*-
import discord


class Role:
    """
    申請チャンネルのトピックに!roleを入れること
    """

    def __init__(self, client):
        
        self.client = client
        self.roles = {server: {f"{role.name.lower()}": role for role in server.roles} for server in client.servers}
        self.channels = {channel.server: channel for channel in client.get_all_channels() if "!role" in channel.topic}
        
        
    async def get_role_obj(self, message, role_name):
        role = self.roles[message.server][role_name.lower()]
        if role is None:
            await self.client.say(f"権限名'{role_name}'は存在していません")
            return False
        return role
        
   
    async def del_roles(self, author):
        for role in author.roles:
            await self.client.remove_roles(author, role)

    async def add_role(self, role, message, author, channel):
        if eval(f"self.client._{role.name}(message)"):
            await self.client.add_roles(author, role)
            await self.client.send_message(channel, f"{author.mention}に'{role.name}'権限付与しました")
            return True


    async def member(self, message, member, role_name, channel):
        role = self.get_role_obj(message, role_name)
    
        if role is False:
            return False
        if not self.client._user(message):
            await self.del_roles(member)
            return None
        if role in member.roles:
            return None

        if not hasattr(self.client,f"_{role.name}"):
            await self.client.say(f"権限名'{role.name}'付与エラー:<@{message.server.owner.id}>")
            return False
        if await self.add_role(role, message, member, channel):
            return True


    async def messeage_author(self, message, role_name):

        role = self.get_role_obj(message, role_name)
        if role is False:
            return 
        if not self.client._user(message):
            await self.del_roles(message.author)
            return 
        if role in message.author.roles:
            await self.client.say(f"{message.author.mention}は権限名'{role.name}'を既に持っています")
            return 

        if not hasattr(self.client,f"_{role.name}"):
            await self.client.say(f"権限名'{role.name}'付与エラー:<@{message.server.owner.id}>")
            return 

        if await self.add_role(role, message, message.author, message.channel):
            return True

        else:
            await self.client.say(f"{message.author.mention} に{role.name}権限付与出来ませんでした")


