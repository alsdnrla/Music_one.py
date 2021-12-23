import discord 
from ast import literal_eval
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, CommandNotFound
from discord_buttons_plugin import  *
import asyncio
from youtube_dl import YoutubeDL
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import urllib.parse
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time
import requests
from discord.utils import get
import os
import json
import math
import pandas as pd
import random
import re
import discord_fortuneTell
import random
from pytube import YouTube
from discord.ext import commands
from discord_together import DiscordTogether

access_token = os.environ["BOT_TOKEN"] 

bot = commands.Bot(command_prefix=';')
client = discord.Client()
buttons = ButtonsClient(bot)



user = []
musictitle = []
song_queue = []
musicnow = []

userF = []
userFlist = []
allplaylist = []


number = 1



def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    driver = load_chrome_driver()
    driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()
    
    musictitle.append(music)
    musicnow.append(music)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']

    driver.quit()
    
    return music, URL

def play(ctx):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    vc = get(bot.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx)) 

def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))


    else:
        if not vc.is_playing():
            client.loop.create_task(vc.disconnect())


def load_chrome_driver():
      
    options = webdriver.ChromeOptions()

    options.binary_location = os.getenv('GOOGLE_CHROME_BIN')

    options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    return webdriver.Chrome(executable_path=str(os.environ.get('CHROME_EXECUTABLE_PATH')), chrome_options=options)            

def again(ctx, url):
    global number
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if number:
        with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        if not vc.is_playing():
            vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: again(ctx, url))



@bot.event
async def on_ready():
    print("로그인중")
    print(bot.user.name)
    print("connect was sucessful")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("갬성 힙합을 연구"))
    bot.togetherControl = await DiscordTogether(access_token)
    
    if not discord.opus.is_loaded():
        discord.opus.load_opus('opus')
    
@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title = "음악한곡", description = "유튜브 라이센스를 사용합니다.", color = 0x6E17E3) 
    embed.add_field(name = bot.command_prefix + "도움", value = "명령어를 볼수 있습니다,", inline = False)
    embed.add_field(name = bot.command_prefix + "들어와", value = "뮤직봇이 음성채널에 들어갑니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "나가", value = "뮤직봇이 채널에서 나갑니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "재생 [노래 이름]  [작곡가] ", value = "유튜브검색기능을 활용하여 찾아드립니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "반복재생 [노래 이름] [작곡가] ", value = "찾은 노래를 반복재생합니다..", inline = False)
    embed.add_field(name = bot.command_prefix + "목록", value = "자신의 플레이 리스트를 볼수있습니다", inline = False)
    embed.add_field(name = bot.command_prefix + "목록초기화", value = "목록에 있는 모든 대기열을 삭제합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "목록추가 [노래 이름] [작곡가]", value = "음악이 목록에 추가됩니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "목록삭제 [대기열 번호]", value = "대기열에 있는 목록이 삭제됩니다..", inline = False)
    embed.add_field(name = bot.command_prefix + "차트", value = "멜론 차트순위 1~10위까지의 노래를 가져옵니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "가사 [노래이름]", value = "노래재목과 유사한 노래 1~5개 까지의 리스트를 뽑아옵니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "선택 [번호]", value = "선택된 노래의 가사를 가져옵니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "즐겨찾기 [추가, 삭제]", value = "즐겨찾기한 노래의 목록을 볼수 있습니다 [추가할수 있습니다] [삭제할수 있습니다]", inline = False)
    embed.add_field(name = bot.command_prefix + "추천곡", value = "추천곡을 즉시 재생할수 있습니다. [이미 재생중이라면 목록으로 자동추가 됩니다.]", inline = False)
    embed.add_field(name = bot.command_prefix + "추천곡리스트", value = "무작위로 추천곡 4개를 선곡하여 목록으로 추가시킬수 있습니다. [대기시간 필요]")
    embed.add_field(name = bot.command_prefix + "미니게임 도움말", value = "<New!> 미니게임 도움말을 볼수 있습니다. [beta] ", inline = False)
    await ctx.send(embed=embed)
    
    
@bot.command()
async def 미니게임도움말(ctx):
    poker_url = "https://www.7luck.com/JSPVIEW/default?URL_JSP=--guid--GUID_04_09_02&sel_lang_typ=KR"
    chess_url = "https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=qpa9&logNo=30146423629"
    checkers_url = "https://ko.wikihow.com/%EC%B2%B4%EC%BB%A4-%EA%B2%8C%EC%9E%84%ED%95%98%EB%8A%94-%EB%B2%95"
        
    embed = discord.Embed(title = "미니게임", description = "Discord-Together", color = 0x6E17E3) 
    embed.add_field(name = bot.command_prefix + "`beta poker`", value = "텍사스 홀덤(포커) 최대 7인까지 가능하며 \n 룰은" + "[이곳에서](<{0}>)".format(poker_url) + "보실수 있습니다", inline = False)
    embed.add_field(name = bot.command_prefix + "`beta chess`", value = "체스 최대 2인까지 가능하며 \n 룰은" + "[이곳에서](<{0}>)".format(chess_url) + "보실수 있습니다", inline = False)
    embed.add_field(name = bot.command_prefix + "`beta checkers`", value = "체커 최대 2인까지 가능하며 \n 룰은" + "[이곳에서](<{0}>)".format(checkers_url) + "보실수 있습니다", inline = False)
    embed.add_field(name = bot.command_prefix + "`beta youtube`", value = "유튜브에 영상을 함께 볼수 있습니다.", inline = False)
    embed.set_footer(text='현제 모바일은 지원되지 않습니다.')
    await ctx.send(embed=embed)


@bot.command(aliases = ('ㄷ', '컴온', '들와', '참가'))
async def 들어와(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(f"{ctx.author.mention} 채널에 유저가 접속해있지 않습니다.")

@bot.command(aliases=('나가', 'ㄲ', '안해', '끄기'))
async def 꺼져(ctx):
    try:
        await vc.disconnect()
    except:
        await ctx.send(f"{ctx.author.mention} 이미 그 채널에 속해있지 않아요.")


@bot.command()
async def URL재생(ctx, *, url):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(f"{ctx.author.mention} 채널에 유저가 접속해있지 않습니다.")

            
    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + url + "을(를) 재생하고 있습니다.", color = 0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있습니다!")

@bot.command(aliases=('탐색', '시작', '플레이', 'ㅈㅅ'))
async def 재생(ctx, *, msg):


    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(f"{ctx.author.mention} 채널에 유저가 접속해있지 않습니다.")


    
    if not vc.is_playing():

        #selenium웹 드라이버를 보이지 않게하는 설정
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("lang=ko_KR")

        
        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        driver = load_chrome_driver()
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl
        
        yt = YouTube(url)

        #드라이버 닫기

        driver.quit()

        musicnow.insert(0, entireText)

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        embed = discord.Embed(title= "노래 재생", description = "현재 " + "[{0}](<{1}>)".format(entireText, url) + "을(를) 재생하고 있습니다.", color = 0x00ff00)
        embed.add_field(name = '재생시간', value = str(yt.length) + "초", inline = False)
        embed.add_field(name = '평점', value = str(yt.rating) + "회", inline = False)
        embed.set_footer(text = '게시자 - ' + yt.author)
        embed.set_thumbnail(url=yt.thumbnail_url)
        await ctx.send(embed=embed)
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: play_next(ctx))
    else:
        user.append(msg)
        result,URLTEST = title(msg)
        song_queue.append(URLTEST)
        await ctx.send("이미 노래가 재생 중이라" + result + "을(를) 대기열로 추가시켰습니다")
        

        
@bot.command()
async def 스킵(ctx):
    if len(user) >= 1:
        if vc.is_playing():
            vc.stop()
            global number
            number = 0
            await ctx.send(embed = discord.Embed(title = "스킵", description = musicnow[1] + "을(를) 다음에 재생합니다!", color = 0x00ff00))
        else:
            await ctx.send("노래가 이미 재생되고 있어요!")
    else:
        await ctx.send("더이상 스킵할 노래가 없습니다.")
        

@bot.command(aliases=('ㅈㅈ', 'ㅇㅅㅈㅈ'))
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed = discord.Embed(title= "일시정지", description = musicnow[0] + "을(를) 일시정지 했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

@bot.command(aliases=('ㄷㅅㅈㅅ', '리플레이'))
async def 다시재생(ctx):
    try:
        vc.resume()
    except:
         await ctx.send("지금 노래가 재생되지 않네요.")
    else:
         await ctx.send(embed = discord.Embed(title= "다시재생", description = musicnow[0]  + "을(를) 다시 재생했습니다.", color = 0x00ff00))

@bot.command(aliases=('ㄲㄱ', '노래스탑'))
async def 노래끄기(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = musicnow[0]  + "을(를) 종료했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")


@bot.command(aliases=('지금나오는거', '현재노래', '노래정보'))
async def 지금노래(ctx):
    if not vc.is_playing():
        await ctx.send("지금은 노래가 재생되지 않네요..")
    else:
        await ctx.send(embed = discord.Embed(title = "지금노래", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))


@bot.command(aliases=('ㅁㄹㅊㄱ', '목록추가'))
async def 대기열추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(result + "를 재생목록에 추가했어요!")

@bot.command(aliases=('ㅁㄹㅅㅈ', '목록삭제'))
async def 대기열삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number)-1]
        del musicnow[int(number)-1+ex]
            
        await ctx.send("대기열이 정상적으로 삭제되었습니다.")
    except:
        if len(list) == 0:
            await ctx.send("대기열에 노래가 없어 삭제할 수 없어요!")
        else:
            if len(list) < int(number):
                await ctx.send("숫자의 범위가 목록개수를 벗어났습니다!")
            else:
                await ctx.send("숫자를 입력해주세요!")

@bot.command(aliases=('ㅁㄹ', '대기열'))
async def 목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
        await ctx.send(embed = discord.Embed(title= "노래목록", description = Text.strip(), color = 0x00ff00))

@bot.command(aliases=('ㅁㄹㅊㄱㅎ', '대기열초기화'))
async def 목록초기화(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(embed = discord.Embed(title= "목록초기화", description = """목록이 정상적으로 초기화되었습니다. 이제 노래를 등록해볼까요?""", color = 0x00ff00))
    except:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")

@bot.command(aliases=('ㅁㄹㅈㅅ', '대기열재생'))
async def 목록재생(ctx):

    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(f"{ctx.author.mention} 채널에 유저가 접속해있지 않습니다.")

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    if len(user) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        if len(musicnow) - len(user) >= 1:
            for i in range(len(musicnow) - len(user)):
                del musicnow[0]
        if not vc.is_playing():
            play(ctx)
        else:
            await ctx.send("노래가 이미 재생되고 있어요!")




@bot.command()
async def 차트(ctx):
    RANK = 10
 
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    req = requests.get('https://www.melon.com/chart/week/index.htm', headers = header) ## 주간 차트를 크롤링 할 것임
    html = req.text
    parse = BeautifulSoup(html, 'html.parser')
 
    titles = parse.find_all("div", {"class": "ellipsis rank01"}) 
    singers = parse.find_all("div", {"class": "ellipsis rank02"}) 
    albums = parse.find_all("div",{"class": "ellipsis rank03"})
 
    title = []
    singer = []
    album = []
 
    for t in titles:
        title.append(t.find('a').text)
 
    for s in singers:
        singer.append(s.find('span', {"class": "checkEllipsis"}).text)

    for a in albums:
        album.append(a.find('a').text)

   
    embed = discord.Embed(title = "Music chart", description = "출처 - 멜론 공식사이트", color = 0x6E17E3)
    for i in range(RANK):
        embed.add_field(name='%3d위: %s [ %s ] - %s'%(i+1, title[i], album[i], singer[i]), value = "ㅤ")
        embed.set_footer(text="주간순위")
        #value -> 공백문자임
    await ctx.send(embed=embed)
            
            
       
        
        
        
        


@bot.command(aliases=('ㅂㅂㅈㅅ', '계속재생'))
async def 반복재생(ctx, *, msg):
    
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
      
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()   
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            pass
    
    global entireText
    global number
    number = 1
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    if len(musicnow) - len(user) >= 1:
        for i in range(len(musicnow) - len(user)):
            del musicnow[0]
            
    driver = load_chrome_driver()
    driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    entireText = entireNum.text.strip()
    musicnow.insert(0, entireText)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    yt = YouTube(url)
    embed = discord.Embed(title= "반복재생", description = "현재 " + "[{0}](<{1}>)".format(musicnow[0], url)+ "을(를) 반복재생하고 있습니다.", color = 0x00ff00)
    embed.add_field(name = '재생시간', value = str(yt.length) + "초", inline = False)
    embed.add_field(name = '평점', value = str(yt.rating) + "회", inline = False)
    embed.set_footer(text = '게시자 - ' + yt.author)
    embed.set_thumbnail(url=yt.thumbnail_url)
    await ctx.send(embed = embed)
    again(ctx, url)



@bot.command()
async def 가사(ctx, song):
    global datas
    global title1

    
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    
    # webdriver 생성 및 대기
    driver = load_chrome_driver()
    driver.implicitly_wait(2)
    # 곡 입력 및 url 접근
    driver.get('https://vibe.naver.com/search/tracks?query='+song)
    time.sleep(2)
    # 페이지 HTML 소스 받기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # 곡 목록 받아오기
    tbody = soup.select_one('div.tracklist > table > tbody')
    trs = tbody.select('tr')
    datas = []
    count = 0
    embed = discord.Embed(title = "Music chart", description = "출처 - 멜론 공식사이트", color = 0x6E17E3)

    for tr in trs:
        title1 = tr.select_one('td.song > div.title_badge_wrap > span > a').get_text()
        artist = tr.select_one('td.artist > span > span > span > a > span').get_text()
        title_id = tr.select_one('td.song > div.title_badge_wrap > span > a')['href']
        datas.append([title1, artist, title_id])
        if count < 4:
            count += 1
        else:
            driver.quit()
            break


    for i in range(count+1):
        embed.add_field(name=f'{i+1}번 : {datas[i][0]} by {datas[i][1]}', value = "ㅤ")
    embed.add_field(name="찾으시는 곡번을 선택해주세요.\n 종료하시려면 0번을 입력해주세요.", value = "ㅤ")
    embed.set_footer(text="출처 - 바이브 공식사이트")
    driver.quit()
    await ctx.send(embed=embed)
    try:
        pass
    except:
        await ctx.send("불러오는 도중 오류가 발생하거나 검색하신 내용이 없어요..")




            

@bot.command()
async def 선택(ctx, menu):
    try:
        pass 
    except:
        await ctx.send("선택하신 사항이 없어요..")
    mem = 0
    mem = int(menu)
    
    

    
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = load_chrome_driver()
    
    embed = discord.Embed(title = "Music lyrics", description = "출처 - 바이브 공식사이트", color = 0x6E17E3)
    if mem == 0:
        await ctx.send("종료했습니다.")
        driver.quit()
            
        
    else:
        driver.get('https://vibe.naver.com'+datas[mem-1][2])
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        lyrics = soup.select_one('#content > div > p.lyrics').get_text()
        for i in range(0, len(lyrics),1024):
            embed.add_field(name=title1, value = lyrics[i:i+1024])
            embed.set_footer(text="출처 - 바이브 공식사이트")
            await ctx.send(embed=embed)
        
        
            
            
    driver.quit()


@bot.command()
async def 즐겨찾기(ctx):
    global Ftext
    Ftext = ""
    correct = 0
    global Flist
    for i in range(len(userF)):
        if userF[i] == str(ctx.message.author.name): #userF에 유저정보가 있는지 확인
            correct = 1 #있으면 넘김
    if correct == 0:
        userF.append(str(ctx.message.author.name)) #userF에다가 유저정보를 저장
        userFlist.append([]) #유저 노래 정보 첫번째에 유저이름을 저장하는 리스트를 만듬.
        userFlist[len(userFlist)-1].append(str(ctx.message.author.name))
        
    for i in range(len(userFlist)):
        if userFlist[i][0] == str(ctx.message.author.name):
            if len(userFlist[i]) >= 2: # 노래가 있다면
                for j in range(1, len(userFlist[i])):
                    Ftext = Ftext + "\n" + str(j) + ". " + str(userFlist[i][j])
                titlename = str(ctx.message.author.name) + "님의 즐겨찾기"
                embed = discord.Embed(title = titlename, description = Ftext.strip(), color = 0x00ff00)
                embed.add_field(name = "목록에 추가\U0001F4E5", value = "즐겨찾기에 모든 곡들을 목록에 추가합니다.", inline = False)
                embed.add_field(name = "플레이리스트로 추가\U0001F4DD", value = "즐겨찾기에 모든 곡들을 새로운 플레이리스트로 저장합니다.", inline = False)
                Flist = await ctx.send(embed = embed)
                await Flist.add_reaction("\U0001F4E5")
                await Flist.add_reaction("\U0001F4DD")
            else:
                await ctx.send("아직 등록하신 즐겨찾기가 없어요.")



@bot.command()
async def 즐겨찾기추가(ctx, *, msg):
    correct = 0
    for i in range(len(userF)):
        if userF[i] == str(ctx.message.author.name): #userF에 유저정보가 있는지 확인
            correct = 1 #있으면 넘김
    if correct == 0:
        userF.append(str(ctx.message.author.name)) #userF에다가 유저정보를 저장
        userFlist.append([]) #유저 노래 정보 첫번째에 유저이름을 저장하는 리스트를 만듦.
        userFlist[len(userFlist)-1].append(str(ctx.message.author.name))

    for i in range(len(userFlist)):
        if userFlist[i][0] == str(ctx.message.author.name):
            
            options = webdriver.ChromeOptions()
            options.add_argument("headless")

            
            driver = load_chrome_driver()
            driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
            source = driver.page_source
            bs = bs4.BeautifulSoup(source, 'lxml')
            entire = bs.find_all('a', {'id': 'video-title'})
            entireNum = entire[0]
            music = entireNum.text.strip()

            driver.quit()

            userFlist[i].append(music)
            await ctx.send(music + "(이)가 정상적으로 등록되었어요!")



@bot.command()
async def 즐겨찾기삭제(ctx, *, number):
    correct = 0
    for i in range(len(userF)):
        if userF[i] == str(ctx.message.author.name): #userF에 유저정보가 있는지 확인
            correct = 1 #있으면 넘김
    if correct == 0:
        userF.append(str(ctx.message.author.name)) #userF에다가 유저정보를 저장
        userFlist.append([]) #유저 노래 정보 첫번째에 유저이름을 저장하는 리스트를 만듦.
        userFlist[len(userFlist)-1].append(str(ctx.message.author.name))

    for i in range(len(userFlist)):
        if userFlist[i][0] == str(ctx.message.author.name):
            if len(userFlist[i]) >= 2: # 노래가 있다면
                try:
                    del userFlist[i][int(number)]
                    await ctx.send("정상적으로 삭제되었습니다.")
                except:
                     await ctx.send("입력한 숫자가 잘못되었거나 즐겨찾기의 범위를 초과하였습니다.")
            else:
                await ctx.send("즐겨찾기에 노래가 없어서 지울 수 없어요!")

                

@bot.event
async def on_reaction_add(reaction, users):
    if users.bot == 1:
        pass
    else:
        try:
            await Flist.delete()
        except:
            pass
        else:
            if str(reaction.emoji) == '\U0001F4E5':
                await reaction.message.channel.send("잠시만 기다려주세요. (즐겨찾기 갯수가 많으면 지연될 수 있습니다.)")
                print(users.name)
                for i in range(len(userFlist)):
                    if userFlist[i][0] == str(users.name):
                        for j in range(1, len(userFlist[i])):
                            try:
                                driver.close()
                            except:
                                print("NOT CLOSED")

                            user.append(userFlist[i][j])
                            result, URLTEST = title(userFlist[i][j])
                            song_queue.append(URLTEST)
                            await reaction.message.channel.send(userFlist[i][j] + "를 재생목록에 추가했어요!")
            elif str(reaction.emoji) == '\U0001F4DD':
                await reaction.message.channel.send("플레이리스트가 나오면 생길 기능이랍니다. 추후 업데이트를 기대해 주세요!")
            
               
    
    
    
@bot.command(aliases=['운세'])
async def today_fortune(ctx, *args):
    args = list(args)
    print(args)
    await ctx.send(discord_fortuneTell.out(args))


    
    
@bot.command()
async def 추천곡(ctx):
    global mum
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    

    driver = load_chrome_driver()

    driver.get('https://www.music-flo.com/')
    time.sleep(3)

    html = driver.page_source
    parse = BeautifulSoup(html, 'html.parser')

    music = parse.select_one('#main > div > section.section_content_wrap.personal > div.section_content.swiper_horizon.PERSONAL_swiper_container.swiper-container-initialized.swiper-container-horizontal > ul > li.swiper-slide.type_theme.swiper-slide-active > a > div.personal_recommend_head > h4').get_text()
    

    embed = discord.Embed(title=f" <{ctx.author.name}>님을 위한 추천곡이에요.", description=music, color=0xAAFFFF)

    rn = random.randint(1, 4)
    
    
    

    mum = parse.select_one('#main > div > section.section_content_wrap.personal > div.section_content.swiper_horizon.PERSONAL_swiper_container.swiper-container-initialized.swiper-container-horizontal > ul > li.swiper-slide.type_theme.swiper-slide-active > a > div.me_album_tracklist > div > ul:nth-child(1) > li:nth-child({0}) > div > strong'.format(rn)).get_text()
    embed.add_field(name=mum, value='Flo api 사용', inline=False)

    im = parse.select('#main > div > section.section_content_wrap.personal > div.section_content.swiper_horizon.PERSONAL_swiper_container.swiper-container-initialized.swiper-container-horizontal > ul > li.swiper-slide.type_theme.swiper-slide-active > a > div.me_album_tracklist > div > ul:nth-child(1) > li:nth-child({0}) > div > img'.format(rn))
        
    for ims in im:
        img = ims['src']

    
    embed.set_thumbnail(url=img)
    
    

    driver.quit()

    await ctx.send(embed=embed)
    await buttons.send(
        content = "아래쪽 버튼을 눌러주세요.",
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label="지금바로 재생하기", 
                    style=ButtonType().Primary, 
                    custom_id="button_one"       
                )
            ])
        ]
    )




@buttons.click
async def button_one(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.reply("채널에 봇이 접속해 있지 않습니다.  [;들어와]명령어를 통해 봇을 추가하세요.")


    
    if not vc.is_playing():

        #selenium웹 드라이버를 보이지 않게하는 설정
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        
        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        driver = load_chrome_driver()
        try:
            driver.get("https://www.youtube.com/results?search_query="+mum+"+lyrics")
        except:
            await ctx.reply("어제 들었던 곡은 이용이 안됩니다!")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl

        #드라이버 닫기

        driver.quit()

        musicnow.insert(0, entireText)

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.reply(embed = discord.Embed(title= "노래 재생", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: play_next(ctx))
    else:
        user.append(mum)
        result,URLTEST = title(mum)
        song_queue.append(URLTEST)
        await ctx.reply("이미 노래가 재생 중이라" + result + "을(를) 대기열로 추가시켰습니다")




@bot.command()
async def 추천곡리스트(ctx):
    global mum
    mum = []
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    

    driver = load_chrome_driver()

    driver.get('https://www.music-flo.com/')
    time.sleep(3)

    html = driver.page_source
    parse = BeautifulSoup(html, 'html.parser')

    music = parse.select_one('#main > div > section.section_content_wrap.personal > div.section_content.swiper_horizon.PERSONAL_swiper_container.swiper-container-initialized.swiper-container-horizontal > ul > li.swiper-slide.type_theme.swiper-slide-active > a > div.personal_recommend_head > h4').get_text()
    

    embed = discord.Embed(title=f" <{ctx.author.name}>님을 위한 추천곡이에요.", description=music, color=0xAAFFFF)

    
    
    for i in range(1,5):
        mum.append(parse.select_one('#main > div > section.section_content_wrap.personal > div.section_content.swiper_horizon.PERSONAL_swiper_container.swiper-container-initialized.swiper-container-horizontal > ul > li.swiper-slide.type_theme.swiper-slide-active > a > div.me_album_tracklist > div > ul:nth-child(1) > li:nth-child({0}) > div > strong'.format(i)).get_text())
        mam = parse.select_one('#main > div > section.section_content_wrap.personal > div.section_content.swiper_horizon.PERSONAL_swiper_container.swiper-container-initialized.swiper-container-horizontal > ul > li.swiper-slide.type_theme.swiper-slide-active > a > div.me_album_tracklist > div > ul:nth-child(1) > li:nth-child({0}) > div > strong'.format(i)).get_text()
        embed.add_field(name=mam, value='ㅤ', inline=False)

    
    

    embed.set_footer(text='flo api')
    driver.quit()

    await ctx.send(embed=embed)
    await buttons.send(
        content = "아래쪽 버튼을 눌러주세요.",
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label="추천곡 리스트를 목록에 저장하기", 
                    style=ButtonType().Primary, 
                    custom_id="button_two"       
                )
            ])
        ]
    )




@buttons.click
async def button_two(ctx):
    for i in range(len(mum)):
        print(mum[i])
        user.append(mum[i])
        result, URLTEST = title(mum[i])
        song_queue.append(URLTEST)
    
    await ctx.reply(mum[i] + "를 대기열 목록에 추가했습니다.")
    
@bot.command()
async def start(ctx):
    link = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
    await ctx.send(f"링크를 눌러주세요\n{link}")

@bot.command()
async def beta(ctx, game_name):
    try:
        link = await bot.togetherControl.create_link(ctx.author.voice.channel.id, '{0}'.format(game_name))
        await ctx.send(f"링크를 눌러주세요\n{link}")
    except:
        await ctx.send("1.게임이름이 정확한지 확인해 주세요 \n 2. 음성체널에 참가하여 있는지 확인해 주세요.")
    
    """


with open('./userdata.json', 'r') as json_file:
    userdata = json.load(json_file)





def getNowPrice(name, df):
    try:
        code = str(int(name))
    except ValueError:
        code = str(df[df.회사명 == name].종목코드.values)[1:-1].zfill(6)
    else:
        code = code.zfill(6)
        name = str(df[df.종목코드 == int(code.lstrip("0"))].회사명.values)[2:-2]
    finally:
         
        # url만 바꾸면 각 기업에 따른 값 크롤링 가능
        html = urllib.request.urlopen("https://finance.naver.com/item/main.nhn?code=" + code)

        bs_obj = bs4.BeautifulSoup(html, "html.parser")
    
        data = bs_obj.find("div", {"class": "today"})
        data_first = data.find("span", {"class": "blind"})
        data_realTime = data_first.text  # 실시간 가격
        data_realTime_result = data_realTime.replace(",","")
        data_realTime_int = int(data_realTime_result)
        price = data_realTime_int
        print(data_realTime_int)
        print(data_realTime)
        

        if price == None:
            code = None
        return name, code, price
            
        


sendMoneyCommand = ['보내기', '송금', 'ㅅㄱ', 'tr', 'send']
myStockCommand = ['내주식', '내', 'ㄵㅅ', 'ㄴㅈㅅ', 'ㄴ', 'swt', 's', 'my']
sellStockCommand = ['판매', '매도', 'sell', 'va']
buyStockCommand = ['구매', '매수', 'buy', 'ra']
selectAllCommand = ['전부', '모두', 'ㅈㅂ', '올인', 'all', 'wq', 'ae']
checkLotteryCommand = ['확인', 'ㅎㅇ', 'gr', 'check']
lotteryNumberCommand = ['번호', 'ㅂㅎ', 'qg', 'number']
latestLotteryCommand = ['최신', '현재', 'ㅊㅅ', 'ㅎㅈ', 'ct', 'gw', 'now', 'latest']
lotteryAutoCommand = ['자동', 'ㅈㄷ', 'auto', 'we']


@bot.command(aliases=['주식명령어', '주식 커맨드'])
async def 주식도움말(ctx, *content):
    embed = discord.Embed(title = "멸망의 주식시장", description = "현재 존재하는 모든 주식의 매매가 가능합니다.\n 장 시작시간(공휴일,주말 제외) 오전9:00 / 장 마감시간 오후3:00", color = 0x6E17E3)
    embed.add_field(name = bot.command_prefix + "주식 매수 <기업명/종목코드> <수량/올인>", value = " 그 기업의 주식을 <수량만큼> 매수합니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "주식 매도 <기업명/종목코드> <수량/올인>", value = "그 기업의 주식을 <수량만큼> 매도합니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "보유주식", value = "자신이 가지고 있는 주식을 보여줍니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "지갑", value = "자신이 가지고 있는 돈을 보여줍니다", inline = False)
    embed.add_field(name = bot.command_prefix + "용돈", value = "20,0000원 에서 50,0000원 까지 용돈을 부여합니다 [하루에 한번씩 받을수 있음]", inline = False)
    embed.add_field(name = '주의사항', value = '-원금손실에 유의하여주세요 \n -명령어가 안된다고 마구 남발하지 말아주세요 딜레이가 있습니다', inline = False )
    embed.set_footer(text = "Beta - 앞으로의 업데이트를 기대해 주세요!")
    await ctx.send(embed=embed)


@bot.command(aliases=['ㄱㅇ', 'join', 'register'])
async def 가입(ctx, *content):
    await checkUser(ctx, lambda: sendAlreadyRegisteredMessage(ctx), lambda: register(ctx))


@bot.command(aliases=['지갑', 'ehs', 'card', 'money'])
async def 돈(ctx, *content):
    try:
        if content[0] in sendMoneyCommand:
            await checkUser(ctx, lambda: sendMoney(ctx, content))
    except IndexError:
        await checkUser(ctx, lambda: showMoney(ctx, str(ctx.author.id)))

@bot.command()
async def 보유주식(ctx):
    try:
        await checkUser(ctx, lambda: myStock(ctx, str(ctx.author.id), corpList))
    except:
        
        await raiseError(ctx, '가입 먼저 해주시고 이용해 주세요!')

@bot.command(aliases=['wntlr', 'wt', 'stock'])
async def 주식(ctx, *content):
    try:
        if content[0] in myStockCommand:
            await checkUser(ctx, lambda: myStock(ctx, str(ctx.author.id), corpList))
        elif content[0] in buyStockCommand:
            await checkUser(ctx, lambda: buyStock(ctx, content))
        elif content[0] in sellStockCommand:
            await checkUser(ctx, lambda: sellStock(ctx, content))
        else:
            [name, code, price] = getNowPrice(content[0], corpList)
            if code == None:
                await raiseError(ctx, '%s 은(는) 존재하지 않는 기업입니다. 기업명을 올바르게 입력했는지, 대소문자를 구분하였는지 확인하세요.' % content[0])
            else:
                await ctx.send(embed=discord.Embed(color=0x0090ff, title=":chart_with_upwards_trend: %s(%s)의 현재 주가" % (name, code), description="`%s원`" % format(int(price), ',')).set_image(url='https://ssl.pstatic.net/imgfinance/chart/item/area/day/%s.png?sidcode=%s' % (code, int(time.time() * 1000))).set_footer(text='차트 제공: 네이버 금융'))
    except IndexError:
        await raiseError(ctx, '형식에 맞게 명령어를 입력하세요.\n주가 확인: `%s주식 [기업명]`\n내 주식 확인: `%s주식 내주식`\n구매: `%s주식 구매 [기업명] [수량]`\n판매: `%s주식 판매 [기업명] [수량]`' % (prefix, prefix, prefix))


@bot.command(aliases=['한강물', 'ㅎㄱ', 'ㅎㄱㅁ', 'gksrkd', 'gksrkdanf', 'gr', 'gra'])
async def 한강(ctx):
    request = requests.get('http://hangang.dkserver.wo.tc')
    await ctx.send(embed=discord.Embed(color=0x0067a3, title=':ocean: 현재 한강 수온', description='현재 한강의 수온은 `%s ℃` 입니다.\n\n자살 예방 핫라인 :telephone: 1577-0199\n희망의 전화 :telephone: 129' % literal_eval(request.text[1:])['temp']))


@bot.command(aliases=['돈받기', 'ㄷㅂㄱ', 'eqr'])
async def 용돈(ctx):
    nowtime = time.localtime(time.time())
    if userdata[str(ctx.author.id)]['lastClaim'] == [nowtime.tm_year, nowtime.tm_yday]:
        await raiseError(ctx, '오늘 용돈을 이미 받으셨습니다. 내일 다시 시도하세요.')
    else:
        money = round(random.randrange(200000, 500001), -2)
        userdata[str(ctx.author.id)]['lastClaim'] = [nowtime.tm_year, nowtime.tm_yday]
        userdata[str(ctx.author.id)]['money'] += money
        await ctx.send(embed=discord.Embed(color=0x008000, title=':money_with_wings: 오늘의 용돈', description='오늘 용돈으로 `%s원`을 받았습니다.\n 현재 잔액: `%s원`' % (format(money, ','), format(userdata[str(ctx.author.id)]['money'], ','))))
        updateUserdata()


        
def findDrwNo():
    drwNo = (int(time.time()) - 1038582000) / 604800 # 회차
    nowtime = time.localtime(time.time())
    if nowtime.tm_wday == 5:
        if int(str(nowtime.tm_hour) + str(nowtime.tm_min)) < 2045: # 토요일 20시 45분(로또 추첨 시간) 이전
            return int(drwNo - 1)
    else:
        return int(drwNo)

def getLotto(drwNo):
    return literal_eval(requests.get('https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=' + str(drwNo)).text)



@bot.command(aliases=['복권', 'lotto'])
async def 로또(ctx, *content):
    try:
        if content[0] in buyStockCommand:
            currentDrwNo = findDrwNo() + 1
            currentDrwAmount = 0
            for lottery in userdata[str(ctx.author.id)]['lottery']:
                if lottery['drwNo'] == currentDrwNo:
                    currentDrwAmount += 1
            if currentDrwAmount == 100:
                await ctx.send(embed=discord.Embed(color=0xffff00, title=':warning: 구매 한도 도달', description='회차당 최대 5게임까지 구매 가능합니다.\n\n한국도박문제 관리센터: :telephone: 1336'))
            else:
                if content[1] in lotteryAutoCommand:
                    numbers = []
                    while len(numbers) < 6:
                        queue = random.randint(1, 45)
                        if queue not in numbers:
                            numbers.append(queue)
                else:
                    numbers = []
                    for queue in list(map(int, content[1:7])):
                        if queue in numbers:
                            await raiseError(ctx, '같은 번호를 여러 개 입력하실 수 없습니다.')
                            return
                        elif queue < 1 or queue > 45:
                            await raiseError(ctx, '로또 번호는 1부터 45까지 입력 가능합니다.')
                            return
                        else:
                            numbers.append(queue)
                userdata[str(ctx.author.id)]['lottery'].append({'drwNo': currentDrwNo, 'numbers': numbers})
                userdata[str(ctx.author.id)]['money'] -= 1000
                updateUserdata()
                await ctx.send(embed=discord.Embed(color=0x008000, title=':white_check_mark: 구매 완료', description='로또를 구매했습니다.\n회차: %s회\n번호: **%s %s %s %s %s %s**' % (currentDrwNo, numbers[0], numbers[1], numbers[2], numbers[3], numbers[4], numbers[5])))
        elif content[0] in checkLotteryCommand:
            if len(userdata[str(ctx.author.id)]['lottery']) == 0:
                await raiseError(ctx, '가진 로또가 없습니다.')
            else:
                currentDrwNo = findDrwNo()
                shouldDelete = []
                msg = ':information_source: %s 님이 보유한 로또 목록입니다.' % ctx.author
                for index, lottery in enumerate(userdata[str(ctx.author.id)]['lottery']):
                    correctAmount = 0
                    lotto = getLotto(lottery['drwNo'])
                    if lotto['returnValue'] == 'success':
                        r = requests.post('https://www.dhlottery.co.kr/gameResult.do?method=byWin', data = {'drwNo': lottery['drwNo']})
                        soup = BeautifulSoup(r.text, 'html.parser')
                        money = soup.find_all('td', class_='tar')
                        firstMoney = re.split('<|>', str(money[1]))[2]
                        secondMoney = re.split('<|>', str(money[3]))[2]
                        thirdMoney = re.split('<|>', str(money[5]))[2]
                        shouldDelete.append(index)
                        for i in range(1, 7):
                            if lotto['drwtNo%s' % i] in lottery['numbers']:
                                correctAmount += 1
                        if lotto['bnusNo'] in lottery['numbers']:
                            isBonus = True
                        else:
                            isBonus = False
                        if correctAmount < 3:
                            lottoHead = 'diff\n-'
                            prize = '(낙첨)'
                        else:
                            lottoHead = 'diff\n+'
                            if correctAmount == 3:
                                prize = '(5등, 5,000원)'
                                userdata[str(ctx.author.id)]['money'] += 5000
                            elif correctAmount == 4:
                                prize = '(4등, 50,000원)'
                                userdata[str(ctx.author.id)]['money'] += 50000
                            elif correctAmount == 5 and not isBonus:
                                prize = '(3등, %s)' % thirdMoney
                                userdata[str(ctx.author.id)]['money'] += int(thirdMoney.replace(',', '')[0:-1])
                            elif correctAmount == 5 and isBonus:
                                prize = '(2등, %s)' % secondMoney
                                userdata[str(ctx.author.id)]['money'] += int(secondMoney.replace(',', '')[0:-1])
                            elif correctAmount == 6:
                                prize = '(1등, %s)' % firstMoney
                                userdata[str(ctx.author.id)]['money'] += int(firstMoney.replace(',', '')[0:-1])
                    else:
                        lottoHead = '\n*'
                        prize = '(추첨 전)'
                    msg += '```%s %s회차 | %s %s %s %s %s %s %s```' % (lottoHead, lottery['drwNo'], lottery['numbers'][0], lottery['numbers'][1], lottery['numbers'][2], lottery['numbers'][3], lottery['numbers'][4], lottery['numbers'][5], prize)
                for i in shouldDelete:
                    userdata[str(ctx.author.id)]['lottery'][i] = 'deleted'
                while 'deleted' in userdata[str(ctx.author.id)]['lottery']:
                    userdata[str(ctx.author.id)]['lottery'].remove('deleted')
                updateUserdata()
                await ctx.send(msg)
        elif content[0] in lotteryNumberCommand:
            if content[1] in latestLotteryCommand:
                drwNo = findDrwNo()
            else:
                drwNo = content[1]
            lotto = getLotto(int(drwNo))
            if lotto['returnValue'] == 'success':
                await ctx.send(embed=discord.Embed(color=0x008000, title=':slot_machine: %s회차(%s) 로또 6/45 당첨번호' % (lotto['drwNo'], lotto['drwNoDate']), description='**%s %s %s %s %s %s + %s**\n1등 당첨자 수: %s명\n1등 당첨금: %s원' % (lotto['drwtNo1'], lotto['drwtNo2'], lotto['drwtNo3'], lotto['drwtNo4'], lotto['drwtNo5'], lotto['drwtNo6'], lotto['bnusNo'], format(lotto['firstPrzwnerCo'], ','), format(lotto['firstWinamnt'], ','))))
            else:
                await raiseError(ctx, '아직 추첨이 진행되지 않았습니다.\n정규 추첨 시간: 매주 토요일 오후 8:45분')
    except:
        await raiseError(ctx, '형식에 맞게 명령어를 입력하세요.\n구매: `%s로또 구매 자동/[번호1 번호2 번호3 번호4 번호5 번호6]`\n당첨 확인: `%s로또 확인`\n번호 확인: `%s로또 번호 최신/[회차 번호]`' % (prefix, prefix, prefix))

@bot.command()
async def admin(ctx, *content):
    if ctx.author.id == 324101597368156161 or ctx.author.id == 828515050640637973:
        if content[0] == 'setMoney':
            userdata[content[1]]['money'] = int(content[2])
        elif content[0] == 'addMoney':
            userdata[content[1]]['money'] += int(content[2])
        elif content[0] == 'showStock':
            await (ctx, content[1], corpList)
        elif content[0] == 'showMoney':
            await showMoney(ctx, content[1])
        elif content[0] == 'addStock':
            userdata[content[1]]['stock'][content[2]]['amount'] += int(content[3])
        elif content[0] == 'setStock':
            userdata[content[1]]['stock'][content[2]]['amount'] = int(content[3])
        elif content[0] == 'resetClaim':
            userdata[content[1]]['lastClaim'] = [0, 0]
        elif content[0] == 'shutdown':
            exit()
        updateUserdata()
    else:
        await raiseError(ctx, '운영자가 아닙니다.')


@bot.event
async def raiseError(ctx, msg):
    await ctx.send(embed=discord.Embed(color=0xff0000, title=':warning: 오류', description=msg))


async def checkUser(ctx, ifRegistered, ifNotRegistered=None):
    if str(ctx.author.id) in userdata:
        await ifRegistered()
    elif ifNotRegistered == None:
        await ctx.send(embed=discord.Embed(color=0xff0000, title=':warning: 가입 필요', description='가입이 필요합니다. `%s가입`을 입력해 가입하세요.' % prefix))
    else:
        await ifNotRegistered()


async def register(ctx):
    userdata[str(ctx.author.id)] = {
        'money': 1000000,
        'stock': {},
        'lottery': [],
        'lastClaim': [0, 0]
    }
    updateUserdata()
    await ctx.send(embed=discord.Embed(color=0x008000, title=':white_check_mark: 가입 완료', description='가입이 완료되었습니다.'))


async def sendAlreadyRegisteredMessage(ctx):
    await raiseError(ctx, '이미 가입돼 있습니다.')


async def showMoney(ctx, userID):
    user = await ctx.message.guild.fetch_member(int(userID))
    stock = list(userdata[userID]['stock'].keys())
    stockValue = list(userdata[userID]['stock'].values())
    money = 0
    for i in range(len(userdata[userID]['stock'])):
        price = getNowPrice(stock[i], corpList)[2]
        if price != None:
            money += int(price) * stockValue[i]['amount']
    await ctx.send(embed=discord.Embed(color=0xffff00, title=':moneybag: %s 님의 돈' % user.display_name, description='현금: `%s원`\n주식: `%s원`\n주식 포함 금액: `%s원`' % (format(userdata[userID]['money'], ','), format(money, ','), format(userdata[userID]['money'] + money, ','))))


async def myStock(ctx, userID, df):
    user = await ctx.message.guild.fetch_member(int(userID))
    stock = list(userdata[userID]['stock'].keys())
    stockValue = list(userdata[userID]['stock'].values())
    if len(stock) == 0:
        await raiseError(ctx, '보유한 주식이 없습니다.')
    else:
        willSendMessage = ':information_source: %s 님의 주식 상태입니다.\n' % user.display_name
        for i in range(len(userdata[userID]['stock'])):
            [name, code, price] = getNowPrice(stock[i], corpList)
            if price == None:
                willSendMessage += '```\n* %s(%s): %s주 (평균 구매가 %s원, 현재 거래정지 상태)```' % (name, code, format(int(stockValue[i]['amount']), ',').replace('.0', ''), format(math.floor(stockValue[i]['buyPrice'] / stockValue[i]['amount']), ',').replace('.0', ''))
            elif stockValue[i]['buyPrice'] > stockValue[i]['amount'] * price:
                willSendMessage += '```diff\n- %s(%s): %s주 (평균 구매가 %s원, 현재 %s원)[%s원, -%s%%]```' % (name, code, format(int(stockValue[i]['amount']), ',').replace('.0', ''), format(math.floor(stockValue[i]['buyPrice'] / stockValue[i]['amount']), ',').replace('.0', ''), format(price, ','), format(int(stockValue[i]['amount'] * price - stockValue[i]['buyPrice']), ','), round(float(stockValue[i]['buyPrice']) / float(stockValue[i]['amount'] * price) * 100 - 100, 2))
            elif stockValue[i]['buyPrice'] < stockValue[i]['amount'] * price:
                willSendMessage += '```diff\n+ %s(%s): %s주 (평균 구매가 %s원, 현재 %s원)[+%s원, +%s%%]```' % (name, code, format(int(stockValue[i]['amount']), ',').replace('.0', ''), format(math.floor(stockValue[i]['buyPrice'] / stockValue[i]['amount']), ',').replace('.0', ''), format(price, ','), format(int(stockValue[i]['amount'] * price - stockValue[i]['buyPrice']), ','), round(float(stockValue[i]['amount'] * price) / float(stockValue[i]['buyPrice']) * 100 - 100, 2))
            else:
                willSendMessage += '```yaml\n= %s(%s): %s주 (평균 구매가 %s원, 현재 %s원)[=]```' % (name, code, format(int(stockValue[i]['amount']), ',').replace('.0', ''), format(math.floor(stockValue[i]['buyPrice'] / stockValue[i]['amount']), ',').replace('.0', ''), format(price, ','))
        await ctx.send(willSendMessage)


async def sendMoney(ctx, content):
    try:
        targetUser = content[1].replace('<', '').replace('>', '').replace('@', '').replace('!', '')
        if len(targetUser) == 18:
            if userdata[str(ctx.author.id)]['money'] <= int(content[2]):
                await raiseError(ctx, '잔액이 부족합니다.')
            elif int(content[2]) <= 0:
                await raiseError(ctx, '보낼 금액은 1원 이상이어야 합니다.')
            else:
                await checkUser(ctx, lambda: sendMoney2(ctx, content, targetUser), lambda: ctx.send(embed=discord.Embed(color=0xff0000, name=':warning: 오류', description='받을 상대가 가입되어있지 않습니다.')))
        else:
            raise Exception()
    except:
        await raiseError(ctx, '잘못된 양식입니다.\n양식: `%s돈 송금 <보낼 사람(멘션)> <액수>`' % prefix)


async def sendMoney2(ctx, content, targetUser):
    user = await ctx.message.guild.fetch_member(int(targetUser))
    userdata[str(ctx.author.id)]['money'] += -int(content[2])
    userdata[targetUser]['money'] += int(content[2])
    updateUserdata()
    await ctx.send(embed=discord.Embed(color=0x008000, title=':white_check_mark: 송금 완료', description='%s 님께 송금을 완료했습니다.\n송금 후 잔액: `%s원`' % (user.display_name, userdata[str(ctx.author.id)]['money'])))


async def buyStock(ctx, content):
    success = False
    buyAmount = ''
    try:
        int(content[2])
    except ValueError:
        if content[2] in selectAllCommand:
            [name, code, price] = getNowPrice(content[1], corpList)
            buyAmount = math.floor(
                userdata[str(ctx.author.id)]['money'] / price)
    else:
        buyAmount = content[2]
    finally:
        try:
            [name, code, price] = getNowPrice(content[1], corpList)
            buyPrice = int(buyAmount) * price
            if code == None:
                await raiseError(ctx, '%s 은(는) 존재하지 않는 기업입니다. 기업명을 올바르게 입력했는지, 대소문자를 구분하였는지 확인하세요.' % content[1])
            elif buyPrice <= 0:
                await raiseError(ctx, '수량은 0보다 커야 합니다.')
            elif userdata[str(ctx.author.id)]['money'] < buyPrice:
                await ctx.send(embed=discord.Embed(color=0xffff00, title=':moneybag: 잔액 부족', description='가진 돈이 부족합니다.'))
            else:
                userdata[str(ctx.author.id)]['money'] += -buyPrice
                userdata[str(ctx.author.id)]['stock'][code]['amount'] += int(buyAmount)
                userdata[str(ctx.author.id)]['stock'][code]['buyPrice'] += buyPrice
                success = True
        except ValueError:
            await raiseError(ctx, '수량에는 숫자 또는 전부만 입력하세요.\n형식: `%s주식 구매 <기업명/종목코드> <수량/전부>`' % config['prefix'])
        except KeyError:
            userdata[str(ctx.author.id)]['stock'][code] = {
                'amount': int(buyAmount),
                'buyPrice': buyPrice
            }
            success = True
        finally:
            if success == True:
                updateUserdata()
                await ctx.send(embed=discord.Embed(color=0x008000, title=':white_check_mark: 구매 완료', description='%s(%s) 주식을 구매했습니다.\n구매 금액: `%s × %s = %s원`\n보유 중인 주식: `%s주`\n남은 돈: `%s원`' % (name, code, format(int(price), ','), format(int(buyAmount), ','), format(int(price) * int(buyAmount), ','), format(userdata[str(ctx.author.id)]['stock'][code]['amount'], ','), format(userdata[str(ctx.author.id)]['money'], ','))))


async def sellStock(ctx, content):
    sellAmount = ''
    try:
        int(content[2])
    except ValueError:
        if content[2] in selectAllCommand:
            code = getNowPrice(content[1], corpList)[1]
            sellAmount = userdata[str(ctx.author.id)]['stock'][code]['amount']
    else:
        sellAmount = content[2]
    finally:
        try:
            [name, code, price] = getNowPrice(content[1], corpList)
            if code == None:
                await raiseError(ctx, '%s 은(는) 존재하지 않는 기업입니다. 기업명을 올바르게 입력했는지, 대소문자를 구분하였는지 확인하세요.' % content[1])
            elif userdata[str(ctx.author.id)]['stock'][code]['amount'] < int(sellAmount):
                await raiseError(ctx, '가진 주식보다 많이 판매할 수 없습니다.')
            elif int(sellAmount) <= 0:
                await raiseError(ctx, '수량은 0보다 커야 합니다.')
            else:
                userdata[str(ctx.author.id)]['stock'][code]['amount'] += -int(sellAmount)
                userdata[str(ctx.author.id)]['stock'][code]['buyPrice'] += - \
                    (int(sellAmount) * price)
                amount = userdata[str(ctx.author.id)]['stock'][code]['amount']
                if userdata[str(ctx.author.id)]['stock'][code]['amount'] == 0:
                    del userdata[str(ctx.author.id)]['stock'][code]
                    amount = 0
                userdata[str(ctx.author.id)
                         ]['money'] += int(sellAmount) * price
                updateUserdata()
                await ctx.send(embed=discord.Embed(color=0x008000, title=':white_check_mark: 판매 완료', description='%s(%s) 주식을 판매했습니다.\n판매 금액: `%s × %s = %s원`\n보유 중인 주식: `%s주`\n남은 돈: `%s원`' % (name, code, format(int(price), ','), format(int(sellAmount), ','), format(int(price) * int(sellAmount), ','), format(amount, ','), format(userdata[str(ctx.author.id)]['money'], ','))))
        except KeyError:
            await raiseError(ctx, '%s(%s)의 주식을 가지고 있지 않습니다.' % (name, code))
        except ValueError as e:
            print(e)
            await raiseError(ctx, '수량에는 숫자 또는 전부만 입력하세요.\n형식: `%s주식 판매 <기업명/종목코드> <수량/전부>`' % config['prefix'])
        except IndexError:
            await raiseError(ctx, '값을 입력하세요.\n형식: `%s주식 판매 <기업명/종목코드> <수량/전부>`' % config['prefix'])


def updateUserdata():
    with open('./userdata.json', 'w') as json_file:
        json.dump(userdata, json_file, indent=4)


# Initialize
corpList = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0][['회사명', '종목코드']]


    
    """


        
        
    

            

bot.run(access_token)
