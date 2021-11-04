import discord 
from discord.ext import commands
from discord_buttons_plugin import  *
from youtube_dl import YoutubeDL
from bs4 import BeautifulSoup
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time
import requests
import os
import discord_fortuneTell

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
    
    if not discord.opus.is_loaded():
        discord.opus.load_opus('opus')
    
@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title = "음악한곡", description = "유튜브 라이센스를 사용합니다.", color = 0x6E17E3) 
    embed.add_field(name = bot.command_prefix + "도움", value = "명령어를 볼수 있습니다,", inline = False)
    embed.add_field(name = bot.command_prefix + "들어와", value = "뮤직봇이 음성채널에 들어갑니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "나가", value = "뮤직봇이 채널에서 나갑니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "재생 [노래 이름]  [작곡가] ", value = "유튜브검색기능을 활용하여 찾아드립니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "목록", value = "자신의 플레이 리스트를 볼수있습니다", inline = False)
    embed.add_field(name = bot.command_prefix + "목록초기화", value = "목록에 있는 모든 대기열들 삭제합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "대기열추가 [노래 이름] [작곡가]", value = "음악이 목록에 추가됩니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "대기열삭제 [대기열 번호]", value = "대기열에 있는 목록이 삭제됩니다..", inline = False)
    embed.add_field(name = bot.command_prefix + "차트", value = "멜론 차트순위 1~10위까지의 노래를 가져옵니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "가사 [노래이름]", value = "노래재목과 유사한 노래 1~5개 까지의 리스트를 뽑아옵니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "선택 [번호]", value = "선택된 노래의 가사를 가져옵니다.", inline = False)
    embed.add_field(name = bot.command_prefix + "즐겨찾기 [추가, 삭제]", value = "즐겨찾기한 노래의 목록을 볼수 있습니다 [추가할수 있습니다] [삭제할수 있습니다]", inline = False)
    
    
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

        #드라이버 닫기

        driver.quit()

        musicnow.insert(0, entireText)

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: play_next(ctx))
    else:
        user.append(msg)
        result,URLTEST = title(msg)
        song_queue.append(URLTEST)
        await ctx.send("이미 노래가 재생 중이라" + result + "을(를) 대기열로 추가시켰습니다")
        

        
@bot.command()
async def 스킵(ctx):
    if len(user) > 1:
        if vc.is_playing():
            vc.stop()
            global number
            number = 0
            await ctx.send(embed = discord.Embed(title = "스킵", description = musicnow[1] + "을(를) 다음에 재생합니다!", color = 0x00ff00))
        else:
            await ctx.send("노래가 이미 재생되고 있어요!")
    else:
        await ctx.send("목록에 노래가 2개 이상 없네요..")
        

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
async def 멜론차트(ctx):
    if not vc.is_playing():
        
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        driver = load_chrome_driver()
        driver.get("https://www.youtube.com/results?search_query=멜론차트")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        driver.quit()

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + entireText + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없어요!")

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
    await ctx.send(embed = discord.Embed(title= "반복재생", description = "현재 " + musicnow[0] + "을(를) 반복재생하고 있습니다.", color = 0x00ff00))
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
    await ctx.send(discord_fortuneTell.out(args))


    
    
@bot.command()
async def 추천곡(ctx):
    global mum
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    

    driver = load_chrome_driver()

    driver.get('https://www.music-flo.com/')
    time.sleep(1)

    html = driver.page_source
    parse = BeautifulSoup(html, 'html.parser')

    music = parse.select_one('#main > div > section.section_content_wrap.personal > div.section_content.swiper_horizon.PERSONAL_swiper_container.swiper-container-initialized.swiper-container-horizontal > ul > li.swiper-slide.type_theme.swiper-slide-active > a > div.personal_recommend_head > h4').get_text()
    

    embed = discord.Embed(title=f" <{ctx.author.name}>님을 위한 추천곡이에요.", description=music, color=0xAAFFFF)

    rn = random.randint(1, 4)
    print(rn)
    
    

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






        
        
    

            
access_token = os.environ["BOT_TOKEN"] 

bot.run(access_token)
