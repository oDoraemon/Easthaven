#filename:Poker.py
#coding:utf-8
#纸牌的模型

#!Attention 最好写个排序和比较函数，因为A和234以及JQK都很难排序及比较
import random
RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
SUITS = ["S","D","H","C"]
class Card(object):
	def __init__(self, rank, suit): # 生成纸牌，只接收合法输入
		try:	#!Attention 注意检验不合标准的输入
			self.__rank__ = str(rank)
			self.__suit__ = suit
			if rank == "A": # 为纸牌赋值
				self.__value__ = 1
			elif rank in ["J","Q","K"]:
				self.__value__ = 10
			else:
				self.value = int(rank)
		except ValueError:
			print "输入不符合标准!"
		
	def __str__(self):
		return self.__rank__ + self.__suit__
		
	def get_rank(self):
		return self.__rank__
		
	def get_suit(self):
		return self.__suit__

	def get_value(self):
		return self.__value__
	
	def __repr__(self):
		return self.__str__()
		
class Deck(object):
	def __init__(self): # 生成一副牌，按顺序堆放
		self.deck = []
		for cardSuit in SUITS:
			for cardRank in RANKS:
				self.deck.append(Card(cardRank, cardSuit))
					
	def __str__(self): 
		cnt = 0
		theStr = ""
		for card in self.deck:
			theStr += card.__str__() + " "
			cnt += 1
			if cnt % 13 == 0:
				theStr += "\n"
		return theStr
	def __repr__(self):
		return self.__str__()
	
	def shuffle(self): # shuffle the deck
		random.shuffle(self.deck)		
	
	def deal(self): # 将最后一张牌弹出
		if not self.empty():
			card = self.deck.pop(len(self.deck) - 1)
		else: #!Attention 注意处理空值问题
			raise IndexError
		return card
		
	def empty(self): #检查牌堆是否为空
		if len(self.deck) <= 0:
			return True
		else:
			return False
	