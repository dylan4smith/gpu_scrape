from selenium import webdriver
from bs4 import BeautifulSoup
import discord

# inserts id into amazon url
def get_url(id):
    template = 'https://www.amazon.com/dp/{}/?aod=1'
    return template.format(id)

# scans RTX 3080 for price below 1100 on Amazon and sends link to Discord
async def discord_3080():
    await client.wait_until_ready()

    # gets channel ID for discord bot to send to
    channel = client.get_channel(id='''your discord channel id without quotes''')

    # ids for each product
    ids = [
        'B08JCRHZGW',
        'B09CLX9JB9',
        'B099ZC8H3G',
        'B08J6F174Z',
        'B099ZCG8T5',
        'B097S6JDMV'
    ]

    # create driver
    driver = webdriver.Chrome()

    # loop infinitely
    while True:

        # for each product ID
        for id in ids:

            # get url to scan
            driver.get(get_url(id))

            result = 0
            while result == 0:
                try:
                    # BeautifulSoup grabbing from webdriver
                    soup = BeautifulSoup(driver.page_source, 'html.parser')

                    # finds div with dollars and div with cents
                    aod = soup.find('div', id='aod-container')
                    dollars = aod.find('span', 'a-price-whole')
                    cents = aod.find('span', 'a-price-fraction')
                    result = 1
                except:
                    print('error')

            # converts dollars and cents into a single float value
            price = float(str(dollars).split('<span class="a-price-whole">')[1].split('<span class="a-price-decimal">')[0].replace(',', '') + '.' + str(cents).split('<span class="a-price-fraction">')[1].split('</span>')[0])

            # when price is equal to or below set price
            if price <= 1100:

                # print link in console
                print(get_url(id))

                # wait for bot to be ready
                await client.wait_until_ready()

                # send message with price and link
                await channel.send(str(price) + '\n' + get_url(id))

            # print price in console
            print(str(price) + ' | ' + get_url(id))

# setting discord client
client = discord.Client()

# when discord bot logs in
@client.event
async def on_ready():
    print('Logged in as {} ID: {}'.format(client.user.name, client.user.id))

# run discord_3080 with discord bot
client.loop.create_task(discord_3080())

# discord bot token
token = "[Your Discord Bot Token]"

# run bot
client.run(token)
