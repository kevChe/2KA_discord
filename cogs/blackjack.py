from discord.ext import commands, tasks
import discord
from discord import File, app_commands
import pymysql
import random
import asyncio
# from .transaction import get_cardboards, update_cardboards

class Deck:
    def __init__(self):
        self.deck = [card for card in range(2, 11)] * 4 + ['A', 'J', 'Q', 'K'] * 4
    
    def shuffle(self):
        random.shuffle(self.deck)

    def get_deck(self):
        print(self.deck)
    
    def deal_card(self):
        return self.deck.pop()
    
class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def get_cards(self):
        return self.cards
    
    def add_card(self, card):
        self.cards.append(card)

    def get_name(self):
        return self.name

    def get_value(self):
        value = 0
        ace = 0
        for card in self.cards:
            if card in [10, 'J', 'Q', 'K']:
                value += 10
            elif card != 'A':
                value += card
            else:
                ace += 1
                value += 11
        
        while value > 21 and ace > 0:
            ace -= 1
            value -= 10
        return value

class blackjack(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.players = []
        self.start_msg = f"21點準備開始，想參加的請按加入游戲"
        self.game_msg = ""
        self.send_msg: discord.WebhookMessage
        self.deck = Deck()

    @commands.Cog.listener()
    async def on_ready(self):
        print('BlackJack ONLINE')    

    @app_commands.command(name="21點")
    async def start(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="21點游戲開始！",view= await self.start_view(),)
        # self.send_msg = await interaction.followup.send(content="21點游戲開始！", wait=True,view= await self.start_view(),)
        # self.send_msg = await interaction.followup.send(content="21點游戲開始！", wait=True,)
        # print(self.send_msg)
        self.deck.shuffle()
    
    async def start_view(self):
        view = discord.ui.View()
        add_player_button = discord.ui.Button(label="加入游戲")
        start_game_button = discord.ui.Button(label="開始游戲")

        async def add_player_action(interaction: discord.Interaction):
            if interaction.user.name not in self.players:
                self.players.append(Player(interaction.user.name))
                self.start_msg += f"\n{interaction.user.name}加入了游戲"
                await interaction.response.edit_message(content=self.start_msg)
            else:
                await interaction.response.send_message(content=f'你已經加入游戲了')

        async def start_game_action(interaction: discord.Interaction):
            if not self.players:
                await interaction.response.edit_message(content=f"游戲最少需要一個人才能開始，請點加入游戲來加入")
            else:
                self.deal_cards()
                player = self.players[0]
                print(player)
                self.game_msg = f"{player.get_name()}，你想在的牌是{player.get_cards()}請選擇要**加牌**還是**不加牌**"
                await interaction.response.edit_message(content=self.game_msg, view= await self.game_view(player, 0))


        add_player_button.callback = add_player_action
        start_game_button.callback = start_game_action
        view.add_item(add_player_button)
        view.add_item(start_game_button)
        return view
    
    def deal_cards(self):
        player: Player
        for player in self.players:
            player.add_card(self.deck.deal_card())
            player.add_card(self.deck.deal_card())
    
    async def game_view(self, player: Player, i):
        view = discord.ui.View()
        hit = discord.ui.Button(label="加牌")
        stand = discord.ui.Button(label="不加牌")

        async def add_hit_action(interaction: discord.Interaction):
            player.add_card(self.deck.deal_card())
            self.game_msg = f"{player.get_name()}，你想在的牌是{player.get_cards()}請選擇要**加牌**還是**不加牌** {player.get_value()}"
            if player.get_value() > 21:
                await interaction.response.edit_message(content=self.game_msg, view=await self.explode(player.get_value(), i))
            else:
                await interaction.response.edit_message(content=self.game_msg)
        
        async def add_stand_action(interaction: discord.Interaction):
            # if i + 1 == len(self.players):
            #     await self.endgame(interaction)
            # else:
            await self.next_player(interaction, i)

        hit.callback = add_hit_action
        stand.callback = add_stand_action
        view.add_item(hit)
        view.add_item(stand)
        return view
    
    async def next_player(self, interaction:discord.Interaction, i):
        if i + 1 == len(self.players):
            await self.endgame(interaction)
        else:
            player = self.players[i + 1]
            self.game_msg = f"{player.get_name()}，你想在的牌是{player.get_cards()}請選擇要**加牌**還是**不加牌**"
            await interaction.response.edit_message(content=self.game_msg, view=await self.game_view(player, i + 1))

    async def explode(self, points, i):
        view = discord.ui.View()
        button = discord.ui.Button(label=f"總共{points}點，爆掉了")
        async def action(interaction: discord.Interaction):
            await self.next_player(interaction, i)
        button.callback = action
        view.add_item(button)
        return view
    
    async def endgame(self, interaction: discord.Interaction):
        msg = ""
        player: Player
        for player in self.players:
            msg += f'{player.get_name()} 你的手牌是 {player.get_cards()}\n'
        await interaction.followup.send(content=msg)
        dealer = Player("莊家")
        send_msg: discord.WebhookMessage
        send_msg = await interaction.followup.send(content=f"莊家的手牌是: {dealer.get_cards()}", wait=True)
        dealer.add_card(self.deck.deal_card())
        while(int(dealer.get_value()) < 17):
            dealer.add_card(self.deck.deal_card())
            await send_msg.edit(content=dealer.get_cards())

    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        blackjack(bot), 
        guild = discord.Object(id = 1021667971682287627))
