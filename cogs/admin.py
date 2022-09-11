from __future__ import annotations

from typing import Literal, TYPE_CHECKING

import discord
from discord import app_commands, Interaction, ui
from discord.ext import commands

if TYPE_CHECKING:
    from bot import ValorantBot


class Admin(commands.Cog):
    """Error handler"""
    
    def __init__(self, bot: ValorantBot) -> None:
        self.bot: ValorantBot = bot
    
    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, sync_type: Literal['guild', 'global']) -> None:
        """ Sync the application commands """

        async with ctx.typing():
            if sync_type == 'guild':
                self.bot.tree.copy_global_to(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                await ctx.reply(f"Synced guild !")
                return

            await self.bot.tree.sync()
            await ctx.reply(f"Synced global !")
    
    @commands.command()
    @commands.is_owner()
    async def unsync(self, ctx: commands.Context, unsync_type: Literal['guild', 'global']) -> None:
        """ Unsync the application commands """
        
        async with ctx.typing():
            if unsync_type == 'guild':
                self.bot.tree.clear_commands(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                await ctx.reply(f"Un-Synced guild !")
                return
            
            self.bot.tree.clear_commands()
            await self.bot.tree.sync()
            await ctx.reply(f"Un-Synced global !")
    
    @app_commands.command(description='Shows basic information about the bot.')
    async def about(self, interaction: Interaction) -> None:
        """ Shows basic information about the bot. """
        
        owner_url = f'https://discord.com/users/258286165155643392'
        github_project = 'https://github.com/createdbyeric/Valorant-Bot'
        support_url = 'https://discord.com/users/258286165155643392'
        
        embed = discord.Embed(color=0xdc3d4b)
        embed.set_author(name='VALORANT Discord Bot', url=github_project)
        embed.add_field(
            name='Developer:',
            value=f"[CreatedbyEric]({owner_url})",
            inline=True
        )
        embed.add_field(
            name='Version:',
            value=f"`1.0.1`",
            inline=True
        )
        embed.add_field(
            name='Open Source:',
            value=f"Coming Soon",
            inline=True
        )
        view = ui.View()
        
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: ValorantBot) -> None:
    await bot.add_cog(Admin(bot))
