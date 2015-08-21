#filename:Easthaven.py
#coding:utf-8
#Windows 上的纸牌游戏，游戏规则见系统

# tableau 和 stock初始化的时候应该是在Game启动时初始化。
# tableau 28张牌， stock24张牌
# 所有有pop()语句的函数，注意检查list为空

# 待考虑的问题还有很多：
# - 异常处理机制
# - 类结构顺序( 主要是没放在类中的方法，变量等的处理，tableau等是否作为独立的模块等)
# - 更完善的功能(如checkAlive， 自动归档，以及触发游戏结束等)

# 虽然多数接口已完成，但如果做成可发布的产品的话，可能只完成了4-50%吧


import Poker

DECK = Deck()

tableau1 =[]
tableau2 =[]
tableau3 =[]
tableau4 =[]
tableau5 =[]
tableau6 =[]
tableau7 =[]

found1=[]
found2=[]
found3=[]
found4=[]

cached = [] #临时存放点击选中及drag的牌
aLive = [] # 保存可以放的牌，如果可以放的牌都不满足addable，则结束


# 
class Game(object):

	# 初始化的时候还是该考虑使用异常机制，确保输入是对的，才能保证游戏正常进行下去
	def __init__(self): # 初始化1个stock，4个foundation，7个tableau
		self.deck = Deck()
		self.deck.shuffle()
		
		 # 初始化stock
		self.stock = stock()
		
		while len(self.stock.hide) < 24:
			self.stock.hide.append(self.deck.pop())
			
		#初始化foundation
		self.found1 = foundation()
		self.found2 = foundation()
		self.found3 = foundation()
		self.found4 = foundation()
		#初始化tableau
		self.tableau1 = tableau()
		self.tableau2 = tableau()
		self.tableau3 = tableau()
		self.tableau4 = tableau()
		self.tableau5 = tableau()
		self.tableau6 = tableau()
		self.tableau7 = tableau()
		

		while len(self.deck) > 0: # 按顺序从左到右分牌 , 背面的牌和正面的牌列表分离
		# !Warning 如果self.deck不小心比28张多，则会出现死循环。怎么办？如果比28张少，初始化未完成即退出。
			if len(self.tableau1.show) < 1:
				self.tableau1.show.append(self.deck.pop())
				
			if len(self.tableau2.show) < 1: # 这一段代码扩展性出乎意料的好，哈哈哈哈
				if len(self.tableau2.hide) == 1:
					self.tableau2.show.append(self.deck.pop())
				else:
					self.tableau2.hide.append(self.deck.pop())
					
			if len(self.tableau3.show) < 1:
				if len(self.tableau3.hide) == 2:
					self.tableau3.show.append(self.deck.pop())
				else:
					self.tableau3.hide.append(self.deck.pop())
					
			if len(self.tableau4.show) < 1:
				if len(self.tableau4.hide) == 3:
					self.tableau4.show.append(self.deck.pop())
				else:
					self.tableau4.hide.append(self.deck.pop())
					
			if len(self.tableau5.show) < 1:
				if len(self.tableau5.hide) == 4:
					self.tableau5.show.append(self.deck.pop())
				else:
					self.tableau5.hide.append(self.deck.pop())
					
			if len(self.tableau6.show) < 1:
				if len(self.tableau6.hide) == 5:
					self.tableau6.show.append(self.deck.pop())
				else:
					self.tableau6.hide.append(self.deck.pop())	
					
			if len(self.tableau7.show) < 1:
				if len(self.tableau7.hide) == 6:
					self.tableau7.show.append(self.deck.pop())
				else:
					self.tableau7.hide.append(self.deck.pop())
			
	# stock主要动作
	# # 翻牌，到底时回头再来
	# # 从stock中移出。
	
	def deal_from_stock():  # 牌堆翻牌
		# !Waring 注意考虑stock为空时如何处理。
		# 从UI角度来说，show为空时，鼠标是点选不到的，也就不能触发这个功能
		self.stock.flipStack()
		self.showStock(self.stock.show)
		
	# foundation 主要动作
	# # 从foundation中取出牌
	# # 将牌放入foundation中
	
	def move_to_foundation(tuple, toFound): 
		cardFrom, card = tuple[0],tuple[1]
		if toFound.addable(card): #pile不addable
			toFound.add(card)
			if isinstance(cardFrom, tableau):
				cardFrom.flip()
		else:
			undo(cardFrom, card)
	# tableau 主要动作
	# # tableau之间移动牌
	# # 从其他地方得到牌
	# 其实这个不是很有必要吧，因为card与出处无关，所以只需考虑moveto就行了吧
	# def move_within_tableau(tuple, tabTo): 
		# cardFrom, card = tuple[0],tuple[1]
		# if tabTo.addable(card):
			# tabTo.add(card)
			# if isinstance(cardFrom, tableau):
				# cardFrom.flip()
		# else:
			# undo(cardFrom,card)
	
	def move_to_tableau(tuple, tabTo): # 跟前面其他一样，功能可能有重复
		cardFrom, card = tuple[0],tuple[1]
		if tabTo.addable(card):
			tabTo.add(card)
			if isinstance(cardFrom, tableau):
				cardFrom.flip()
		else:
			undo(cardFrom,card)
		
	def undo(cardFrom, card): # 牌面回到原来的地方
		cardFrom.add(card)
		unChaced()
		
class stock(object): # 新牌来源

	def __init__(self): 
		self.hide = []
		self.show = []
	
	def flipStack(self): # 翻stock，每三张放入stack中
		if len(self.hide) >= 3:
			self.show.append(self.hide.pop())
			self.show.append(self.hide.pop())
			self.show.append(self.hide.pop())
			
		elif len(self.hide) < 3 and len(self.hide) > 0: # 牌堆还剩不到三张 
			while len(self.hide) > 0:
				self.show.append(self.hide.pop())
		
		elif len(self.hide) == 0: # pile空之后，须将stack反序，然后进入下一轮循环
			if len(self.show) > 0:
				self.show.reverse()
				self.hide = self.show
				self.show = []
		return
		
	# 鼠标点选牌堆，就会触发getCard
	# 总是返回cardList，和tableau接口一致，保证鼠标get到的内容一致
	def getCard(self): 
		if len(self.show) == 0:
			return
		cards = []
		cards.append(self.show.pop())
		return self.show, cards
	
class foundation(object): #归档牌堆，将4种花色按顺序归档. 
	def __init__(self):
		self.found = []
		
	def add(self,card): # 
		if self.addable(card):
			self.found.extend(card)
		
	def addable(self, card):
		if len(card) > 1: # 只支持移动一张牌
			return False
		if len(self.found) == 0:
			if card.get_rank() == "A":
				return True
		elif len(self.found) > 0 and len(self.found) < 13:
			if 	sameSuit(self.found[-1],card):
				if isRank(self.found[-1],card):
					return True
		return False
	
	# 鼠标点选牌堆，就会触发getCard
	# 总是返回cardList，和tableau接口一致，保证鼠标get到的内容一致	
	def getCard(self): 
		if len(self.found) == 0:
			return
		cards =[]
		cards.append(self.found.pop())
		return self.found, cards
		
class tableau(object): # 主画面牌堆
# 重新构造tableau
	def __init__(self):
		self.show = []
		self.hide = []
	
	#判断一个tableau是否为空
	# def isEmpty(self): # 是否有必要留下这个接口，在UI中检查不触发翻牌动画：好像它可以自己解决吧，假如len为0的话
		# if len(self.show)== 0\
			# and len(self.hide)==0: # show 为空，hide也为空
			# return True
		
		# return False
	
	#翻面
	def flip(self):
		if len(self.show) == 0:
			if len(self.hide) != 0: #  若牌堆为空，不处理也OK的吧？
				self.show.append(self.hide.pop())
				# self.show.show() # 触发翻牌动画
				
	def getPile(self,card):  # 鼠标点选牌堆，就会触发getCard,跟其他对象不同，这里返回的是tableau对象，不是列表
		#!Attention 处理空队列(会有空队列么？空的话应该没有card这个对象了)	
		if len(self.show) == 0:
			return
		index = self.show.index(card)
		cards = self.show[index:]
		for card in self.show:
			self.show.remove(card)
		return self, cards
		
	
	def addable(self, tabList): # 接受list参数，支持多个移动
		if len(self.show) == 0: # 牌堆为空,需保证每次移牌成功之后都要flip牌堆，否则这里会有问题
			if tabList[0] == "K":
				return True
		else:
			if isRank(self.show[-1],tabList[0]) and \
				diffColor(self.show[-1], tabList[0])
				return True
		return False
		
	def add(self, tabList):
		self.show.extend(tabList)

def checkAlive(): # 收集游戏信息，判断是否还可以移动。这个应该涉及优化算法，否则会很慢
	
# 辅助型功能函数
	# aLive.append(tableau1.show())
	# aLive.append(tableau2.show())
	# aLive.append(tableau3.show())
	# aLive.append(tableau4.show())
	# aLive.append(tableau5.show())
	# aLive.append(tableau6.show())
	# aLive.append(tableau7.show())
	# aLive .append(found)
	pass
	
def isRank(card1, card2): #rank是否连续, card1=2， card2 = A 
	if RANKS.index(card1.get_rank()) - \ 
		RANKS.index(card2.get_rank()) == 1: #还是应该有顺序，否则4放3下面了
		return True
	else:
		return False
	
def  sameSuit(card1, card2): # 花色一致检验
	if card1.get_suit()== card2.get_suit():
		return True
	else:
		return False

def diffColor(card1, card2) # 花颜色不一致
	suit1 = card1.get_suit()
	suit2 = card2.get_suit()
	# 花色相间，不同颜色间距为奇数
	if abs(SUITS.index(suit1) - SUITS.index(suit2)) %2 != 0:
		return True
		
	return False
	
def isAccessable(place, card): # 留给鼠标挪牌时的接口，如果不可访问，点选不到
	if isinstance(place, stock):
		if card == place.show[-1]:
			return True
	elif isinstance(place,foundation):
		if card == place[-1]:
			return True
	elif isinstance(place,tableau):
		if card in place:
			return True
	return False

def isCached(self): # Cached中有没有东西
	return len(self.cached) == 0
	
def unCached(self): #  清空Cached,undo的时候会默认清空
	self.cached = []
	
def addCached(self): # 增加一个cache的方法，暂时还不知道放在哪里好
	pass