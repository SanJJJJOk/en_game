
class Holder(object):
	def __init__(self):
		self.players = {}
		self.games_count = 3        

	def set_nickname(self, id, nick):
		self.players[id].nickname = nick

	def show_stat(self):
		result = []
		for key, player in self.players:
		    player_res = ''
		    for i in range(self.games_count):
		        if player.gamestats[i] is None:
		            player_res=player_res+'x'
		        else:
		            if player.gamestats[i]:
		                player_res=player_res+'+'
		            else:
		                player_res=player_res+'-'
		    result.append(player.nickname + ': ' + player_res)
		return result

	def play(self, id, gamenum):
		if gamenum>self.games_count or gamenum<1:
		    return 'game does not exist'
		if self.players[id].gamestats[gamenum - 1] is None:
		    return 'you are not authorized to this game'
		self.players[id].currgame = gamenum
		return 'game # ' + gamenum
		    
	def game(self, id, message):
		if self.players[id].currgame == 1:
		    return self.__game1(id, message)
		return ['choose game with ''/play N'' command']
		    
	def gamehelp(self, id):
		if self.players[id].currgame == 1:
		    return [
                'available commands:',
                ' ''0'' - reset state',
                ' ''NN''(N - number from 1 to 7) - make a move. after this you receive two messages: first - state after your move, second - state after the rabbit actions']
		return ['choose game with ''/play <N>'' command']
		
	def __game1(self, id, message):
		vals = self.players[id].game1
		if text=="show":
		    return [self.__game1_show(id)]
		if not len(text)==2:
		    if text=="0":
		        for i in range(7):
		            vals[i] = True
		        return ['reseted']
		    return ['not valid input']
		try:
		    i1 = int(text[0])
		    i2 = int(text[1])
		    if i1>7 or i1<1 or i2>7 or i2<1 or i1==i2:
		        return ['not valid input']
		    vals[i1-1]=False
		    vals[i2-1]=False
		    first_result = self.__game1_show(id)
		    tmp = [False, False, False, False, False, False, False]
		    for i in range(7):
		        if vals[i]:
		            if i == 0:
		                tmp[1]=True
		                tmp[6]=True
		                continue
		            if i == 6:
		                tmp[0]=True
		                tmp[5]=True
		                continue
		    self.players[id].game1 = tmp
		    return [first_result, self.__game1_show(id)]
		except:
		    return ['not valid input']

	def __game1_show(id):
		strr = ''
		for i in range(7):
		    if self.players[id].game1[i]:
		        strr=strr+str(i+1)
		    else:
		        strr=strr+'x'
		return strr
		
class Player(object):
	def __init__(self, id):
		self.id = id
		self.nickname = id
		self.gamestats = [False, None, None]
		self.currgame = 0
		self.game1 = [False, False, False, False, False, False, False]
