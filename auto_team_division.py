import re
from unittest import result
import discord
import random
from create_table import create_table
import json

intents = discord.Intents.default()
client = discord.Client(intents=intents)
TOKEN = 'OTk0ODg2ODE1NzgzODUwMDA0.G9ac-s.5vhWxzN4OVvmsUGqUkZii438oM7oaza5-Uckqk'


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    # /division --without @れふてぃ
    # 送信者がbotかの判断
    if message.author.bot:
        return

    commands = message.content.split()

    if "/help" in commands:
        with open('help.txt', 'r', encoding='UTF-8') as f:
            await message.channel.send(f.read())
    # ランク登録
    # /register IR1 BR1 SI1 GO1 PL1 DI1
    if "/register" in commands:
        input = commands[1]
        ranks = ["IR", "BR", "SI", "GO", "PL", "DI"]
        num = ["4", "3", "2", "1"]
        # 入力確認
        if input[0:2] in ranks and input[2] in num:
            rate = ranks.index(input[0:2]) * 4 + num.index(input[2])
            # データ登録
            members = []
            with open('members.json', 'r', encoding="UTF-8") as f:
                members = json.load(f)
            with open('members.json', 'w', encoding="UTF-8") as f:
                members = [i for i in members if i['name'] != message.author.name]
                members.append({
                    "name": message.author.name,
                    "rank": input,
                    "rate": rate,
                })
                f.write(json.dumps(members, indent=2, ensure_ascii=False))

            # 表示
            await message.channel.send(f"@{message.author.name}さんが`{commands[1]}`で登録されました")
        else:
            await message.channel.send("不正な入力です")

    if "/debug" in commands:
        members = [
            "れふてぃ", "SKS", "unpichan", "セツ", "rolence", "タニタ食道",
            "あぶきーる", "CronoA", "Xtushi.N*", "Alreina（リーズ）"
        ]
        diff_rate_setting = 8
        if "--rate" in commands:
            data = commands[commands.index("--rate") + 1]
            diff_rate_setting = int(data)

        # 画像の作成
        members, diff_rate = balancer(members, diff_rate_setting)
        create_table(members)
        # チーム分け結果の送信
        await message.channel.send(
            f"レート設定は**{diff_rate_setting}**、レート差は**{diff_rate}**です",
            file=discord.File("./team.png")
        )

    if "/showMembers" in commands:
        with open('members.json', 'r', encoding="UTF-8") as f:
            members = json.load(f)
            result = ""
            for member in members:
                result += f"@{member['name']}: `{member['rank']}`\n"
            await message.channel.send(result)

    if "/division" in commands:
        # 送信者がVCにいるかどうか
        if message.author.voice != None:
            # ボイスチャンネルにいるメンバーのリストを取得
            members = [i.name for i in message.author.voice.channel.members]
            without_members = []
            # without_members の検出
            if message.content.find('--without'):
                if message.mentions:
                    without_members = [mention.name for mention in message.mentions]
            # without_membersの削除
            members = [mem for mem in members if mem not in without_members]
            # 配列のシャッフル
            # random.shuffle(members)
            if len(members) == 10:
                diff_rate_setting = 8
                if "--rate" in commands:
                    data = commands[commands.index("--rate") + 1]
                    diff_rate_setting = int(data)
                # 画像の作成
                members, diff_rate = balancer(members, diff_rate_setting)
                create_table(members)
                # チーム分け結果の送信
                await message.channel.send(
                    f"レート設定は**{diff_rate_setting}**、レート差は**{diff_rate}**です",
                    file=discord.File("./team.png")
                )
            else:
                msg = f'メンバーが10人でありません。[現在、{len(members)}人]\n'\
                    "もしくは、BOTがメンバーを読み込めていない可能性があります。\n"\
                    "一度全員、別の部屋に入り直して実行してみてください。"
                await message.channel.send(msg)
        else:
            await message.channel.send('あなたはボイスチャンネルにいないようです...')


def balancer(members_only_name, diff_rate_setting):
    with open('members.json', 'r', encoding="UTF-8") as f:
        members_data = json.load(f)
        members = []
        random.shuffle(members_only_name)
        for name in members_only_name:
            flag = False
            for member_data in members_data:
                if name in member_data['name']:
                    members.append(member_data)
                    flag = True
                    break
            if not flag:
                members.append({
                    "name": name,
                    "rank": "SI2",
                    "rate": 10,
                })

        red_team = []
        blue_team = []
        for index, member in enumerate(members):
            if index % 2 == 0:
                red_team.append(member)
            else:
                blue_team.append(member)

        print(f"rate: {abs(get_sum_rate(red_team) - get_sum_rate(blue_team))}")
        diff_rate = abs(get_sum_rate(red_team) - get_sum_rate(blue_team))
        if abs(get_sum_rate(red_team) - get_sum_rate(blue_team)) > diff_rate_setting:
            return balancer(members_only_name, diff_rate_setting)

        result = []
        for index in range(5):
            result.append(red_team[index])
            result.append(blue_team[index])

        return result, diff_rate


def get_sum_rate(members):
    sum = 0
    for member in members:
        sum += member['rate']
    return sum


client.run(TOKEN)
