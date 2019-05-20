# -*- coding: utf-8 -*-
# encoding=utf8
import sys
import json
import re
from Crypto.Cipher import AES
import base64
import binascii

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import random
import requests
import os
import time
import datetime


class AESCipher:
    def __init__(self, key):
        self.key = key
        self.block_size = 16

    def encrypt(self, raw):
        raw = self.addpad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        #

        cipher = AES.new(self.key, AES.MODE_ECB)
        return self.strippad(cipher.decrypt(enc))

    def strippad(self, text):
        nl = len(text)
        te = str(text[-1])
        te = te.encode("latin-1")
        val = int(te)
        # val = int(binascii.hexlify(te), 16)
        if val > self.block_size:
            raise ValueError('Input is not padded or padding is corrupt')
        l = nl - val
        return text[:l]

    def addpad(self, text):
        l = len(text)
        output = StringIO()
        val = self.block_size - (l % self.block_size)
        for _ in range(val):
            output.write('%02x' % val)
        return text + binascii.unhexlify(output.getvalue())


def getymd():
    return datetime.datetime.fromtimestamp(int(time.time())).strftime("%Y%m%d")


def getymdt():
    return datetime.datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %X")


Unit_Name_Dict_Lookup = {'100000102': 'Rain - 2*', '100000103': 'Rain - 3*', '100000104': 'Rain - 4*',
                         '100000105': 'Rain - 5*', '100000202': 'Lasswell - 2*', '100000203': 'Lasswell - 3*',
                         '100000204': 'Lasswell - 4*', '100000205': 'Lasswell - 5*', '100000302': 'Fina - 2*',
                         '100000303': 'Fina - 3*', '100000304': 'Fina - 4*', '100000305': 'Fina - 5*',
                         '100000901': 'Rizer', '100000902': 'Rizer - 2*', '100001001': 'Leah', '100001002': 'Leah - 2*',
                         '100001101': 'Tronn', '100001102': 'Tronn - 2*', '100001201': 'Eldin',
                         '100001202': 'Eldin - 2*', '100001301': 'Baurg', '100001302': 'Baurg - 2*',
                         '100001401': 'Gimlee', '100001402': 'Gimlee - 2*', '100001501': 'Maxell',
                         '100001502': 'Maxell - 2*', '100001601': 'Liza', '100001602': 'Liza - 2*',
                         '206001502': 'Wedge - 2*', '206001503': 'Wedge - 3*', '206001602': 'Biggs - 2*',
                         '206001603': 'Biggs - 3*', '202001402': 'Paul - 2*', '202001403': 'Paul - 3*',
                         '212000702': 'Anastasis - 2*', '212000703': 'Anastasis - 3*', '201000302': 'Sarah - 2*',
                         '201000303': 'Sarah - 3*', '204001302': 'King Giott - 2*', '204001303': 'King Giott - 3*',
                         '100001702': 'Shiki - 2*', '100001703': 'Shiki - 3*', '100001802': 'Mizell - 2*',
                         '100001803': 'Mizell - 3*', '100001902': 'Ronaldo - 2*', '100001903': 'Ronaldo - 3*',
                         '100002002': 'Mel - 2*', '100002003': 'Mel - 3*', '209000203': 'Vivi - 3*',
                         '209000204': 'Vivi - 4*', '212000403': 'Penelo - 3*', '212000404': 'Penelo - 4*',
                         '202000203': 'Maria - 3*', '202000204': 'Maria - 4*', '206000403': 'Sabin - 3*',
                         '206000404': 'Sabin - 4*', '206000503': 'Shadow - 3*', '206000504': 'Shadow - 4*',
                         '205000503': 'Krile - 3*', '205000504': 'Krile - 4*', '204000203': 'Kain - 3*',
                         '204000204': 'Kain - 4*', '206000303': 'Edgar - 3*', '206000304': 'Edgar - 4*',
                         '212000603': 'Fran - 3*', '212000604': 'Fran - 4*', '211000103': 'Shantotto - 3*',
                         '211000104': 'Shantotto - 4*', '204000403': 'Rydia - 3*', '204000404': 'Rydia - 4*',
                         '206000603': 'Cyan - 3*', '206000604': 'Cyan - 4*', '100002103': 'Clyne - 3*',
                         '100002104': 'Clyne - 4*', '100002203': 'Anzelm - 3*', '100002204': 'Anzelm - 4*',
                         '100002303': 'Luna - 3*', '100002304': 'Luna - 4*', '100002403': 'Bedile - 3*',
                         '100002404': 'Bedile - 4*', '201000203': 'Garland - 3*', '201000204': 'Garland - 4*',
                         '201000205': 'Garland - 5*', '205000703': 'Exdeath - 3*', '205000704': 'Exdeath - 4*',
                         '205000705': 'Exdeath - 5*', '209001003': 'Kuja - 3*', '209001004': 'Kuja - 4*',
                         '209001005': 'Kuja - 5*', '203000803': 'Cloud of Darkness - 3*',
                         '203000804': 'Cloud of Darkness - 4*', '203000805': 'Cloud of Darkness - 5*',
                         '204000103': 'Cecil - 3*', '204000104': 'Cecil - 4*', '204000105': 'Cecil - 5*',
                         '206000103': 'Terra - 3*', '206000104': 'Terra - 4*', '206000105': 'Terra - 5*',
                         '206000113': 'Magitek Armor Terra - 3*', '206000114': 'Magitek Armor Terra - 4*',
                         '205000103': 'Bartz - 3*', '205000104': 'Bartz - 4*', '205000105': 'Bartz - 5*',
                         '202000103': 'Firion - 3*', '202000104': 'Firion - 4*', '202000105': 'Firion - 5*',
                         '209000103': 'Zidane - 3*', '209000104': 'Zidane - 4*', '209000105': 'Zidane - 5*',
                         '212000103': 'Vaan - 3*', '212000104': 'Vaan - 4*', '212000105': 'Vaan - 5*',
                         '100002503': 'Duane - 3*', '100002504': 'Duane - 4*', '100002505': 'Duane - 5*',
                         '100002603': 'Cerius - 3*', '100002604': 'Cerius - 4*', '100002605': 'Cerius - 5*',
                         '100002703': 'Roselia - 3*', '100002704': 'Roselia - 4*', '100002705': 'Roselia - 5*',
                         '100002803': 'Medius - 3*', '100002804': 'Medius - 4*', '100002805': 'Medius - 5*',
                         '100002901': 'Sarai', '100002902': 'Sarai - 2*', '100003002': 'Paula - 2*',
                         '100003003': 'Paula - 3*', '100003202': 'Kenyu - 2*', '100003203': 'Kenyu - 3*',
                         '100003302': 'Ollie - 2*', '100003303': 'Ollie - 3*', '100003402': 'Carrie - 2*',
                         '100003403': 'Carrie - 3*', '100003502': 'Skaha - 2*', '100003503': 'Skaha - 3*',
                         '100003602': 'Montana - 2*', '100003603': 'Montana - 3*', '100003703': 'Russell - 3*',
                         '100003704': 'Russell - 4*', '100003803': 'Miyuki - 3*', '100003804': 'Miyuki - 4*',
                         '100003805': 'Miyuki - 5*', '204001403': 'Golbez - 3*', '204001404': 'Golbez - 4*',
                         '204001405': 'Golbez - 5*', '205000303': 'Galuf - 3*', '205000304': 'Galuf - 4*',
                         '100004003': 'Xiao - 3*', '100004004': 'Xiao - 4*', '100004005': 'Xiao - 5*',
                         '900020101': 'Metal Minituar', '900020201': 'Metal Cactuar', '900020301': 'Metal Gigantuar',
                         '199000101': 'Emma (Battle NPC)', '100004403': 'Artemios - 3*', '100004404': 'Artemios - 4*',
                         '100004405': 'Artemios - 5*', '206000203': 'Locke - 3*', '206000204': 'Locke - 4*',
                         '206000205': 'Locke - 5*', '206001803': 'Leo - 3*', '206001804': 'Leo - 4*',
                         '206001805': 'Leo - 5*', '900010101': 'Mini Gil Snapper', '900010201': 'Gil Snapper',
                         '900010301': 'King Gil Snapper', '100003903': 'Gilbert - 3*', '100003904': 'Gilbert - 4*',
                         '100003905': 'Gilbert - 5*', '206000703': 'Celes - 3*', '206000704': 'Celes - 4*',
                         '206000705': 'Celes - 5*', '206001703': 'Kefka - 3*', '206001704': 'Kefka - 4*',
                         '206001705': 'Kefka - 5*', '301000103': 'Samatha - 3*', '301000104': 'Samatha - 4*',
                         '199000102': 'Lid - 2*', '100004103': 'Rakshasa - 3*', '100004104': 'Rakshasa - 4*',
                         '100004105': 'Rakshasa - 5*', '100004604': 'Chizuru - 4*', '100004605': 'Chizuru - 5*',
                         '100004703': 'Hayate - 3*', '100004704': 'Hayate - 4*', '100004705': 'Hayate - 5*',
                         '201000104': 'Warrior of Light - 4*', '201000105': 'Warrior of Light - 5*',
                         '204000503': 'Tellah - 3*', '204000504': 'Tellah - 4*', '204000505': 'Tellah - 5*',
                         '205000203': 'Lenna - 3*', '205000204': 'Lenna - 4*', '205000205': 'Lenna - 5*',
                         '209000304': 'Garnet - 4*', '209000305': 'Garnet - 5*', '209000503': 'Freya - 3*',
                         '209000504': 'Freya - 4*', '209000505': 'Freya - 5*', '209000803': 'Amarant - 3*',
                         '209000804': 'Amarant - 4*', '209000805': 'Amarant - 5*', '209000903': 'Lani - 3*',
                         '209000904': 'Lani - 4*', '100000503': 'Lid - 3*', '100000504': 'Lid - 4*',
                         '100000505': 'Lid - 5*', '100004203': 'Ludmille - 3*', '100004204': 'Ludmille - 4*',
                         '100004205': 'Ludmille - 5*', '100004303': 'Charlotte - 3*', '100004304': 'Charlotte - 4*',
                         '100004305': 'Charlotte - 5*', '213000105': 'Lightning - 5*', '213000106': 'Lightning - 6*',
                         '253000105': 'Ramza - 5*', '253000106': 'Ramza - 6*', '253000205': 'Delita - 5*',
                         '253000206': 'Delita - 6*', '253000304': 'Agrias - 4*', '253000305': 'Agrias - 5*',
                         '253000403': 'Alma - 3*', '253000404': 'Alma - 4*', '253000405': 'Alma - 5*',
                         '253000504': 'Gaffgarion - 4*', '253000505': 'Gaffgarion - 5*', '253000603': 'Mustadio - 3*',
                         '253000604': 'Mustadio - 4*', '253000605': 'Mustadio - 5*', '213000204': 'Snow - 4*',
                         '213000205': 'Snow - 5*', '213000206': 'Snow - 6*', '213000304': 'Vanille - 4*',
                         '213000305': 'Vanille - 5*', '213000403': 'Sazh - 3*', '213000404': 'Sazh - 4*',
                         '213000405': 'Sazh - 5*', '213000504': 'Hope - 4*', '213000505': 'Hope - 5*',
                         '213000603': 'Fang - 3*', '213000604': 'Fang - 4*', '213000605': 'Fang - 5*',
                         '255000104': 'Juggler - 4*', '255000105': 'Juggler - 5*', '255000204': 'Thief - 4*',
                         '255000205': 'Thief - 5*', '255000304': 'Fencer - 4*', '255000305': 'Fencer - 5*',
                         '204000304': 'Rosa - 4*', '204000305': 'Rosa - 5*', '204000115': 'Dark Knight Cecil - 5*',
                         '204000116': 'Dark Knight Cecil - 6*', '204001103': 'Edge - 3*', '204001104': 'Edge - 4*',
                         '204001105': 'Edge - 5*', '204000106': 'Cecil - 6*', '204000405': 'Rydia - 5*',
                         '204000205': 'Kain - 5*', '904000105': 'Trust Moogle - 5*', '905000102': 'Mini Burst Pot - 2*',
                         '303000103': 'Adel - 3*', '303000104': 'Adel - 4*', '302000104': 'Tilith - 4*',
                         '302000105': 'Tilith - 5*', '302000204': 'Karl - 4*', '302000205': 'Karl - 5*',
                         '302000304': 'Seria - 4*', '302000305': 'Seria - 5*', '100000403': 'Nichol - 3*',
                         '100000404': 'Nichol - 4*', '100000405': 'Nichol - 5*', '254000105': 'Ace - 5*',
                         '254000106': 'Ace - 6*', '254000403': 'Trey - 3*', '254000404': 'Trey - 4*',
                         '254000405': 'Trey - 5*', '254000603': 'Jack - 3*', '254000604': 'Jack - 4*',
                         '254000605': 'Jack - 5*', '254000704': 'Seven - 4*', '254000705': 'Seven - 5*',
                         '254000706': 'Seven - 6*', '203000205': 'Luneth - 5*', '203000206': 'Luneth - 6*',
                         '203000303': 'Arc - 3*', '203000304': 'Arc - 4*', '203000305': 'Arc - 5*',
                         '203000404': 'Refia - 4*', '203000405': 'Refia - 5*', '203000406': 'Refia - 6*',
                         '203000503': 'Ingus - 3*', '203000504': 'Ingus - 4*', '203000505': 'Ingus - 5*',
                         '203000806': 'Cloud of Darkness - 6*', '304000105': 'Randi - 5*', '304000106': 'Randi - 6*',
                         '304000204': 'Primm - 4*', '304000205': 'Primm - 5*', '304000206': 'Primm - 6*',
                         '304000303': 'Popoi - 3*', '304000304': 'Popoi - 4*', '304000305': 'Popoi - 5*',
                         '904000103': 'Trust Moogle - 3*', '904000104': 'Trust Moogle - 4*',
                         '905000103': 'Burst Pot - 3*', '905000104': 'King Burst Pot - 4*',
                         '900000101': 'Mini Tough Pot', '900000201': 'Tough Pot', '900000301': 'King Tough Pot',
                         '900001101': 'Mini Magi Pot', '900001201': 'Magi Pot', '900001301': 'King Magi Pot',
                         '900002101': 'Mini Power Pot', '900002201': 'Power Pot', '900002301': 'King Power Pot',
                         '900003101': 'Mini Shield Pot', '900003201': 'Shield Pot', '900003301': 'King Shield Pot',
                         '900004101': 'Mini Smart Pot', '900004201': 'Smart Pot', '900004301': 'King Smart Pot',
                         '900005101': 'Mini Soul Pot', '900005201': 'Soul Pot', '900005301': 'King Soul Pot',
                         '205000403': 'Faris - 3*', '205000404': 'Faris - 4*', '205000405': 'Faris - 5*',
                         '205000805': 'Gilgamesh - 5*', '205000806': 'Gilgamesh - 6*', '100005104': 'Mercedes - 4*',
                         '100005105': 'Mercedes - 5*', '100005106': 'Mercedes - 6*', '205000106': 'Bartz - 6*',
                         '205000706': 'Exdeath - 6*', '205000505': 'Krile - 5*', '205000305': 'Galuf - 5*',
                         '254000205': 'Queen - 5*', '254000206': 'Queen - 6*', '254000304': 'Nine - 4*',
                         '254000305': 'Nine - 5*', '254000306': 'Nine - 6*', '254000503': 'Cinque - 3*',
                         '254000504': 'Cinque - 4*', '254000505': 'Cinque - 5*', '254001003': 'Eight - 3*',
                         '254001004': 'Eight - 4*', '254001005': 'Eight - 5*', '100000106': 'Rain - 6*',
                         '100004606': 'Chizuru - 6*', '100000315': 'Dark Fina - 5*', '100000316': 'Dark Fina - 6*',
                         '100004903': 'Elle - 3*', '100004904': 'Elle - 4*', '100004905': 'Elle - 5*',
                         '100005004': 'Luka - 4*', '100005005': 'Luka - 5*', '100005006': 'Luka - 6*',
                         '302000106': 'Tilith - 6*', '302000505': 'Maxwell - 5*', '302000506': 'Maxwell - 6*',
                         '401000205': 'Demon Rain - 5*', '401000206': 'Demon Rain - 6*',
                         '401000305': 'Dracu Lasswell - 5*', '401000306': 'Dracu Lasswell - 6*',
                         '401000404': 'White Witch Fina - 4*', '401000405': 'White Witch Fina - 5*',
                         '401000406': 'White Witch Fina - 6*', '401000503': 'Black Cat Lid - 3*',
                         '401000504': 'Black Cat Lid - 4*', '401000505': 'Black Cat Lid - 5*', '302000605': 'Elza - 5*',
                         '302000606': 'Elza - 6*', '100000703': 'Jake - 3*', '100000704': 'Jake - 4*',
                         '100000705': 'Jake - 5*', '253000805': 'Orlandeau - 5*', '253000806': 'Orlandeau - 6*',
                         '253001103': 'Ovelia - 3*', '253001104': 'Ovelia - 4*', '253001105': 'Ovelia - 5*',
                         '100005304': 'Soleil - 4*', '100005305': 'Soleil - 5*', '100005306': 'Soleil - 6*',
                         '100005203': 'Lawrence - 3*', '100005204': 'Lawrence - 4*', '100005205': 'Lawrence - 5*',
                         '202000106': 'Firion - 6*', '202000205': 'Maria - 5*', '100005404': 'Shine - 4*',
                         '100005405': 'Shine - 5*', '100005406': 'Shine - 6*', '100005503': 'Shera - 3*',
                         '100005504': 'Shera - 4*', '100005505': 'Shera - 5*', '100005805': 'Marie - 5*',
                         '100005806': 'Marie - 6*', '202000303': 'Guy - 3*', '202000304': 'Guy - 4*',
                         '202000305': 'Guy - 5*', '202000404': 'Leon - 4*', '202000405': 'Leon - 5*',
                         '202000505': 'Emperor - 5*', '202000506': 'Emperor - 6*', '100000206': 'Lasswell - 6*',
                         '306000105': 'Dragonlord - 5*', '306000106': 'Dragonlord - 6*',
                         '306000404': 'Killing Machine - 4*', '306000405': 'Killing Machine - 5*',
                         '306000603': 'Slime - 3*', '306000604': 'Slime - 4*', '306000605': 'Slime - 5*',
                         '306000503': 'Golem - 3*', '306000504': 'Golem - 4*', '306000505': 'Golem - 5*',
                         '306000204': 'Orochi - 4*', '306000205': 'Orochi - 5*', '306000206': 'Orochi - 6*',
                         '306000804': 'Liquid Metal Slime - 4*', '306000805': 'Liquid Metal Slime - 5*',
                         '306000303': 'Robbin' 'Ood - 3*', '306000304': 'Robbin' 'Ood - 4*',
                         '306000305': 'Robbin' 'Ood - 5*', '201000106': 'Warrior of Light - 6*',
                         '201000206': 'Garland - 6*', '100005604': 'Sozhe - 4*', '100005605': 'Sozhe - 5*',
                         '100005606': 'Sozhe - 6*', '100005703': 'Heltich - 3*', '100005704': 'Heltich - 4*',
                         '100005705': 'Heltich - 5*', '100005905': 'Aileen - 5*', '100005906': 'Aileen - 6*',
                         '100006003': 'Ulrica - 3*', '100006004': 'Ulrica - 4*', '100006005': 'Ulrica - 5*',
                         '254000905': 'Rem - 5*', '254000906': 'Rem - 6*', '254001204': 'King - 4*',
                         '254001205': 'King - 5*', '254001206': 'King - 6*', '254001403': 'Sice - 3*',
                         '254001404': 'Sice - 4*', '254001405': 'Sice - 5*', '100000603': 'Sakura - 3*',
                         '100000604': 'Sakura - 4*', '100000605': 'Sakura - 5*', '210000105': 'Tidus - 5*',
                         '210000106': 'Tidus - 6*', '100006105': 'Wilhelm - 5*', '100006106': 'Wilhelm - 6*',
                         '100006204': 'Grace - 4*', '100006205': 'Grace - 5*', '100006206': 'Grace - 6*',
                         '100006303': 'Abel - 3*', '100006304': 'Abel - 4*', '100006305': 'Abel - 5*',
                         '100006503': 'Jean - 3*', '100006504': 'Jean - 4*', '100006505': 'Jean - 5*',
                         '302000405': 'Vargas - 5*', '302000406': 'Vargas - 6*', '214000105': 'Y\'shtola - 5*',
                         '214000106': 'Y\'shtola - 6*', '214000203': 'Thancred - 3*', '214000204': 'Thancred - 4*',
                         '214000205': 'Thancred - 5*', '214000304': 'Minfilia - 4*', '214000305': 'Minfilia - 5*',
                         '214000306': 'Minfilia - 6*', '100007104': 'Beach Time Fina - 4*',
                         '100007105': 'Beach Time Fina - 5*', '100007106': 'Beach Time Fina - 6*',
                         '100007205': 'Seabreeze Dark Fina - 5*', '100007206': 'Seabreeze Dark Fina - 6*',
                         '100007303': 'Summer Lid - 3*', '100007304': 'Summer Lid - 4*', '100007305': 'Summer Lid - 5*',
                         '206000106': 'Terra - 6*', '206001706': 'Kefka - 6*', '206000125': 'Trance Terra - 5*',
                         '206000126': 'Trance Terra - 6*', '206000804': 'Setzer - 4*', '206000805': 'Setzer - 5*',
                         '206000806': 'Setzer - 6*', '206001103': 'Gau - 3*', '206001104': 'Gau - 4*',
                         '206001105': 'Gau - 5*', '900020401': 'King Metal Minituar', '900010401': 'Gil Snapper Family',
                         '100006805': 'Fohlen - 5*', '100006806': 'Fohlen - 6*', '100007004': 'Amelia - 4*',
                         '100007005': 'Amelia - 5*', '100007006': 'Amelia - 6*', '100006704': 'Ilias - 4*',
                         '100006705': 'Ilias - 5*', '100006706': 'Ilias - 6*', '100006603': 'Camille - 3*',
                         '100006604': 'Camille - 4*', '100006605': 'Camille - 5*', '210000704': 'Rikku - 4*',
                         '210000705': 'Rikku - 5*', '210000706': 'Rikku - 6*', '210000303': 'Wakka - 3*',
                         '210000304': 'Wakka - 4*', '210000305': 'Wakka - 5*', '212000505': 'Balthier - 5*',
                         '212000506': 'Balthier - 6*', '212000204': 'Ashe - 4*', '212000205': 'Ashe - 5*',
                         '212000206': 'Ashe - 6*', '212001004': 'Rasler - 4*', '212001005': 'Rasler - 5*',
                         '212001006': 'Rasler - 6*', '212000106': 'Vaan - 6*', '212000405': 'Penelo - 5*',
                         '100007505': 'Lunera - 5*', '100007506': 'Lunera - 6*', '100007404': 'Bran - 4*',
                         '100007405': 'Bran - 5*', '100007406': 'Bran - 6*', '100008504': 'Helena - 4*',
                         '100008505': 'Helena - 5*', '100008506': 'Helena - 6*', '100007603': 'Ruggles - 3*',
                         '100007604': 'Ruggles - 4*', '100007605': 'Ruggles - 5*',
                         '302000705': 'White Knight Noel - 5*', '302000706': 'White Knight Noel - 6*',
                         '302000804': 'Santa Roselia - 4*', '302000805': 'Santa Roselia - 5*',
                         '302000806': 'Santa Roselia - 6*', '100002606': 'Cerius - 6*', '100002806': 'Medius - 6*',
                         '215000105': 'Noctis - 5*', '215000106': 'Noctis - 6*', '401000104': 'Dangerous Ariana - 4*',
                         '401000105': 'Dangerous Ariana - 5*', '401000106': 'Dangerous Ariana - 6*',
                         '302000905': 'Yun - 5*', '302000906': 'Yun - 6*', '302001004': 'Ling - 4*',
                         '302001005': 'Ling - 5*', '302001006': 'Ling - 6*', '100004006': 'Xiao - 6*',
                         '211000105': 'Shantotto - 5*', '211000204': 'Werei - 4*', '211000205': 'Werei - 5*',
                         '211000206': 'Werei - 6*', '211000303': 'Kupipi - 3*', '211000304': 'Kupipi - 4*',
                         '211000305': 'Kupipi - 5*', '211000405': 'Prishe - 5*', '211000406': 'Prishe - 6*',
                         '904000101': 'Trust Moogle', '302001104': 'Cupid Artemios - 4*',
                         '302001105': 'Cupid Artemios - 5*', '302001106': 'Cupid Artemios - 6*',
                         '302001203': 'Cupid Luna - 3*', '302001204': 'Cupid Luna - 4*', '302001205': 'Cupid Luna - 5*',
                         '302001305': 'Olive - 5*', '302001306': 'Olive - 6*', '253000115': 'Mercenary Ramza - 5*',
                         '253000116': 'Mercenary Ramza - 6*', '253000215': 'Knight Delita - 5*',
                         '253000216': 'Knight Delita - 6*', '253000306': 'Agrias - 6*', '253000506': 'Gaffgarion - 6*',
                         '253000904': 'Meliadoul - 4*', '253000905': 'Meliadoul - 5*', '253000906': 'Meliadoul - 6*',
                         '253001204': 'Orran - 4*', '253001205': 'Orran - 5*', '253001206': 'Orran - 6*',
                         '100007705': 'Veritas of the Dark - 5*', '100007706': 'Veritas of the Dark - 6*',
                         '100008005': 'Veritas of the Flame - 5*', '100008006': 'Veritas of the Flame - 6*',
                         '100008104': 'Veritas of the Earth - 4*', '100008105': 'Veritas of the Earth - 5*',
                         '100008106': 'Veritas of the Earth - 6*', '100006904': 'Victoria - 4*',
                         '100006905': 'Victoria - 5*', '100006906': 'Victoria - 6*', '100008703': 'Timothy - 3*',
                         '100008704': 'Timothy - 4*', '100008705': 'Timothy - 5*', '100008804': 'Moogle - 4*',
                         '100008805': 'Moogle - 5*', '100008806': 'Moogle - 6*', '203000105': 'Onion Knight - 5*',
                         '203000106': 'Onion Knight - 6*', '203000904': 'Aria - 4*', '203000905': 'Aria - 5*',
                         '203000906': 'Aria - 6*', '203000704': 'Desch - 4*', '203000705': 'Desch - 5*',
                         '203000706': 'Desch - 6*', '203001003': 'Sara - 3*', '203001004': 'Sara - 4*',
                         '203001005': 'Sara - 5*', '100008205': 'Veritas of the Light - 5*',
                         '100008206': 'Veritas of the Light - 6*', '100007804': 'Veritas of the Heavens - 4*',
                         '100007805': 'Veritas of the Heavens - 5*', '100007806': 'Veritas of the Heavens - 6*',
                         '100007904': 'Veritas of the Waters - 4*', '100007905': 'Veritas of the Waters - 5*',
                         '100007906': 'Veritas of the Waters - 6*', '100004306': 'Charlotte - 6*',
                         '100004706': 'Hayate - 6*', '100008903': 'Guromu - 3*', '100008904': 'Guromu - 4*',
                         '100008905': 'Guromu - 5*', '100009004': 'Aura - 4*', '100009005': 'Aura - 5*',
                         '100009006': 'Aura - 6*', '100000115': 'Hunter Rain - 5*', '100000116': 'Hunter Rain - 6*',
                         '100000324': 'Hunter Fina - 4*', '100000325': 'Hunter Fina - 5*',
                         '100000326': 'Hunter Fina - 6*', '100000513': 'Hunter Lid - 3*',
                         '100000514': 'Hunter Lid - 4*', '100000515': 'Hunter Lid - 5*',
                         '100000414': 'Hunter Nichol - 4*', '100000415': 'Hunter Nichol - 5*',
                         '100000416': 'Hunter Nichol - 6*', '100000215': 'Hunter Lasswell - 5*',
                         '100000216': 'Hunter Lasswell - 6*', '100000614': 'Hunter Sakura - 4*',
                         '100000615': 'Hunter Sakura - 5*', '100000616': 'Hunter Sakura - 6*',
                         '100000713': 'Hunter Jake - 3*', '100000714': 'Hunter Jake - 4*',
                         '100000715': 'Hunter Jake - 5*', '100000306': 'Fina - 6*', '215001105': 'Nyx - 5*',
                         '215001106': 'Nyx - 6*', '215001204': 'Glauca - 4*', '215001205': 'Glauca - 5*',
                         '215001206': 'Glauca - 6*', '215001304': 'Crowe - 4*', '215001305': 'Crowe - 5*',
                         '215001306': 'Crowe - 6*', '215001403': 'Libertus - 3*', '215001404': 'Libertus - 4*',
                         '215001405': 'Libertus - 5*', '100009105': 'Loren - 5*', '100009106': 'Loren - 6*',
                         '100008605': 'Ayaka - 5*', '100008606': 'Ayaka - 6*', '100006404': 'Goken - 4*',
                         '100006405': 'Goken - 5*', '100006406': 'Goken - 6*', '100010104': 'Silvia - 4*',
                         '100010105': 'Silvia - 5*', '100010106': 'Silvia - 6*', '100010203': 'Kamui - 3*',
                         '100010204': 'Kamui - 4*', '100010205': 'Kamui - 5*', '100010303': 'Yuri - 3*',
                         '100010304': 'Yuri - 4*', '100010305': 'Yuri - 5*', '309000105': 'Julian - 5*',
                         '309000106': 'Julian - 6*', '309000205': 'Katarina - 5*', '309000206': 'Katarina - 6*',
                         '309000304': 'Harid - 4*', '309000305': 'Harid - 5*', '309000306': 'Harid - 6*',
                         '309000403': 'Robyn - 3*', '309000404': 'Robyn - 4*', '309000405': 'Robyn - 5*',
                         '303000204': '<na> - 4*', '303000205': '<na> - 5*', '303000206': '<na> - 6*',
                         '207000105': 'Cloud - 5*', '207000106': 'Cloud - 6*', '100009805': 'Elfreeda - 5*',
                         '100009806': 'Elfreeda - 6*', '100009903': 'Conrad - 3*', '100009904': 'Conrad - 4*',
                         '100009905': 'Conrad - 5*', '100010504': 'William - 4*', '100010505': 'William - 5*',
                         '100010506': 'William - 6*', '100010405': 'Roy - 5*', '100010406': 'Roy - 6*',
                         '100010604': 'Chloe - 4*', '100010605': 'Chloe - 5*', '100010606': 'Chloe - 6*',
                         '100010703': 'Amy - 3*', '100010704': 'Amy - 4*', '100010705': 'Amy - 5*',
                         '302001405': 'Fryevia - 5*', '302001406': 'Fryevia - 6*', '302001504': 'Xon - 4*',
                         '302001505': 'Xon - 5*', '302001506': 'Xon - 6*', '302001603': 'Aiden - 3*',
                         '302001604': 'Aiden - 4*', '302001605': 'Aiden - 5*', '401001705': 'Reberta - 5*',
                         '401001706': 'Reberta - 6*', '401001804': 'Zyrus - 4*', '401001805': 'Zyrus - 5*',
                         '401001806': 'Zyrus - 6*', '214000404': 'Yda - 4*', '214000405': 'Yda - 5*',
                         '214000406': 'Yda - 6*', '214000504': 'Papalymo - 4*', '214000505': 'Papalymo - 5*',
                         '214000506': 'Papalymo - 6*', '100009405': 'Kelsus  - 5*', '100009406': 'Kelsus  - 6*',
                         '401001105': 'Zargabaath - 5*', '401001106': 'Zargabaath - 6*',
                         '401000604': 'Artisan Lid - 4*', '401000605': 'Artisan Lid - 5*',
                         '401000704': 'Swordsman Lasswell - 4*', '401000705': 'Swordsman Lasswell - 5*',
                         '401000804': 'Cheerleader Fina - 4*', '401000805': 'Cheerleader Fina - 5*',
                         '401000904': 'Maiden Sakura - 4*', '401000905': 'Maiden Sakura - 5*',
                         '401001004': 'Cowboy Jake - 4*', '401001005': 'Cowboy Jake - 5*',
                         '100009304': 'Ashteroze - 4*', '100009305': 'Ashteroze - 5*', '100009306': 'Ashteroze - 6*',
                         '100009504': 'Nyalu - 4*', '100009505': 'Nyalu - 5*', '100009506': 'Nyalu - 6*',
                         '100009204': 'Kupolkan - 4*', '100009205': 'Kupolkan - 5*', '100009206': 'Kupolkan - 6*',
                         '100009604': 'Sandee - 4*', '100009605': 'Sandee - 5*', '100009606': 'Sandee - 6*',
                         '100009704': 'Grinfield - 4*', '100009705': 'Grinfield - 5*', '100009706': 'Grinfield - 6*',
                         '215000205': 'Gladiolus - 5*', '215000206': 'Gladiolus - 6*', '215000304': 'Cor - 4*',
                         '215000305': 'Cor - 5*', '215000306': 'Cor - 6*', '215000403': 'Iris - 3*',
                         '215000404': 'Iris - 4*', '215000405': 'Iris - 5*', '100010805': 'Duke - 5*',
                         '100010806': 'Duke - 6*', '100010904': 'Olif - 4*', '100010905': 'Olif - 5*',
                         '100010906': 'Olif - 6*', '100011004': 'Mystea - 4*', '100011005': 'Mystea - 5*',
                         '100011006': 'Mystea - 6*', '100011103': 'Charie - 3*', '100011104': 'Charie - 4*',
                         '100011105': 'Charie - 5*', '100011203': 'Ryunan - 3*', '100011204': 'Ryunan - 4*',
                         '100011205': 'Ryunan - 5*', '209000106': 'Zidane - 6*', '209000205': 'Vivi - 5*',
                         '209000206': 'Vivi - 6*', '209000306': 'Garnet - 6*', '209001006': 'Kuja - 6*',
                         '209001105': 'Beatrix - 5*', '209001106': 'Beatrix - 6*', '209000404': 'Steiner - 4*',
                         '209000405': 'Steiner - 5*', '209000406': 'Steiner - 6*', '209000705': 'Eiko - 5*',
                         '209000706': 'Eiko - 6*', '209001203': 'Black Waltz 3 - 3*', '209001204': 'Black Waltz 3 - 4*',
                         '209001205': 'Black Waltz 3 - 5*', '100003806': 'Miyuki - 6*', '100010306': 'Yuri - 6*',
                         '100011305': 'Jiraiya - 5*', '100011306': 'Jiraiya - 6*', '100011404': 'Kaede - 4*',
                         '100011405': 'Kaede - 5*', '100011406': 'Kaede - 6*', '100011504': 'Ohga - 4*',
                         '100011505': 'Ohga - 5*', '100011506': 'Ohga - 6*', '100011603': 'Otogiri - 3*',
                         '100011604': 'Otogiri - 4*', '100011605': 'Otogiri - 5*',
                         '100011705': 'Pyro Glacial Lasswell - 5*', '100011706': 'Pyro Glacial Lasswell - 6*',
                         '310000105': '2B - 5*', '310000106': '2B - 6*', '310000204': '9S - 4*', '310000205': '9S - 5*',
                         '310000206': '9S - 6*', '310000304': 'Adam - 4*', '310000305': 'Adam - 5*',
                         '310000306': 'Adam - 6*', '310000403': '21O - 3*', '310000404': '21O - 4*',
                         '310000405': '21O - 5*', '210000205': 'Yuna - 5*', '210000206': 'Yuna - 6*',
                         '210000405': 'Lulu - 5*', '210000406': 'Lulu - 6*', '210000804': 'Seymour - 4*',
                         '210000805': 'Seymour - 5*', '210000806': 'Seymour - 6*', '210000306': 'Wakka - 6*',
                         '100012405': 'Blossom Sage Sakura - 5*', '100012406': 'Blossom Sage Sakura - 6*',
                         '100013004': 'Verun - 4*', '100013005': 'Verun - 5*', '100013006': 'Verun - 6*',
                         '100013104': 'Cedona - 4*', '100013105': 'Cedona - 5*', '100013106': 'Cedona - 6*',
                         '100002706': 'Roselia - 6*', '100007606': 'Ruggles - 6*', '401001205': 'A2 - 5*',
                         '401001206': 'A2 - 6*', '401001304': 'Eve - 4*', '401001305': 'Eve - 5*',
                         '401001306': 'Eve - 6*', '304000306': 'Popoi - 6*', '401002304': 'Chic Ariana - 4*',
                         '401002305': 'Chic Ariana - 5*', '401002306': 'Chic Ariana - 6*', '312000105': 'Lise - 5*',
                         '312000106': 'Lise - 6*', '312000205': 'Hawk - 5*', '312000206': 'Hawk - 6*',
                         '312000305': 'Kevin - 5*', '312000306': 'Kevin - 6*', '312000404': 'Charlotte - 4*',
                         '312000405': 'Charlotte - 5*', '312000406': 'Charlotte - 6*', '311000105': 'Hero - 5*',
                         '311000106': 'Hero - 6*', '100011805': 'Lotus Mage Fina - 5*',
                         '100011806': 'Lotus Mage Fina - 6*', '100012605': 'Kunshira - 5*',
                         '100012606': 'Kunshira - 6*', '100012704': 'Wadow - 4*', '100012705': 'Wadow - 5*',
                         '100012706': 'Wadow - 6*', '100013203': 'Erwin - 3*', '100013204': 'Erwin - 4*',
                         '100013205': 'Erwin - 5*', '215000605': 'Aranea - 5*', '215000606': 'Aranea - 6*',
                         '215000705': 'Prompto - 5*', '215000706': 'Prompto - 6*', '215000406': 'Iris - 6*',
                         '401001903': 'Scarmiglione - 3*', '401001904': 'Scarmiglione - 4*',
                         '401001905': 'Scarmiglione - 5*', '401001604': 'Cagnazzo - 4*', '401001605': 'Cagnazzo - 5*',
                         '401001606': 'Cagnazzo - 6*', '401001504': 'Rubicante - 4*', '401001505': 'Rubicante - 5*',
                         '401001506': 'Rubicante - 6*', '401001405': 'Barbariccia - 5*',
                         '401001406': 'Barbariccia - 6*', '401002504': 'Sportive Ariana - 4*',
                         '401002505': 'Sportive Ariana - 5*', '401002506': 'Sportive Ariana - 6*',
                         '401002405': 'Charming Kitty Ariana - 5*', '401002406': 'Charming Kitty Ariana - 6*',
                         '401002005': 'Grim Lord Sakura - 5*', '401002006': 'Grim Lord Sakura - 6*',
                         '401002104': 'Illusionist Nichol - 4*', '401002105': 'Illusionist Nichol - 5*',
                         '401002106': 'Illusionist Nichol - 6*', '401002204': 'Pirate Jake - 4*',
                         '401002205': 'Pirate Jake - 5*', '401002206': 'Pirate Jake - 6*',
                         '401000506': 'Black Cat Lid - 6*', '212001105': 'Gabranth - 5*', '212001106': 'Gabranth - 6*',
                         '212000905': 'Basch - 5*', '212000906': 'Basch - 6*', '212001204': 'Vayne - 4*',
                         '212001205': 'Vayne - 5*', '212001206': 'Vayne - 6*', '212001404': 'Drace - 4*',
                         '212001405': 'Drace - 5*', '212001406': 'Drace - 6*', '212001303': 'Larsa - 3*',
                         '212001304': 'Larsa - 4*', '212001305': 'Larsa - 5*', '100012005': 'Nameless Gunner Jake - 5*',
                         '100012006': 'Nameless Gunner Jake - 6*', '100013305': 'Emperor Shera - 5*',
                         '100013306': 'Emperor Shera - 6*', '100012104': 'Emilia - 4*', '100012105': 'Emilia - 5*',
                         '100012106': 'Emilia - 6*', '100012304': 'Ozetta - 4*', '100012305': 'Ozetta - 5*',
                         '100012306': 'Ozetta - 6*', '100012203': 'Riley - 3*', '100012204': 'Riley - 4*',
                         '100012205': 'Riley - 5*', '100006606': 'Camille - 6*', '313000105': 'Tiz - 5*',
                         '313000106': 'Tiz - 6*', '313000205': 'Agnès - 5*', '313000206': 'Agnès - 6*',
                         '313000305': 'Bravo Bunny Agnès - 5*', '313000306': 'Bravo Bunny Agnès - 6*',
                         '313000404': 'Edea - 4*', '313000405': 'Edea - 5*', '313000406': 'Edea - 6*',
                         '314000104': 'Yew - 4*', '314000105': 'Yew - 5*', '314000106': 'Yew - 6*',
                         '314000203': 'Magnolia - 3*', '314000204': 'Magnolia - 4*', '314000205': 'Magnolia - 5*',
                         '315000104': 'Rinne - 4*', '315000105': 'Rinne - 5*', '315000106': 'Rinne - 6*',
                         '204001505': 'Pure Summoner Rydia - 5*', '204001506': 'Pure Summoner Rydia - 6*',
                         '204001605': 'Atoning Dragoon Kain - 5*', '204001606': 'Atoning Dragoon Kain - 6*',
                         '204000704': 'Yang - 4*', '204000705': 'Yang - 5*', '204000706': 'Yang - 6*',
                         '204000603': 'Edward - 3*', '204000604': 'Edward - 4*', '204000605': 'Edward - 5*',
                         '204000306': 'Rosa - 6*', '100011905': 'Heavenly Technician Lid - 5*',
                         '100011906': 'Heavenly Technician Lid - 6*', '100013404': 'Killian - 4*',
                         '100013405': 'Killian - 5*', '100013406': 'Killian - 6*', '100006006': 'Ulrica - 6*',
                         '100005706': 'Heltich - 6*', '100014405': 'Reberta - 5*', '100014406': 'Reberta - 6*',
                         '100014504': 'Ling - 4*', '100014505': 'Ling - 5*', '100014506': 'Ling - 6*',
                         '100014604': 'Xon - 4*', '100014605': 'Xon - 5*', '100014606': 'Xon - 6*',
                         '100014703': 'Aiden - 3*', '100014704': 'Aiden - 4*', '100014705': 'Aiden - 5*',
                         '100014005': 'Mediena - 5*', '100014006': 'Mediena - 6*', '207001005': 'Sephiroth - 5*',
                         '207001006': 'Sephiroth - 6*', '100013805': 'Lila - 5*', '100013806': 'Lila - 6*',
                         '100013504': 'Shylt - 4*', '100013505': 'Shylt - 5*', '100013506': 'Shylt - 6*',
                         '100013903': 'Mim - 3*', '100013904': 'Mim - 4*', '100013905': 'Mim - 5*',
                         '100012505': 'Maritime Strategist Nichol - 5*', '100012506': 'Maritime Strategist Nichol - 6*',
                         '100014104': 'Lexa - 4*', '100014105': 'Lexa - 5*', '100014106': 'Lexa - 6*',
                         '100014204': 'Elbis - 4*', '100014205': 'Elbis - 5*', '100014206': 'Elbis - 6*',
                         '100014303': 'Merald - 3*', '100014304': 'Merald - 4*', '100014305': 'Merald - 5*',
                         '100011106': 'Charie - 6*', '318000105': 'Fayt - 5*', '318000106': 'Fayt - 6*',
                         '317000105': 'Rena - 5*', '317000106': 'Rena - 6*', '320000104': 'Fidel - 4*',
                         '320000105': 'Fidel - 5*', '320000106': 'Fidel - 6*', '319000104': 'Reimi - 4*',
                         '319000105': 'Reimi - 5*', '319000106': 'Reimi - 6*', '316000103': 'Roddick - 3*',
                         '316000104': 'Roddick - 4*', '316000105': 'Roddick - 5*', '100010005': 'Raegen - 5*',
                         '100010006': 'Raegen - 6*', '100015104': 'Ryumynui - 4*', '100015105': 'Ryumynui - 5*',
                         '100015106': 'Ryumynui - 6*', '100015204': 'Zile - 4*', '100015205': 'Zile - 5*',
                         '100015206': 'Zile - 6*', '100015303': 'Lucille - 3*', '100015304': 'Lucille - 4*',
                         '100015305': 'Lucille - 5*', '401002605': 'Christine - 5*', '401002606': 'Christine - 6*',
                         '401002705': 'Kryla - 5*', '401002706': 'Kryla - 6*', '401002804': 'Tinkerer Carrie - 4*',
                         '401002805': 'Tinkerer Carrie - 5*', '401002806': 'Tinkerer Carrie - 6*',
                         '100003906': 'Gilbert - 6*', '401002905': 'Ray Jack - 5*', '401002906': 'Ray Jack - 6*',
                         '401003104': 'Kaliva - 4*', '401003105': 'Kaliva - 5*', '401003106': 'Kaliva - 6*',
                         '401003004': 'Barusa - 4*', '401003005': 'Barusa - 5*', '401003006': 'Barusa - 6*',
                         '401003203': 'Toby - 3*', '401003204': 'Toby - 4*', '401003205': 'Toby - 5*',
                         '401003704': 'Yan - 4*', '401003705': 'Yan - 5*', '401003706': 'Yan - 6*',
                         '401003805': 'Chow - 5*', '401003806': 'Chow - 6*', '401003905': 'Ang - 5*',
                         '401003906': 'Ang - 6*', '401003303': 'Pharaoh Abel - 3*', '401003304': 'Pharaoh Abel - 4*',
                         '401003305': 'Pharaoh Abel - 5*', '401003404': 'Divine Soleil - 4*',
                         '401003405': 'Divine Soleil - 5*', '401003406': 'Divine Soleil - 6*',
                         '401003505': 'Explorer Aileen - 5*', '401003506': 'Explorer Aileen - 6*',
                         '401003605': 'Lara Croft - 5*', '401003606': 'Lara Croft - 6*', '100014905': 'Madam - 5*',
                         '100015005': 'Vagrant Knight Rain - 5*', '100015006': 'Vagrant Knight Rain - 6*',
                         '100015805': 'Rain (Awoken) - 5*', '100015806': 'Rain (Awoken) - 6*',
                         '208000105': 'Squall - 5*', '208000106': 'Squall - 6*', '208000107': 'Squall - 7*',
                         '208000205': 'Rinoa - 5*', '208000206': 'Rinoa - 6*', '208000207': 'Rinoa - 7*',
                         '208000404': 'Zell - 4*', '208000405': 'Zell - 5*', '208000406': 'Zell - 6*',
                         '100016503': 'Ramilla - 3*', '100016504': 'Ramilla - 4*', '100016505': 'Ramilla - 5*',
                         '213000107': 'Lightning - 7*', '253000107': 'Ramza - 7*', '253000207': 'Delita - 7*',
                         '204000117': 'Dark Knight Cecil - 7*', '254000107': 'Ace - 7*', '203000207': 'Luneth - 7*',
                         '254000207': 'Queen - 7*', '100000317': 'Dark Fina - 7*', '253000807': 'Orlandeau - 7*',
                         '100005807': 'Marie - 7*', '202000507': 'Emperor - 7*', '306000107': 'Dragonlord - 7*',
                         '100005907': 'Aileen - 7*', '254000907': 'Rem - 7*', '210000107': 'Tidus - 7*',
                         '100006107': 'Wilhelm - 7*', '100007207': 'Seabreeze Dark Fina - 7*',
                         '206000127': 'Trance Terra - 7*', '100006807': 'Fohlen - 7*',
                         '100007707': 'Veritas of the Dark - 7*', '203000107': 'Onion Knight - 7*',
                         '100015405': 'Nalu - 5*', '100015406': 'Nalu - 6*', '100015407': 'Nalu - 7*',
                         '100015504': 'Pecciotta - 4*', '100015505': 'Pecciotta - 5*', '100015506': 'Pecciotta - 6*',
                         '100015604': 'Shinju - 4*', '100015605': 'Shinju - 5*', '100015606': 'Shinju - 6*',
                         '100015703': 'Ryuka - 3*', '100015704': 'Ryuka - 4*', '100015705': 'Ryuka - 5*',
                         '306000905': 'Estark - 5*', '306000906': 'Estark - 6*', '306000907': 'Estark - 7*',
                         '306001005': 'Marquis de Léon - 5*', '306001006': 'Marquis de Léon - 6*',
                         '306001007': 'Marquis de Léon - 7*', '306001104': 'Überkilling Machine - 4*',
                         '306001105': 'Überkilling Machine - 5*', '306001106': 'Überkilling Machine - 6*',
                         '306001204': 'Slime Knight - 4*', '306001205': 'Slime Knight - 5*',
                         '306001206': 'Slime Knight - 6*', '306001303': 'Dracky - 3*', '306001304': 'Dracky - 4*',
                         '306001305': 'Dracky - 5*', '211000805': 'Livid Shantotto - 5*',
                         '211000806': 'Livid Shantotto - 6*', '211000807': 'Livid Shantotto - 7*',
                         '211000905': 'Shadow Lord - 5*', '211000906': 'Shadow Lord - 6*',
                         '211000907': 'Shadow Lord - 7*', '211001004': 'Joachim - 4*', '211001005': 'Joachim - 5*',
                         '211001006': 'Joachim - 6*', '211000306': 'Kupipi - 6*', '100007507': 'Lunera - 7*',
                         '211000407': 'Prishe - 7*', '253000117': 'Mercenary Ramza - 7*',
                         '253000217': 'Knight Delita - 7*', '207000107': 'Cloud - 7*',
                         '100008007': 'Veritas of the Flame - 7*', '100009107': 'Loren - 7*',
                         '100008207': 'Veritas of the Light - 7*', '215000107': 'Noctis - 7*',
                         '209001107': 'Beatrix - 7*', '209000707': 'Eiko - 7*', '100016205': 'Hyoh - 5*',
                         '100016206': 'Hyoh - 6*', '100016207': 'Hyoh - 7*', '100016304': 'Shatal - 4*',
                         '100016305': 'Shatal - 5*', '100016306': 'Shatal - 6*', '100016403': 'Domino - 3*',
                         '100016404': 'Domino - 4*', '100016405': 'Domino - 5*', '100017005': 'Santa Roselia - 5*',
                         '100017006': 'Santa Roselia - 6*', '100017007': 'Santa Roselia - 7*',
                         '100016605': 'Ukiyo - 5*', '100016606': 'Ukiyo - 6*', '215000505': 'Ignis - 5*',
                         '215000506': 'Ignis - 6*', '215000507': 'Ignis - 7*', '215001004': 'Ravus - 4*',
                         '215001005': 'Ravus - 5*', '215001006': 'Ravus - 6*', '215001406': 'Libertus - 6*',
                         '307000105': 'Ray Jack - 5*', '307000106': 'Ray Jack - 6*', '307000107': 'Ray Jack - 7*',
                         '307000204': 'Kaliva - 4*', '307000205': 'Kaliva - 5*', '307000206': 'Kaliva - 6*',
                         '307000404': 'Toby - 4*', '307000405': 'Toby - 5*', '307000406': 'Toby - 6*',
                         '307000303': 'Barusa - 3*', '307000304': 'Barusa - 4*', '307000305': 'Barusa - 5*',
                         '212000507': 'Balthier - 7*', '205000807': 'Gilgamesh - 7*', '100008607': 'Ayaka - 7*',
                         '100009807': 'Elfreeda - 7*', '100010407': 'Roy - 7*', '215000207': 'Gladiolus - 7*',
                         '100010807': 'Duke - 7*', '100011707': 'Pyro Glacial Lasswell - 7*', '210000207': 'Yuna - 7*',
                         '210000407': 'Lulu - 7*', '100012407': 'Blossom Sage Sakura - 7*',
                         '100011807': 'Lotus Mage Fina - 7*', '215000607': 'Aranea - 7*', '215000707': 'Prompto - 7*',
                         '100012607': 'Kunshira - 7*', '100016905': 'Citra - 5*', '100016906': 'Citra - 6*',
                         '100016907': 'Citra - 7*', '100016704': 'Macmedi - 4*', '100016705': 'Macmedi - 5*',
                         '100016706': 'Macmedi - 6*', '100016803': 'Lotti - 3*', '100016804': 'Lotti - 4*',
                         '100016805': 'Lotti - 5*', '330000105': 'Lenneth - 5*', '330000106': 'Lenneth - 6*',
                         '330000107': 'Lenneth - 7*', '330000205': 'Freya (VP) - 5*', '330000206': 'Freya (VP) - 6*',
                         '330000207': 'Freya (VP) - 7*', '330000305': 'Arngrim - 5*', '330000306': 'Arngrim - 6*',
                         '330000307': 'Arngrim - 7*', '330000404': 'Lucian - 4*', '330000405': 'Lucian - 5*',
                         '330000406': 'Lucian - 6*', '330000503': 'Jelanda - 3*', '330000504': 'Jelanda - 4*',
                         '330000505': 'Jelanda - 5*', '207000305': 'Tifa - 5*', '207000306': 'Tifa - 6*',
                         '207000307': 'Tifa - 7*', '207000805': 'Vincent - 5*', '207000806': 'Vincent - 6*',
                         '207000807': 'Vincent - 7*', '207000204': 'Barret - 4*', '207000205': 'Barret - 5*',
                         '207000206': 'Barret - 6*', '207000703': 'Cait Sith - 3*', '207000704': 'Cait Sith - 4*',
                         '207000705': 'Cait Sith - 5*', '215001107': 'Nyx - 7*', '100011307': 'Jiraiya - 7*',
                         '212001107': 'Gabranth - 7*', '212000907': 'Basch - 7*',
                         '100012007': 'Nameless Gunner Jake - 7*', '100013307': 'Emperor Shera - 7*',
                         '204001507': 'Pure Summoner Rydia - 7*', '204001607': 'Atoning Dragoon Kain - 7*',
                         '100011907': 'Heavenly Technician Lid - 7*', '100014007': 'Mediena - 7*',
                         '207001007': 'Sephiroth - 7*', '100013807': 'Lila - 7*',
                         '100012507': 'Maritime Strategist Nichol - 7*', '100010007': 'Raegen - 7*',
                         '100015807': 'Rain (Awoken) - 7*', '100017105': 'Elephim - 5*', '100017106': 'Elephim - 6*',
                         '100017107': 'Elephim - 7*', '100017204': 'Leopold - 4*', '100017205': 'Leopold - 5*',
                         '100017206': 'Leopold - 6*', '100017304': 'Magna - 4*', '100017305': 'Magna - 5*',
                         '100017306': 'Magna - 6*', '100017403': 'Forelsket - 3*', '100017404': 'Forelsket - 4*',
                         '100017405': 'Forelsket - 5*', '304000405': 'Flammie - 5*', '304000406': 'Flammie - 6*',
                         '304000407': 'Flammie - 7*', '304000107': 'Randi - 7*', '312000307': 'Kevin - 7*',
                         '312000107': 'Lise - 7*', '312000207': 'Hawkeye - 7*', '304000503': 'Rabite - 3*',
                         '304000504': 'Rabite - 4*', '304000505': 'Rabite - 5*', '254001805': 'Machina - 5*',
                         '254001806': 'Machina - 6*', '254001807': 'Machina - 7*', '254001905': 'Kurasame - 5*',
                         '254001906': 'Kurasame - 6*', '254001907': 'Kurasame - 7*', '254002004': 'Deuce - 4*',
                         '254002005': 'Deuce - 5*', '254002006': 'Deuce - 6*', '254001103': 'Cater - 3*',
                         '254001104': 'Cater - 4*', '254001105': 'Cater - 5*', '100017905': 'Sieghard - 5*',
                         '100017906': 'Sieghard - 6*', '100017907': 'Sieghard - 7*', '100018004': 'Detrinde - 4*',
                         '100018005': 'Detrinde - 5*', '100018006': 'Detrinde - 6*', '100018104': 'Deobalt - 4*',
                         '100018105': 'Deobalt - 5*', '100018106': 'Deobalt - 6*', '100018203': 'Cannon - 3*',
                         '100018204': 'Cannon - 4*', '100018205': 'Cannon - 5*', '332000105': 'Lara Croft - 5*',
                         '332000106': 'Lara Croft - 6*', '100017605': 'Yuraisha - 5*', '100017606': 'Yuraisha - 6*',
                         '100017607': 'Yuraisha - 7*', '100017704': 'Franis - 4*', '100017705': 'Franis - 5*',
                         '100017706': 'Franis - 6*', '100017803': 'Ishil - 3*', '100017804': 'Ishil - 4*',
                         '100017805': 'Ishil - 5*', '203001305': 'Onion Knight Refia - 5*',
                         '203001306': 'Onion Knight Refia - 6*', '203001307': 'Onion Knight Refia - 7*',
                         '203001405': 'Dark Knight Luneth - 5*', '203001406': 'Dark Knight Luneth - 6*',
                         '203001407': 'Dark Knight Luneth - 7*', '203000604': 'Doga - 4*', '203000605': 'Doga - 5*',
                         '203000606': 'Doga - 6*', '203001503': 'Unei - 3*', '203001504': 'Unei - 4*',
                         '203001505': 'Unei - 5*', '900010501': 'Gil Snapper Tower', '904000115': 'Prism Moogle - 5*'}

jsondata = '{"PurchaseSettlement": {"Url": "yt82BRwk.php", "EncodeKey": "jmh7xID8", "RequestID": "JsFd4b7j"}, "RbMatching": {"Url": "mn5cHaJ0.php", "EncodeKey": "4GSMn0qb", "RequestID": "DgG4Cy0F"}, "RmDungeonStart": {"Url": "NC8Ie07P.php", "EncodeKey": "A7V1zkyc", "RequestID": "R5mWbQ3M"}, "ExchangeShop": {"Url": "1bf0HF4w.php", "EncodeKey": "qoRP87Fw", "RequestID": "I7fmVX3R"}, "FriendDelete": {"Url": "8R4fQbYh.php", "EncodeKey": "d0VP5ia6", "RequestID": "a2d6omAy"}, "UpdateSwitchInfo": {"Url": "SqoB3a1T.php", "EncodeKey": "4Z5UNaIW", "RequestID": "mRPo5n2j"}, "VariableStoreCheck": {"Url": "Nhn93ukW.php", "EncodeKey": "Hi0FJU3c", "RequestID": "i0woEP4B"}, "CraftStart": {"Url": "w71MZ0Gg.php", "EncodeKey": "K92H8wkY", "RequestID": "Gr9zxXk5"}, "SearchGetItemInfo": {"Url": "e4Gjkf0x.php", "EncodeKey": "vK2V8mZM", "RequestID": "0D9mpGUR"}, "SublimationSkill": {"Url": "xG3jBbw5.php", "EncodeKey": "97Uvrdz3", "RequestID": "s48Qzvhd"}, "TownIn": {"Url": "isHfQm09.php", "EncodeKey": "JI8zU5rC", "RequestID": "8EYGrg76"}, "MissionBreak": {"Url": "P4oIeVf0.php", "EncodeKey": "Z2oPiE6p", "RequestID": "17LFJD0b"}, "BeastMix": {"Url": "7vHqNPF0.php", "EncodeKey": "WfNSmy98", "RequestID": "C8X1KUpV"}, "LoginBonus": {"Url": "iP9ogKy6.php", "EncodeKey": "Vi6vd9zG", "RequestID": "vw9RP3i4"}, "AllianceEntry": {"Url": "EzfT0wX6.php", "EncodeKey": "zS4tPgi7", "RequestID": "HtR8XF4e"}, "DmgRankEnd": {"Url": "zd5KJ3jn.php", "EncodeKey": "7pGj8hSW", "RequestID": "s98cw1WA"}, "GetUserInfo": {"Url": "u7sHDCg4.php", "EncodeKey": "rcsq2eG7", "RequestID": "X07iYtp5"}, "NoticeUpdate": {"Url": "TqtzK84R.php", "EncodeKey": "9t68YyjT", "RequestID": "CQ4jTm2F"}, "TownOut": {"Url": "0EF3JPjL.php", "EncodeKey": "Kc2PXd9D", "RequestID": "sJcMPy04"}, "BeastBoardPieceOpen": {"Url": "Y2Zvnad9.php", "EncodeKey": "7uxYTm3k", "RequestID": "0gk3Tfbz"}, "NoticeReadUpdate": {"Url": "j6kSWR3q.php", "EncodeKey": "iLdaq6j2", "RequestID": "pC3a2JWU"}, "MissionWaveStart": {"Url": "Mn15zmDZ.php", "EncodeKey": "d2mqJ6pT", "RequestID": "BSq28mwY"}, "PlaybackMissionStart": {"Url": "zm2ip59f.php", "EncodeKey": "YC20v1Uj", "RequestID": "1YnQM4iB"}, "MissionContinue": {"Url": "ZzCXI6E7.php", "EncodeKey": "34n2iv7z", "RequestID": "LuCN4tU5"}, "RmEnd": {"Url": "I9p3n48A.php", "EncodeKey": "FX5L3Sfv", "RequestID": "fyp10Rrc"}, "FriendSuggest": {"Url": "6TCn0BFh.php", "EncodeKey": "j2P3uqRC", "RequestID": "iAs67PhJ"}, "RoutineWorldUpdate": {"Url": "oR1psQ5B.php", "EncodeKey": "XDIL4E7j", "RequestID": "6H1R9WID"}, "UnitSell": {"Url": "0qmzs2gA.php", "EncodeKey": "DJ43wmds", "RequestID": "9itzg1jc"}, "StrongBoxOpen": {"Url": "48ktHf13.php", "EncodeKey": "sgc30nRh", "RequestID": "PIv7u8jU"}, "GetReinforcementInfo": {"Url": "hXMoLwgE.php", "EncodeKey": "87khNMou", "RequestID": "AJhnI37s"}, "RbStart": {"Url": "dR20sWwE.php", "EncodeKey": "P1w8BKLI", "RequestID": "eHY7X8Nn"}, "ClsmStart": {"Url": "rncR9js8.php", "EncodeKey": "wdSs23yW", "RequestID": "4uCSA3ko"}, "GachaExe": {"Url": "oC30VTFp.php", "EncodeKey": "oaEJ9y1Z", "RequestID": "9fVIioy1"}, "ExploreRetire": {"Url": "Gv0BZr4X.php", "EncodeKey": "3jTz0GIE", "RequestID": "t8Yd2Pcy"}, "CraftExe": {"Url": "UyHLjV60.php", "EncodeKey": "ZbHEB15J", "RequestID": "PKDhIN34"}, "ChallengeClear": {"Url": "dEvLKchl.php", "EncodeKey": "UD5QCa2s", "RequestID": "D9xphQ8X"}, "RoutineRaidMenuUpdate": {"Url": "Sv85kcPQ.php", "EncodeKey": "z80swWd9", "RequestID": "g0BjrU5D"}, "Friend": {"Url": "8drhF2mG.php", "EncodeKey": "6WAkj0IH", "RequestID": "j0A5vQd8"}, "PurchaseHold": {"Url": "dCxtMZ27.php", "EncodeKey": "5Mwfq90Z", "RequestID": "79EVRjeM"}, "RmRetire": {"Url": "fBn58ApV.php", "EncodeKey": "T4Undsr6", "RequestID": "e0R3iDm1"}, "FriendList": {"Url": "p3hwqW5U.php", "EncodeKey": "1iV2oN9r", "RequestID": "u7Id4bMg"}, "MailList": {"Url": "u3E8hpad.php", "EncodeKey": "7kgsrGQ1", "RequestID": "KQHpi0D7"}, "FriendRefuse": {"Url": "Vw0a4I3i.php", "EncodeKey": "RYdX9h2A", "RequestID": "1nbWRV9w"}, "RmRestart": {"Url": "NC8Ie07P.php", "EncodeKey": "R1VjnNx0", "RequestID": "yh21MTaG"}, "MissionEnd": {"Url": "0ydjM5sU.php", "EncodeKey": "1tg0Lsqj", "RequestID": "x5Unqg2d"}, "UpdateUserInfo": {"Url": "v3RD1CUB.php", "EncodeKey": "6v5ykfpr", "RequestID": "ey8mupb4"}, "MissionContinueRetire": {"Url": "cQU1D9Nx.php", "EncodeKey": "F1QRxT5m", "RequestID": "V3CiWT0r"}, "RmStart": {"Url": "8BJSL7g0.php", "EncodeKey": "iu67waph", "RequestID": "7FyJS3Zn"}, "ExploreStart": {"Url": "0PIk8qdm.php", "EncodeKey": "0Xpfxg7U", "RequestID": "FR4ISN7P"}, "MissionUpdate": {"Url": "fRDUy3E2.php", "EncodeKey": "Nq9uKGP7", "RequestID": "j5JHKq6S"}, "ExploreSetting": {"Url": "O4JRsPZU.php", "EncodeKey": "i6M7o0cg", "RequestID": "f8Q0BJVX"}, "CreateUser": {"Url": "0FK8NJRX.php", "EncodeKey": "73BUnZEr", "RequestID": "P6pTz4WA"}, "ClsmEnd": {"Url": "7vHqNPF0.php", "EncodeKey": "6aBHXGv4", "RequestID": "3zgbapQ7"}, "IsNeedValidate": {"Url": "gk3Wtr8A.php", "EncodeKey": "djhiU6x8", "RequestID": "er5xMIj6"}, "SpChallengeEntry": {"Url": "8DermCsY.php", "EncodeKey": "Uey5jW2G", "RequestID": "MTf2j9aK"}, "ItemBuy": {"Url": "oQrAys71.php", "EncodeKey": "InN5PUR0", "RequestID": "sxK2HG6T"}, "RmEntry": {"Url": "fBn58ApV.php", "EncodeKey": "p2tqP7Ng", "RequestID": "wx5sg9ye"}, "MissionSwitchUpdate": {"Url": "1Xz8kJLr.php", "EncodeKey": "bZezA63a", "RequestID": "Tvq54dx6"}, "GachaEntry": {"Url": "tUJxSQz7.php", "EncodeKey": "39cFjtId", "RequestID": "rj6dxU9w"}, "TransferCodeCheck": {"Url": "C9LoeYJ8.php", "EncodeKey": "c5aNjK9J", "RequestID": "CY89mIdz"}, "CraftEnd": {"Url": "9G7Vc8Ny.php", "EncodeKey": "yD97t8kB", "RequestID": "WIuvh09n"}, "AllianceDeckEdit": {"Url": "7gAGFC4I.php", "EncodeKey": "2E3UinsJ", "RequestID": "P76LYXow"}, "MissionRetire": {"Url": "gbZ64SQ2.php", "EncodeKey": "oUh1grm8", "RequestID": "v51PM7wj"}, "FriendAgree": {"Url": "1DYp5Nqm.php", "EncodeKey": "9FjK0zM3", "RequestID": "kx13SLUY"}, "GiftUpdate": {"Url": "noN8I0UK.php", "EncodeKey": "xLEtf78b", "RequestID": "9KN5rcwj"}, "ClsmEntry": {"Url": "UmLwv56W.php", "EncodeKey": "8bmHF3Cz", "RequestID": "5g0vWZFq"}, "MissionReStart": {"Url": "r5vfM1Y3.php", "EncodeKey": "Vw6bP0rN", "RequestID": "GfI4LaU3"}, "TransferCodeIssue": {"Url": "hF0yCKc1.php", "EncodeKey": "T0y6ij47", "RequestID": "crzI2bA5"}, "RoutineHomeUpdate": {"Url": "1YWTzU9h.php", "EncodeKey": "aw0syG7H", "RequestID": "Daud71Hn"}, "ItemCarryEdit": {"Url": "8BE6tJbf.php", "EncodeKey": "04opy1kf", "RequestID": "UM7hA0Zd"}, "ClsmLottery": {"Url": "4uj3NhUQ.php", "EncodeKey": "pU62SkhJ", "RequestID": "Un16HuNI"}, "EquipGrowAbilityFix": {"Url": "CnPyXkUV.php", "EncodeKey": "58dS0DZN", "RequestID": "k8ew94DN"}, "MissionStart": {"Url": "63VqtzbQ.php", "EncodeKey": "i48eAVL6", "RequestID": "29JRaDbd"}, "DungeonResourceLoadMstList": {"Url": "Sl8UgmP4.php", "EncodeKey": "3PVu6ReZ", "RequestID": "jnw49dUq"}, "PurchaseGiveUp": {"Url": "C2w0f3go.php", "EncodeKey": "xoZ62QWy", "RequestID": "BFf1nwh6"}, "PurchaseCurrentState": {"Url": "bAR4k7Qd.php", "EncodeKey": "X9k5vFdu", "RequestID": "9mM3eXgi"}, "UnitFavorite": {"Url": "sqeRg12M.php", "EncodeKey": "w9mWkGX0", "RequestID": "tBDi10Ay"}, "Initialize": {"Url": "fSG1eXI9.php", "EncodeKey": "rVG09Xnt", "RequestID": "75fYdNxq"}, "FriendFavorite": {"Url": "8IYSJ5H1.php", "EncodeKey": "3EBXbj1d", "RequestID": "1oE3Fwn4"}, "RbRanking": {"Url": "3fd8y7W1.php", "EncodeKey": "SR6PoLM3", "RequestID": "kcW85SfU"}, "DailyDungeonSelect": {"Url": "9LgmdR0v.php", "EncodeKey": "ioC6zqG1", "RequestID": "JyfxY2e0"}, "PurchaseList": {"Url": "YqZ6Qc1z.php", "EncodeKey": "X3Csghu0", "RequestID": "BT28S96F"}, "RbReStart": {"Url": "DQ49vsGL.php", "EncodeKey": "PRzAL3V2", "RequestID": "6ZNY3zAm"}, "EquipGrowAbilitySelectResume": {"Url": "Ke7YG3xW.php", "EncodeKey": "7YxgkK1V", "RequestID": "80R6BXUw"}, "ArchiveUpdate": {"Url": "2bCcKx0D.php", "EncodeKey": "IFLW9H4M", "RequestID": "cVTxW0K3"}, "PurchaseSetting": {"Url": "9hUtW0F8.php", "EncodeKey": "ePFcMX53", "RequestID": "QkwU4aD9"}, "RbEntry": {"Url": "30inL7I6.php", "EncodeKey": "EA5amS29", "RequestID": "f8kXGWy0"}, "DungeonLiberation": {"Url": "0vc6irBY.php", "EncodeKey": "0xDA4Cr9", "RequestID": "nQMb2L4h"}, "OptionUpdate": {"Url": "0Xh2ri5E.php", "EncodeKey": "B9mAa7rp", "RequestID": "otgXV79T"}, "UnitMix": {"Url": "6aLHwhJ8.php", "EncodeKey": "4zCuj2hK", "RequestID": "UiSC9y8R"}, "UnitEquip": {"Url": "nIk9z5pT.php", "EncodeKey": "45VZgFYv", "RequestID": "pB3st6Tg"}, "Transfer": {"Url": "v6Jba7pX.php", "EncodeKey": "C6eHo3wU", "RequestID": "oE5fmZN9"}, "CraftAdd": {"Url": "iQ7R4CFB.php", "EncodeKey": "qz0SG1Ay", "RequestID": "QkN1Sp64"}, "GachaSelectExe": {"Url": "eB0VYGMt.php", "EncodeKey": "BuJqHc41", "RequestID": "xio14KrL"}, "GachaInfo": {"Url": "3nhWq25K.php", "EncodeKey": "VA8QR57X", "RequestID": "UNP1GR5n"}, "RbEnd": {"Url": "e8AHNiT7.php", "EncodeKey": "MVA3Te2i", "RequestID": "os4k7C0b"}, "RmDungeonEnd": {"Url": "CH9fWn8K.php", "EncodeKey": "dEnsQ75t", "RequestID": "WaPC2T6i"}, "ExploreEntry": {"Url": "mr6DnTQV.php", "EncodeKey": "a4X1Q2Hm", "RequestID": "Tnkz60cb"}, "TownUpdate": {"Url": "0ZJzH2qY.php", "EncodeKey": "37nH21zE", "RequestID": "G1hQM8Dr"}, "GetTitleInfo": {"Url": "BbIeq31M.php", "EncodeKey": "Mw56RNZ2", "RequestID": "ocP3A1FI"}, "PurchaseFailed": {"Url": "2TCis0R6.php", "EncodeKey": "sW0vf3ZM", "RequestID": "jSe80Gx7"}, "PurchaseCancel": {"Url": "y71uBCER.php", "EncodeKey": "Z1mojg9a", "RequestID": "L7K0ezU2"}, "DmgRankRetire": {"Url": "8wdmR9yG.php", "EncodeKey": "5fkWyeE6", "RequestID": "W3Z4VF1X"}, "ItemSell": {"Url": "hQRf8D6r.php", "EncodeKey": "E8H3UerF", "RequestID": "d9Si7TYm"}, "ExploreRewardGet": {"Url": "RhznNjzo.php", "EncodeKey": "LaFmew85", "RequestID": "XG3CwM1N"}, "RbBoardPieceOpen": {"Url": "iXKfI4v1.php", "EncodeKey": "g68FW4k1", "RequestID": "hqzU9Qc5"}, "FriendDetail": {"Url": "QBiJEyUt.php", "EncodeKey": "aKvkU6Y4", "RequestID": "7kG0JAvE"}, "PlaybackMissionWaveStart": {"Url": "scyPYa81.php", "EncodeKey": "NdkX15vE", "RequestID": "1BpXP3Fs"}, "MailReceipt": {"Url": "M2fHBe9d.php", "EncodeKey": "P2YFr7N9", "RequestID": "XK7efER9"}, "UnitClassUp": {"Url": "8z4Z0DUY.php", "EncodeKey": "L2sTK0GM", "RequestID": "zf49XKg8"}, "SpChallengeRewardGet": {"Url": "9inGHyqC.php", "EncodeKey": "mG25PIUn", "RequestID": "2G7ZVs4A"}, "PartyDeckEdit": {"Url": "6xkK4eDG.php", "EncodeKey": "34qFNPf7", "RequestID": "TS5Dx9aZ"}, "FriendSearch": {"Url": "6Y1jM3Wp.php", "EncodeKey": "VCL5oj6u", "RequestID": "3siZRSU4"}, "ShopUse": {"Url": "w76ThDMm.php", "EncodeKey": "ZT0Ua4wL", "RequestID": "73SD2aMR"}, "MedalExchange": {"Url": "0X8Fpjhb.php", "EncodeKey": "dCja1E54", "RequestID": "LiM9Had2"}, "DmgRankStart": {"Url": "j37Vk5xe.php", "EncodeKey": "1d5AP9p6", "RequestID": "5P6ULvjg"}, "PurchaseStart": {"Url": "tPc64qmn.php", "EncodeKey": "9Kf4gYvm", "RequestID": "qAUzP3R6"}, "TrophyReward": {"Url": "05vJDxg9.php", "EncodeKey": "2o7kErn1", "RequestID": "wukWY4t2"}, "MissionWaveReStart": {"Url": "8m7KNezI.php", "EncodeKey": "M3bYZoU5", "RequestID": "e9RP8Cto"}, "CraftCancel": {"Url": "7WdDLIE4.php", "EncodeKey": "68zcUF3E", "RequestID": "79xDN1Mw"}, "Sacrifice": {"Url": "QBiJEyUt.php", "EncodeKey": "U80FYThX", "RequestID": "7tWdn9zH"}, "CampaignTieup": {"Url": "2u30vqfY.php", "EncodeKey": "72d5UTNC", "RequestID": "mI0Q2YhW"}}'

GL_1WKh6Xqe = 'ver.6.9.6'

lapishostgl = 'lapis-prod.gumi.sg'

after = r'"}}'

jdata = json.loads(jsondata)

headersgl = {
    'host': lapishostgl,
    'Content-type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'CFNetwork/889.9 Darwin/17.2.0',
    'Accept-Language': 'en-us',
    'Accept-Encoding': 'br, gzip, deflate'
}


def final_data_create(requestkey, new_data):
    key = jdata[requestkey]["EncodeKey"].encode().ljust(16, b'\0')
    aes = AESCipher(key)
    new_data = new_data.encode("latin-1")
    final_data = aes.encrypt(new_data)
    final_data_decode = final_data.decode("utf-8")

    final_data = '{"TEAYk6R1":{"ytHoz4E2":"690' + str(random.randint(1000, 9999)) + r'","z5hB3P01":"' + \
                 jdata[requestkey]["RequestID"] + r'"},"t7n6cVWf":{"qrVcDe48":"' + final_data_decode + '"}}'
    return final_data


def Send_URL_Initialize_Get_Info():
    requestkey = "Initialize"

    new_data = r'{"LhVz6aD2":[{"6Nf5risL":"0","io30YcLA":"GT-I9300_android4.4.2","K1G4fBjF":"2","e8Si6TGh":"AgLrGVH1+hpOKzIwQFwBTakVI8wB7O0G6//xrCWzQfEs8BfWHUbzFPAoig5nikZE","1WKh6Xqe":"ver.6.9.9","64anJRhx":"' + getymdt() + '","Y76dKryw":"US","6e4ik6kA":"2373417eb9f43d55","NggnPgQC":"1ac769c9-e5e2-47cc-b24a-f992e8a9a91f"}],"c1qYg84Q":[{"a4hXTIm0":"F_APP_VERSION_AND","wM9AfX6I":"0"},{"a4hXTIm0":"F_RSC_VERSION","wM9AfX6I":"0"},{"a4hXTIm0":"F_MST_VERSION","wM9AfX6I":"0"}]}'

    final_data = final_data_create(requestkey, new_data)
    print(final_data)

    responsex = requests.request("POST",
                                 'https://' + lapishostgl + '/lapisProd/app/php/gme/actionSymbol/' + jdata[requestkey][
                                     "Url"], data=final_data, headers=headersgl)
    if responsex:
        print(responsex)
        dump = responsex.json()
        dump = json.dumps(dump)
        dump = str(dump)
        matchid2 = re.search(r'"t7n6cVWf": \{"qrVcDe48": "([^"]*)', dump)
        if matchid2:
            dump = matchid2.group(1)
        # print(dump)
        elif "SERVER_MSG_" in dump:
            print(dump)
            print("\n\nTrying Again, Some Error!!!\n\n")

        else:
            print(dump)
            print("\n\nTrying Again, Not Sure What Went Wrong!!!\n\n")

        data = dump.encode("latin-1")

        key = jdata[requestkey]["EncodeKey"].encode().ljust(16, b'\0')
        aes = AESCipher(key)

        decoded_data_response = aes.decrypt(data)
        ui = decoded_data_response.decode("utf-8")
        print(ui)

        # New_qrVcDe48 = re.search(r'"qrVcDe48":"([^"]*)"', ui)
        # if New_qrVcDe48:
        #	New_qrVcDe48 = New_qrVcDe48.group(1)
        #	print(New_qrVcDe48)
        # else:
        #	New_qrVcDe48 = ""

        # F_APP_VERSION_IOS

        GL_F_APP_VERSION_AND = re.search(r'"F_APP_VERSION_AND","wM9AfX6I":"([^"]*)"', ui)
        if GL_F_APP_VERSION_AND:
            GL_F_APP_VERSION_AND = GL_F_APP_VERSION_AND.group(1)
            print(GL_F_APP_VERSION_AND)
        else:
            GL_F_APP_VERSION_AND = "0"

        requestkey = "Initialize"

        new_data = r'{"LhVz6aD2":[{"6Nf5risL":"0","io30YcLA":"GT-I9300_android4.4.2","K1G4fBjF":"2","e8Si6TGh":"AgLrGVH1+hpOKzIwQFwBTakVI8wB7O0G6//xrCWzQfEs8BfWHUbzFPAoig5nikZE","1WKh6Xqe":"ver.6.9.9","64anJRhx":"' + getymdt() + '","Y76dKryw":"US","6e4ik6kA":"2373417eb9f43d55","NggnPgQC":"1ac769c9-e5e2-47cc-b24a-f992e8a9a91f"}],"c1qYg84Q":[{"a4hXTIm0":"F_APP_VERSION_AND","wM9AfX6I":"' + GL_F_APP_VERSION_AND + '"},{"a4hXTIm0":"F_RSC_VERSION","wM9AfX6I":"0"},{"a4hXTIm0":"F_MST_VERSION","wM9AfX6I":"0"}]}'

        final_data = final_data_create(requestkey, new_data)
        print(final_data)

        responsex = requests.request("POST", 'https://' + lapishostgl + '/lapisProd/app/php/gme/actionSymbol/' +
                                     jdata[requestkey]["Url"], data=final_data, headers=headersgl)
        if responsex:
            print(responsex)
            dump = responsex.json()
            dump = json.dumps(dump)
            dump = str(dump)
            matchid2 = re.search(r'"t7n6cVWf": \{"qrVcDe48": "([^"]*)', dump)
            if matchid2:
                dump = matchid2.group(1)
            # print(dump)
            elif "SERVER_MSG_" in dump:
                print(dump)
                print("\n\nTrying Again, Some Error!!!\n\n")

            else:
                print(dump)
                print("\n\nTrying Again, Not Sure What Went Wrong!!!\n\n")

            data = dump.encode("latin-1")

            key = jdata[requestkey]["EncodeKey"].encode().ljust(16, b'\0')
            aes = AESCipher(key)

            decoded_data_response = aes.decrypt(data)
            ui = decoded_data_response.decode("utf-8")
            print(ui)

            New_qrVcDe48 = re.search(r'"qrVcDe48":"([^"]*)"', ui)
            if New_qrVcDe48:
                New_qrVcDe48 = New_qrVcDe48.group(1)
                print(New_qrVcDe48)
            else:
                New_qrVcDe48 = ""

            GL_F_MST_VERSION = re.search(r'"F_MST_VERSION","wM9AfX6I":"([^"]*)"', ui)
            if GL_F_MST_VERSION:
                GL_F_MST_VERSION = GL_F_MST_VERSION.group(1)
                print(GL_F_MST_VERSION)
            else:
                GL_F_MST_VERSION = ""

            GL_c1qYg84Q = 'c1qYg84Q":[{"a4hXTIm0":"F_RSC_VERSION","wM9AfX6I":"0"}]}'

            # Info = {'qrVcDe48': New_qrVcDe48,'6Nf5risL': GL_6Nf5risL,'mESKDlqL': GL_mESKDlqL,'iVN1HD3p': GL_iVN1HD3p,'Y76dKryw': GL_Y76dKryw,'6e4ik6kA': GL_6e4ik6kA,'NggnPgQC': GL_NggnPgQC,'9K0Pzcpd': GL_9K0Pzcpd,'io30YcLA': GL_io30YcLA,'9qh17ZUf': GL_9qh17ZUf,'e8Si6TGh': GL_e8Si6TGh,'m3Wghr1j': GL_m3Wghr1j,'JC61TPqS': GL_JC61TPqS,'9Tbns0eI': GL_9Tbns0eI,'c1qYg84Q': GL_c1qYg84Q}

            return GL_c1qYg84Q


def Send_URL_Initialize(FB_ID, FB_Token, Device_OS):
    GL_e8Si6TGh = 'ffbe6969-569e-69aa-6969-ff' + datetime.datetime.now().strftime("%S")

    GL_e8Si6TGh_BU = GL_e8Si6TGh

    # GL_9K0Pzcpd = re.search(r'"F_APP_VERSION_AND","wM9AfX6I":"([^"]*)"', GL_c1qYg84Q)
    # if GL_9K0Pzcpd:
    #	GL_9K0Pzcpd = GL_9K0Pzcpd.group(1)
    #	print(GL_9K0Pzcpd)
    # else:
    #	GL_9K0Pzcpd = "1069"

    requestkey = "Initialize"

    if int(Device_OS) == 1:
        new_data = r'{"LhVz6aD2":[{"9Tbns0eI":"Npz69kjv69VT","9qh17ZUf":"nope","JC61TPqS":"CWEW69Kc69Hx","6Nf5risL":"","io30YcLA":"iPhone10,6_ios11.1.2","K1G4fBjF":"1","e8Si6TGh":"' + GL_e8Si6TGh + '","1WKh6Xqe":"ver.6.9.6","64anJRhx":"' + getymdt() + '","Y76dKryw":"US","6e4ik6kA":"","m3Wghr1j":"225569121","ma6Ac53v":"0","D2I1Vtog":"0","mESKDlqL":"","iVN1HD3p":"","Y76dKryw":"US","6e4ik6kA":"","NggnPgQC":"","X6jT6zrQ":"' + FB_ID + '","DOFV3qRF":"' + FB_Token + '"}],"Euv8cncS":[{"K2jzG6bp":"1"}],"QCcFB3h9":[{"qrVcDe48":"iPTllGUnX1fS"}],"' + GL_c1qYg84Q
    else:
        new_data = r'{"LhVz6aD2":[{"9Tbns0eI":"Npz69kjv69VT","9qh17ZUf":"nope","JC61TPqS":"CWEW69Kc69Hx","6Nf5risL":"","io30YcLA":"GT-I9300_android4.4.2","K1G4fBjF":"2","e8Si6TGh":"' + GL_e8Si6TGh + '","1WKh6Xqe":"ver.6.9.6","64anJRhx":"' + getymdt() + '","Y76dKryw":"US","6e4ik6kA":"","m3Wghr1j":"225569121","ma6Ac53v":"0","D2I1Vtog":"0","mESKDlqL":"","iVN1HD3p":"","Y76dKryw":"US","6e4ik6kA":"","NggnPgQC":"","X6jT6zrQ":"' + FB_ID + '","DOFV3qRF":"' + FB_Token + '"}],"Euv8cncS":[{"K2jzG6bp":"1"}],"QCcFB3h9":[{"qrVcDe48":"iPTllGUnX1fS"}],"' + GL_c1qYg84Q

    final_data = final_data_create(requestkey, new_data)
    print(new_data)

    responsex = requests.request("POST",
                                 'https://' + lapishostgl + '/lapisProd/app/php/gme/actionSymbol/' + jdata[requestkey][
                                     "Url"], data=final_data, headers=headersgl)
    if responsex:
        print(responsex)
        dump = responsex.json()
        dump = json.dumps(dump)
        dump = str(dump)
        matchid2 = re.search(r'"t7n6cVWf": \{"qrVcDe48": "([^"]*)', dump)
        if matchid2:
            dump = matchid2.group(1)
        # print(dump)
        elif "SERVER_MSG_" in dump:
            print(dump)
            print("\n\nTrying Again, Some Error!!!\n\n")

        else:
            print(dump)
            print("\n\nTrying Again, Not Sure What Went Wrong!!!\n\n")

        data = dump.encode("latin-1")

        key = jdata[requestkey]["EncodeKey"].encode().ljust(16, b'\0')
        aes = AESCipher(key)

        decoded_data_response = aes.decrypt(data)
        ui = decoded_data_response.decode("utf-8")
        print(ui)

        New_qrVcDe48 = re.search(r'"qrVcDe48":"([^"]*)"', ui)
        if New_qrVcDe48:
            New_qrVcDe48 = New_qrVcDe48.group(1)
            print(New_qrVcDe48)
        else:
            New_qrVcDe48 = ""

        GL_K1G4fBjF = re.search(r'"K1G4fBjF":"([^"]*)"', ui)
        if GL_K1G4fBjF:
            GL_K1G4fBjF = GL_K1G4fBjF.group(1)
            print(GL_K1G4fBjF)
        else:
            GL_K1G4fBjF = Device_OS

        GL_6Nf5risL = re.search(r'"6Nf5risL":"([^"]*)"', ui)
        if GL_6Nf5risL:
            GL_6Nf5risL = GL_6Nf5risL.group(1)
            print(GL_6Nf5risL)
        else:
            GL_6Nf5risL = ""

        GL_mESKDlqL = re.search(r'"mESKDlqL":"([^"]*)"', ui)
        if GL_mESKDlqL:
            GL_mESKDlqL = GL_mESKDlqL.group(1)
            print(GL_mESKDlqL)
        else:
            GL_mESKDlqL = ""

        GL_iVN1HD3p = re.search(r'"iVN1HD3p":"([^"]*)"', ui)
        if GL_iVN1HD3p:
            GL_iVN1HD3p = GL_iVN1HD3p.group(1)
            print(GL_iVN1HD3p)
        else:
            GL_iVN1HD3p = ""

        GL_Y76dKryw = re.search(r'"Y76dKryw":"([^"]*)"', ui)
        if GL_Y76dKryw:
            GL_Y76dKryw = GL_Y76dKryw.group(1)
            print(GL_Y76dKryw)
        else:
            GL_Y76dKryw = ""

        GL_6e4ik6kA = re.search(r'"6e4ik6kA":"([^"]*)"', ui)
        if GL_6e4ik6kA:
            GL_6e4ik6kA = GL_6e4ik6kA.group(1)
            print(GL_6e4ik6kA)
        else:
            GL_6e4ik6kA = ""

        GL_NggnPgQC = re.search(r'"NggnPgQC":"([^"]*)"', ui)
        if GL_NggnPgQC:
            GL_NggnPgQC = GL_NggnPgQC.group(1)
            print(GL_NggnPgQC)
        else:
            GL_NggnPgQC = ""

        GL_9K0Pzcpd = re.search(r'"9K0Pzcpd":"([^"]*)"', ui)
        if GL_9K0Pzcpd:
            GL_9K0Pzcpd = GL_9K0Pzcpd.group(1)
            print(GL_9K0Pzcpd)
        else:
            GL_9K0Pzcpd = ""

        GL_io30YcLA = re.search(r'"io30YcLA":"([^"]*)"', ui)
        if GL_io30YcLA:
            GL_io30YcLA = GL_io30YcLA.group(1)
            print(GL_io30YcLA)
        else:
            GL_io30YcLA = ""

        GL_9qh17ZUf = re.search(r'"9qh17ZUf":"([^"]*)"', ui)
        if GL_9qh17ZUf:
            GL_9qh17ZUf = GL_9qh17ZUf.group(1)
            print(GL_9qh17ZUf)
        else:
            GL_9qh17ZUf = ""

        GL_e8Si6TGh = re.search(r'"e8Si6TGh":"([^"]*)"', ui)
        if GL_e8Si6TGh:
            GL_e8Si6TGh = GL_e8Si6TGh.group(1)
            print(GL_e8Si6TGh)
        else:
            GL_e8Si6TGh = GL_e8Si6TGh_BU

        if len(GL_e8Si6TGh) <= 2:
            GL_e8Si6TGh = GL_e8Si6TGh_BU

        GL_m3Wghr1j = re.search(r'"m3Wghr1j":"([^"]*)"', ui)
        if GL_m3Wghr1j:
            GL_m3Wghr1j = GL_m3Wghr1j.group(1)
            print(GL_m3Wghr1j)
        else:
            GL_m3Wghr1j = ""

        GL_JC61TPqS = re.search(r'"JC61TPqS":"([^"]*)"', ui)
        if GL_JC61TPqS:
            GL_JC61TPqS = GL_JC61TPqS.group(1)
            print(GL_JC61TPqS)
        else:
            GL_JC61TPqS = ""

        GL_9Tbns0eI = re.search(r'"9Tbns0eI":"([^"]*)"', ui)
        if GL_9Tbns0eI:
            GL_9Tbns0eI = GL_9Tbns0eI.group(1)
            print(GL_9Tbns0eI)
        else:
            GL_9Tbns0eI = ""

        GL_1WKh6Xqe = re.search(r'"1WKh6Xqe":"([^"]*)"', ui)
        if GL_1WKh6Xqe:
            GL_1WKh6Xqe = GL_1WKh6Xqe.group(1)
            print(GL_1WKh6Xqe)
        else:
            GL_1WKh6Xqe = "ver.6.9.6"
        if len(GL_1WKh6Xqe) <= 2:
            GL_1WKh6Xqe = "ver.6.9.6"

        GL_X6jT6zrQ = re.search(r'"X6jT6zrQ":"([^"]*)"', ui)
        if GL_X6jT6zrQ:
            GL_X6jT6zrQ = GL_X6jT6zrQ.group(1)
            print(GL_X6jT6zrQ)
        else:
            GL_X6jT6zrQ = FB_ID

        GL_DOFV3qRF = re.search(r'"DOFV3qRF":"([^"]*)"', ui)
        if GL_DOFV3qRF:
            GL_DOFV3qRF = GL_DOFV3qRF.group(1)
            print(GL_DOFV3qRF)
        else:
            GL_DOFV3qRF = FB_Token

        GL_F_MST_VERSION = re.search(r'"F_MST_VERSION","wM9AfX6I":"([^"]*)"', ui)
        if GL_F_MST_VERSION:
            GL_F_MST_VERSION = GL_F_MST_VERSION.group(1)
            print(GL_F_MST_VERSION)
        else:
            GL_F_MST_VERSION = ""

        Info = {'qrVcDe48': New_qrVcDe48, '6Nf5risL': GL_6Nf5risL, 'mESKDlqL': GL_mESKDlqL, 'iVN1HD3p': GL_iVN1HD3p,
                'Y76dKryw': GL_Y76dKryw, '6e4ik6kA': GL_6e4ik6kA, 'NggnPgQC': GL_NggnPgQC, '9K0Pzcpd': GL_9K0Pzcpd,
                'io30YcLA': GL_io30YcLA, '9qh17ZUf': GL_9qh17ZUf, 'e8Si6TGh': GL_e8Si6TGh, 'm3Wghr1j': GL_m3Wghr1j,
                'JC61TPqS': GL_JC61TPqS, '9Tbns0eI': GL_9Tbns0eI, '1WKh6Xqe': GL_1WKh6Xqe, 'K1G4fBjF': GL_K1G4fBjF,
                'X6jT6zrQ': GL_X6jT6zrQ, 'DOFV3qRF': GL_DOFV3qRF}

        return Info


def Send_URL_GetUserInfo(FB_ID, FB_Token, Device_OS, Info):
    requestkey = "GetUserInfo"

    new_data = r'{"LhVz6aD2":[{"9Tbns0eI":"' + Info['9Tbns0eI'] + '","9qh17ZUf":"' + Info[
        '9qh17ZUf'] + '","JC61TPqS":"' + Info['JC61TPqS'] + '","6Nf5risL":"' + Info['6Nf5risL'] + '","io30YcLA":"' + \
               Info['io30YcLA'] + '","K1G4fBjF":"' + Info['K1G4fBjF'] + '","e8Si6TGh":"' + Info[
                   'e8Si6TGh'] + '","1WKh6Xqe":"' + Info['1WKh6Xqe'] + '","64anJRhx":"' + getymdt() + '","m3Wghr1j":"' + \
               Info['m3Wghr1j'] + '","ma6Ac53v":"0","D2I1Vtog":"' + getymd() + '","9K0Pzcpd":"' + Info[
                   '9K0Pzcpd'] + '","mESKDlqL":"' + Info['mESKDlqL'] + '","iVN1HD3p":"' + Info[
                   'iVN1HD3p'] + '","Y76dKryw":"' + Info['Y76dKryw'] + '","6e4ik6kA":"' + Info[
                   '6e4ik6kA'] + '","NggnPgQC":"' + Info[
                   'NggnPgQC'] + '","X6jT6zrQ":"' + FB_ID + '","DOFV3qRF":"' + FB_Token + '"}],"Euv8cncS":[{"K2jzG6bp":"1"}],"QCcFB3h9":[{"qrVcDe48":"' + \
               Info['qrVcDe48'] + '"}],"' + GL_c1qYg84Q

    print(new_data)

    final_data = final_data_create(requestkey, new_data)
    # print(final_data)

    responsex = requests.request("POST",
                                 'https://' + lapishostgl + '/lapisProd/app/php/gme/actionSymbol/' + jdata[requestkey][
                                     "Url"], data=final_data, headers=headersgl)
    if responsex:
        print(responsex)
        dump = responsex.json()
        dump = json.dumps(dump)
        dump = str(dump)
        matchid2 = re.search(r'"t7n6cVWf": \{"qrVcDe48": "([^"]*)', dump)
        if matchid2:
            dump = matchid2.group(1)
        # print(dump)
        elif "SERVER_MSG_" in dump:
            print(dump)
            print("\n\nTrying Again, Some Error!!!\n\n")

        else:
            print(dump)
            print("\n\nTrying Again, Not Sure What Went Wrong!!!\n\n")

        data = dump.encode("latin-1")

        key = jdata[requestkey]["EncodeKey"].encode().ljust(16, b'\0')
        aes = AESCipher(key)

        decoded_data_response = aes.decrypt(data)
        ui = decoded_data_response.decode("utf-8")
        # print(ui)
        ui_json = json.loads(ui)

        New_qrVcDe48 = re.search(r'"qrVcDe48":"([^"]*)"', ui)
        if New_qrVcDe48:
            New_qrVcDe48 = New_qrVcDe48.group(1)
            print(New_qrVcDe48)
        else:
            New_qrVcDe48 = ""

        try:
            AccountLvL = 'NULL'
            AccountGil = 'NULL'
            AccountNRG = 'NULL'

            AccountName = 'NULL'
            AccountFriendID = 'NULL'

            Account_Lapis = 'NULL'

            Account_NRG_Pots = 'NULL'

            AccountLvL = ui_json['3oU9Ktb7'][0]['7wV3QZ80']
            AccountGil = ui_json['3oU9Ktb7'][0]['7UR4J2SE']
            AccountNRG = ui_json['3oU9Ktb7'][0]['B6kyCQ9M']

            AccountName = ui_json['LhVz6aD2'][0]['9qh17ZUf']
            AccountFriendID = ui_json['LhVz6aD2'][0]['m3Wghr1j']

            Account_Lapis = str(int(ui_json['J3pAG0I5'][0]['T7sah9rc']) + int(ui_json['J3pAG0I5'][0]['cb3WmiD0']))

            for onehund in ui_json['Md0N5abE']:
                if onehund['2dfixko3'] == '100':
                    Account_NRG_Pots = onehund['Qy5EvcK1']

            print(AccountLvL)
            print(AccountGil)
            print(AccountNRG)
            print(AccountName)
            print(AccountFriendID)
            print(Account_Lapis)
            print(Account_NRG_Pots)



        except:
            print('ACCOUNT INFO ERROR')

        try:
            unit_dict = {i["og2GHy49"]: {'UnitName': Unit_Name_Dict_Lookup[i["3HriTp6B"]], 'UnitSID': i["og2GHy49"],
                                         'UnitID': i["3HriTp6B"], 'ULevel': i["7wV3QZ80"], 'UTrust': i["f17L8wuX"]} for
                         i in ui_json["B71MekS8"]}
            # print(unit_dict)

            party_name_1 = ui_json['5Eb0Rig6'][0]['G4L0YIB2']
            party_1 = ui_json['5Eb0Rig6'][0]['2A6fYiEC']
            party_1_Dict = {}
            for Match_Unit_Server_ID in re.finditer('(\d{11}\d*)', party_1):
                if Match_Unit_Server_ID:
                    Unit_Server_ID = Match_Unit_Server_ID.group(1)
                    party_1_Dict[Unit_Server_ID] = unit_dict[Unit_Server_ID]
            # print(party_1_Dict)

            party_name_2 = ui_json['5Eb0Rig6'][1]['G4L0YIB2']
            party_2 = ui_json['5Eb0Rig6'][1]['2A6fYiEC']
            party_2_Dict = {}
            for Match_Unit_Server_ID in re.finditer('(\d{11}\d*)', party_2):
                if Match_Unit_Server_ID:
                    Unit_Server_ID = Match_Unit_Server_ID.group(1)
                    party_2_Dict[Unit_Server_ID] = unit_dict[Unit_Server_ID]
            # print(party_2_Dict)

            party_name_3 = ui_json['5Eb0Rig6'][2]['G4L0YIB2']
            party_3 = ui_json['5Eb0Rig6'][2]['2A6fYiEC']
            party_3_Dict = {}
            party_3_Name_List = []
            for Match_Unit_Server_ID in re.finditer('(\d{11}\d*)', party_3):
                if Match_Unit_Server_ID:
                    Unit_Server_ID = Match_Unit_Server_ID.group(1)
                    party_3_Dict[Unit_Server_ID] = unit_dict[Unit_Server_ID]
            # print(party_3_Dict)

            party_name_4 = ui_json['5Eb0Rig6'][3]['G4L0YIB2']
            party_4 = ui_json['5Eb0Rig6'][3]['2A6fYiEC']
            party_4_Dict = {}
            party_4_Name_List = []
            for Match_Unit_Server_ID in re.finditer('(\d{11}\d*)', party_4):
                if Match_Unit_Server_ID:
                    Unit_Server_ID = Match_Unit_Server_ID.group(1)
                    party_4_Dict[Unit_Server_ID] = unit_dict[Unit_Server_ID]
            # print(party_4_Dict)

            party_name_5 = ui_json['5Eb0Rig6'][4]['G4L0YIB2']
            party_5 = ui_json['5Eb0Rig6'][4]['2A6fYiEC']
            party_5_Dict = {}
            party_5_Name_List = []
            for Match_Unit_Server_ID in re.finditer('(\d{11}\d*)', party_5):
                if Match_Unit_Server_ID:
                    Unit_Server_ID = Match_Unit_Server_ID.group(1)
                    party_5_Dict[Unit_Server_ID] = unit_dict[Unit_Server_ID]
        # print(party_5_Dict)

        except:
            print('PARTY ERROR')

        Info['qrVcDe48'] = New_qrVcDe48

        print('updating qrVcDe48 to: ' + New_qrVcDe48)

        GetInfo = {'PARTY1': {party_name_1: party_1_Dict}, 'PARTY2': {party_name_2: party_2_Dict},
                   'PARTY3': {party_name_3: party_3_Dict}, 'PARTY4': {party_name_4: party_4_Dict},
                   'PARTY5': {party_name_5: party_5_Dict}, 'AccountLvL': AccountLvL, 'AccountGil': AccountGil,
                   'AccountName': AccountName, 'AccountFriendID': AccountFriendID, 'Account_Lapis': Account_Lapis,
                   'Account_NRG_Pots': Account_NRG_Pots, 'AccountNRG': AccountNRG}

        return GetInfo


def Send_URL_StartWaveMission(FB_ID, FB_Token, Device_OS, Info, WithFriend, MissionID):
    requestkey = "MissionWaveStart"

    if WithFriend >= 1:

        new_data = r'{"jQsE54Iz":[{"qo3PECw6":"' + MissionID + '","w40YsHIz":"789149261","0XUs3Tv6":"0","qLke7K8f":"100012505","xojJ2w0S":"0"}],"LhVz6aD2":[{"9Tbns0eI":"' + \
                   Info['9Tbns0eI'] + '","9qh17ZUf":"' + Info['9qh17ZUf'] + '","JC61TPqS":"' + Info[
                       'JC61TPqS'] + '","6Nf5risL":"' + Info['6Nf5risL'] + '","io30YcLA":"' + Info[
                       'io30YcLA'] + '","K1G4fBjF":"' + Info['K1G4fBjF'] + '","e8Si6TGh":"' + Info[
                       'e8Si6TGh'] + '","1WKh6Xqe":"' + Info[
                       '1WKh6Xqe'] + '","64anJRhx":"' + getymdt() + '","m3Wghr1j":"' + Info[
                       'm3Wghr1j'] + '","ma6Ac53v":"0","D2I1Vtog":"' + getymd() + '","9K0Pzcpd":"' + Info[
                       '9K0Pzcpd'] + '","mESKDlqL":"' + Info['mESKDlqL'] + '","iVN1HD3p":"' + Info[
                       'iVN1HD3p'] + '","Y76dKryw":"' + Info['Y76dKryw'] + '","6e4ik6kA":"' + Info[
                       '6e4ik6kA'] + '","NggnPgQC":"' + Info[
                       'NggnPgQC'] + '","X6jT6zrQ":"' + FB_ID + '","DOFV3qRF":"' + FB_Token + '"}],"Euv8cncS":[{"K2jzG6bp":"1"}],"QCcFB3h9":[{"qrVcDe48":"' + \
                   Info['qrVcDe48'] + '"}],"' + GL_c1qYg84Q
    else:
        new_data = r'{"jQsE54Iz":[{"qo3PECw6":"' + MissionID + '"}],"LhVz6aD2":[{"9Tbns0eI":"' + Info[
            '9Tbns0eI'] + '","9qh17ZUf":"' + Info['9qh17ZUf'] + '","JC61TPqS":"' + Info['JC61TPqS'] + '","6Nf5risL":"' + \
                   Info['6Nf5risL'] + '","io30YcLA":"' + Info['io30YcLA'] + '","K1G4fBjF":"' + Info[
                       'K1G4fBjF'] + '","e8Si6TGh":"' + Info['e8Si6TGh'] + '","1WKh6Xqe":"' + Info[
                       '1WKh6Xqe'] + '","64anJRhx":"' + getymdt() + '","m3Wghr1j":"' + Info[
                       'm3Wghr1j'] + '","ma6Ac53v":"0","D2I1Vtog":"' + getymd() + '","9K0Pzcpd":"' + Info[
                       '9K0Pzcpd'] + '","mESKDlqL":"' + Info['mESKDlqL'] + '","iVN1HD3p":"' + Info[
                       'iVN1HD3p'] + '","Y76dKryw":"' + Info['Y76dKryw'] + '","6e4ik6kA":"' + Info[
                       '6e4ik6kA'] + '","NggnPgQC":"' + Info[
                       'NggnPgQC'] + '","X6jT6zrQ":"' + FB_ID + '","DOFV3qRF":"' + FB_Token + '"}],"Euv8cncS":[{"K2jzG6bp":"1"}],"QCcFB3h9":[{"qrVcDe48":"' + \
                   Info['qrVcDe48'] + '"}],"' + GL_c1qYg84Q

    print(new_data)

    final_data = final_data_create(requestkey, new_data)
    # print(final_data)

    responsex = requests.request("POST",
                                 'https://' + lapishostgl + '/lapisProd/app/php/gme/actionSymbol/' + jdata[requestkey][
                                     "Url"], data=final_data, headers=headersgl)
    if responsex:
        print(responsex)
        dump = responsex.json()
        dump = json.dumps(dump)
        dump = str(dump)
        matchid2 = re.search(r'"t7n6cVWf": \{"qrVcDe48": "([^"]*)', dump)
        if matchid2:
            dump = matchid2.group(1)
        # print(dump)
        elif "SERVER_MSG_" in dump:
            print(dump)
            print("\n\nTrying Again, Some Error!!!\n\n")

        else:
            print(dump)
            print("\n\nTrying Again, Not Sure What Went Wrong!!!\n\n")

        data = dump.encode("latin-1")

        key = jdata[requestkey]["EncodeKey"].encode().ljust(16, b'\0')
        aes = AESCipher(key)

        decoded_data_response = aes.decrypt(data)
        ui = decoded_data_response.decode("utf-8")
        print(ui)

        New_qrVcDe48 = re.search(r'"qrVcDe48":"([^"]*)"', ui)
        if New_qrVcDe48:
            New_qrVcDe48 = New_qrVcDe48.group(1)
            print(New_qrVcDe48)
        else:
            New_qrVcDe48 = ""

        Info['qrVcDe48'] = New_qrVcDe48

        print('updating qrVcDe48 to: ' + New_qrVcDe48)


def Send_URL_MissionEnd(FB_ID, FB_Token, Device_OS, Info, WithFriend, MissionID, GetInfo):
    requestkey = "MissionEnd"

    if WithFriend >= 1:

        new_data = r'{"jQsE54Iz":[{"qo3PECw6":"' + MissionID + '","w40YsHIz":"789149261"}],"LhVz6aD2":[{"9Tbns0eI":"' + \
                   Info['9Tbns0eI'] + '","9qh17ZUf":"' + Info['9qh17ZUf'] + '","JC61TPqS":"' + Info[
                       'JC61TPqS'] + '","6Nf5risL":"' + Info['6Nf5risL'] + '","io30YcLA":"' + Info[
                       'io30YcLA'] + '","K1G4fBjF":"' + Info['K1G4fBjF'] + '","e8Si6TGh":"' + Info[
                       'e8Si6TGh'] + '","1WKh6Xqe":"' + Info[
                       '1WKh6Xqe'] + '","64anJRhx":"' + getymdt() + '","m3Wghr1j":"' + Info[
                       'm3Wghr1j'] + '","ma6Ac53v":"0","D2I1Vtog":"' + getymd() + '","9K0Pzcpd":"' + Info[
                       '9K0Pzcpd'] + '","mESKDlqL":"' + Info['mESKDlqL'] + '","iVN1HD3p":"' + Info[
                       'iVN1HD3p'] + '","Y76dKryw":"' + Info['Y76dKryw'] + '","6e4ik6kA":"' + Info[
                       '6e4ik6kA'] + '","NggnPgQC":"' + Info[
                       'NggnPgQC'] + '","X6jT6zrQ":"' + FB_ID + '","DOFV3qRF":"' + FB_Token + '"}],"Euv8cncS":[{"K2jzG6bp":"1"}],"QCcFB3h9":[{"qrVcDe48":"' + \
                   Info[
                       'qrVcDe48'] + '"}],"09HRWXDf":[{"S4U09svH":"8","ZGSr7T06":"0","Wdi3MAs2":"4","Syar71nw":"0","8CfoLQv5":"0","wQhu9G7n":"0","xF9Sr1a6":"20:202000400:1,20:290020500:1","7a1Ugx4e":"0","t4v2o0zM":"0","PB3vLE2r":"0","PB3vLE2r":"0","aK4k1PvY":"0","NCFk6Zv1":"0","nar74pDu":"1010010","f6M1cJgk":"101001000:2","uU21m4ry":"101001000:1"}],"nE7pV2wr":[{"jsvoa0I2":"0:101000100:3"}],"nSG9Jb1s":[{"NYb0Cri6":"MAX_CHAIN_TURN","6gAX1BpC":"10"},{"NYb0Cri6":"MAX_LB_CRISTAL","6gAX1BpC":"18"},{"NYb0Cri6":"MAX_DAMAGE_HIT","6gAX1BpC":"1242"},{"NYb0Cri6":"TOTAL_LB_CRISTAL","6gAX1BpC":"35"},{"NYb0Cri6":"TOTAL_DAMAGE","6gAX1BpC":"2371"},{"NYb0Cri6":"TOTAL_MISSION_BATTLE_WIN","6gAX1BpC":"2"},{"NYb0Cri6":"MAX_SPARK_CHAIN_TURN","6gAX1BpC":"0"},{"NYb0Cri6":"MAX_ELEMENT_CHAIN_TURN","6gAX1BpC":"0"},{"NYb0Cri6":"MAX_DAMAGE_TURN","6gAX1BpC":"1358"}],"2urzfX6d":[{"Z1p0j9uF":"0","69ieJGhD":"1:111010101:1,2:111010101:1","vMo5cnmx":"101001000:0:0"}],"L4i4418y":[{"6q35TL07":"0"}],"' + GL_c1qYg84Q

    else:
        new_data = r'{"jQsE54Iz":[{"qo3PECw6":"' + MissionID + '"}],"LhVz6aD2":[{"9Tbns0eI":"' + Info[
            '9Tbns0eI'] + '","9qh17ZUf":"' + Info['9qh17ZUf'] + '","JC61TPqS":"' + Info['JC61TPqS'] + '","6Nf5risL":"' + \
                   Info['6Nf5risL'] + '","io30YcLA":"' + Info['io30YcLA'] + '","K1G4fBjF":"' + Info[
                       'K1G4fBjF'] + '","e8Si6TGh":"' + Info['e8Si6TGh'] + '","1WKh6Xqe":"' + Info[
                       '1WKh6Xqe'] + '","64anJRhx":"' + getymdt() + '","m3Wghr1j":"' + Info[
                       'm3Wghr1j'] + '","ma6Ac53v":"0","D2I1Vtog":"' + getymd() + '","9K0Pzcpd":"' + Info[
                       '9K0Pzcpd'] + '","mESKDlqL":"' + Info['mESKDlqL'] + '","iVN1HD3p":"' + Info[
                       'iVN1HD3p'] + '","Y76dKryw":"' + Info['Y76dKryw'] + '","6e4ik6kA":"' + Info[
                       '6e4ik6kA'] + '","NggnPgQC":"' + Info[
                       'NggnPgQC'] + '","X6jT6zrQ":"' + FB_ID + '","DOFV3qRF":"' + FB_Token + '"}],"Euv8cncS":[{"K2jzG6bp":"1"}],"QCcFB3h9":[{"qrVcDe48":"' + \
                   Info[
                       'qrVcDe48'] + '"}],"09HRWXDf":[{"S4U09svH":"8","ZGSr7T06":"0","Wdi3MAs2":"4","Syar71nw":"0","8CfoLQv5":"0","wQhu9G7n":"0","xF9Sr1a6":"20:202000400:1,20:290020500:1","7a1Ugx4e":"0","t4v2o0zM":"0","PB3vLE2r":"0","PB3vLE2r":"0","aK4k1PvY":"0","NCFk6Zv1":"0","nar74pDu":"1010010","f6M1cJgk":"101001000:2","uU21m4ry":"101001000:1"}],"nE7pV2wr":[{"jsvoa0I2":"0:101000100:3"}],"nSG9Jb1s":[{"NYb0Cri6":"MAX_CHAIN_TURN","6gAX1BpC":"10"},{"NYb0Cri6":"MAX_LB_CRISTAL","6gAX1BpC":"18"},{"NYb0Cri6":"MAX_DAMAGE_HIT","6gAX1BpC":"1242"},{"NYb0Cri6":"TOTAL_LB_CRISTAL","6gAX1BpC":"35"},{"NYb0Cri6":"TOTAL_DAMAGE","6gAX1BpC":"2371"},{"NYb0Cri6":"TOTAL_MISSION_BATTLE_WIN","6gAX1BpC":"2"},{"NYb0Cri6":"MAX_SPARK_CHAIN_TURN","6gAX1BpC":"0"},{"NYb0Cri6":"MAX_ELEMENT_CHAIN_TURN","6gAX1BpC":"0"},{"NYb0Cri6":"MAX_DAMAGE_TURN","6gAX1BpC":"1358"}],"2urzfX6d":[{"Z1p0j9uF":"0","69ieJGhD":"1:111010101:1,2:111010101:1","vMo5cnmx":"101001000:0:0"}],"L4i4418y":[{"6q35TL07":"0"}],"' + GL_c1qYg84Q

    print(new_data)

    final_data = final_data_create(requestkey, new_data)
    # print(final_data)

    responsex = requests.request("POST",
                                 'https://' + lapishostgl + '/lapisProd/app/php/gme/actionSymbol/' + jdata[requestkey][
                                     "Url"], data=final_data, headers=headersgl)
    if responsex:
        print(responsex)
        dump = responsex.json()
        dump = json.dumps(dump)
        dump = str(dump)
        matchid2 = re.search(r'"t7n6cVWf": \{"qrVcDe48": "([^"]*)', dump)
        if matchid2:
            dump = matchid2.group(1)
        # print(dump)
        elif "SERVER_MSG_" in dump:
            print(dump)
            print("\n\nTrying Again, Some Error!!!\n\n")

        else:
            print(dump)
            print("\n\nTrying Again, Not Sure What Went Wrong!!!\n\n")

        data = dump.encode("latin-1")

        key = jdata[requestkey]["EncodeKey"].encode().ljust(16, b'\0')
        aes = AESCipher(key)

        decoded_data_response = aes.decrypt(data)
        ui = decoded_data_response.decode("utf-8")
        print(ui)

        ui_json = json.loads(ui)

        New_qrVcDe48 = re.search(r'"qrVcDe48":"([^"]*)"', ui)
        if New_qrVcDe48:
            New_qrVcDe48 = New_qrVcDe48.group(1)
            print(New_qrVcDe48)
        else:
            New_qrVcDe48 = ""

        try:
            AccountLvL = 'NULL'
            AccountGil = 'NULL'
            AccountNRG = 'NULL'

            Account_Lapis = 'NULL'

            AccountLvL = ui_json['3oU9Ktb7'][0]['7wV3QZ80']
            AccountGil = ui_json['3oU9Ktb7'][0]['7UR4J2SE']
            AccountNRG = ui_json['3oU9Ktb7'][0]['B6kyCQ9M']

            Account_Lapis = str(int(ui_json['J3pAG0I5'][0]['T7sah9rc']) + int(ui_json['J3pAG0I5'][0]['cb3WmiD0']))

            print(AccountLvL)
            print(AccountGil)
            print(AccountNRG)
            print(Account_Lapis)

            GetInfo['AccountLvL'] = AccountLvL
            GetInfo['AccountGil'] = AccountGil
            GetInfo['AccountNRG'] = AccountNRG
            GetInfo['Account_Lapis'] = Account_Lapis

            ACTIVE_PARTY_dict = {
            i["og2GHy49"]: {'UnitName': Unit_Name_Dict_Lookup[i["3HriTp6B"]], 'UnitSID': i["og2GHy49"],
                            'UnitID': i["3HriTp6B"], 'ULevel': i["7wV3QZ80"], 'UTrust': int(i["f17L8wuX"]) / 10} for i
            in ui_json["8gSkPD6b"]}
            # print(unit_dict)

            ACTIVE_PARTY_name = 'ACTIVE_PARTY'

            GetInfo[ACTIVE_PARTY_name] = ACTIVE_PARTY_dict


        except:
            print('ACCOUNT INFO ERROR')

        Info['qrVcDe48'] = New_qrVcDe48

        print('updating qrVcDe48 to: ' + New_qrVcDe48)

        return GetInfo


GL_c1qYg84Q = 'c1qYg84Q":[{"a4hXTIm0":"F_RSC_VERSION","wM9AfX6I":"0"}]}'


# GL_c1qYg84Q = Send_URL_Initialize_Get_Info()

# print(GL_c1qYg84Q)

def start(fb_ID, fb_Token, level):
    Info = Send_URL_Initialize(fb_ID, fb_Token, level)

    print(Info)

    GetInfo = Send_URL_GetUserInfo(fb_ID, fb_Token, '1', Info)

    # print(GetInfo)

    # test = list(GetInfo['PARTY1'].keys())[0]
    party1 = next(iter(GetInfo['PARTY1']))
    # test = GetInfo['PARTY1']
    print(party1)
    print(GetInfo['PARTY1'])

    print(GetInfo['AccountFriendID'])

    print(Info['qrVcDe48'])

    WithFriend = 0

    Send_URL_StartWaveMission(fb_ID, fb_Token, '1', Info, WithFriend, level)

    print(Info['qrVcDe48'])

    time.sleep(9)
    Send_URL_MissionEnd(fb_ID, fb_Token, '1', Info, WithFriend, level, GetInfo)

    print(GetInfo)

    print('Account Level:  ' + GetInfo['AccountLvL'])
    print('Account Lapis:  ' + GetInfo['Account_Lapis'])
    print('Account Gil:  ' + GetInfo['AccountGil'])
    print('Account NRG:  ' + GetInfo['AccountNRG'])

    print('\n\nUnit Info:\n==================\n')
    for keys, values in GetInfo['ACTIVE_PARTY'].items():
        # print(keys)
        print(values['UnitName'] + '\nLEVEL: ' + values['ULevel'] + '\nTRUST %: ' + str(
            int(values['UTrust']) / 100) + '\n==================')

    return GetInfo

# start('545107032526793','EAARmB9evD0cBAFuwsMaevkvb2hnZAraZALSBoGdZA5UdQhlCU3DmZCVfxhY9QGISf5jZCug9FwSnDuP85leCXuSbDuLuflPfX6M9Ia3xRCN9fJb7Yylvc09nmCUrBJS8qHxzuTIAtK2oBTUwKvhjPWCjZAQx2hRcfQTDwCbidiMGCwCipYmr25U1xKUfsZAk0GZBlKO3LarH4rz9D7srTO5sizmEbOlIdqEuIFVTnka7iaFQuXoT0MzJ','1110101')