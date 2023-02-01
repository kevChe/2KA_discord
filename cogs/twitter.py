from discord.ext import commands, tasks
import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

class twitter(commands.Cog):
    
    urlTemplate = 'https://twitter.com/twitter/statuses/'
    # queries = ["from:usadapekora OR from:uraakapeko -is:retweet", "from:tokoyamitowa -is:retweet", "from:shirakamifubuki -is:retweet"]
    query = ["from:usadapekora OR from:uraakapeko OR from:tokoyamitowa OR from:shirakamifubuki -is:retweet"]
    since = 1618086166947061760

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'))


    @commands.Cog.listener()
    async def on_ready(self):
        print('twitter')
        self.channel = self.bot.get_channel(1067648094340141146)
        self.scrape.start()

    @tasks.loop(seconds=10)
    async def scrape(self):
        tweets = self.client.search_recent_tweets(query=self.query, tweet_fields=['context_annotations', 'created_at'], max_results=30, expansions=['author_id'], since_id=self.since)
        # print(tweets.data)
        if tweets.data is not None:
            for tweet in tweets.data:
                if tweet is not None:
                    await self.channel.send(f'{self.urlTemplate}{tweet.id}')
                    self.since = tweet.id


async def setup(bot):
    await bot.add_cog(twitter(bot))