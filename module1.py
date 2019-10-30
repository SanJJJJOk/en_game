import enum

class ModeType(enum.Enum):
    Disabled = 0
    Special = 1
    Olymp = 2
    Gibrid = 3
    Meta = 4
    Logo = 5

    def next(self):
        val = self.value + 1
        if (val == 6):
            val = 0
        return ModeType(val)

    def prev(self):
        val = self.value - 1
        if (val == -1):
            val = 5
        return ModeType(val)

    @staticmethod
    def get_well_known_mode_types():
        return {
            ModeType.Special: ['special', 'специальный'],
            ModeType.Olymp: ['olymp', 'олимпийка'],
            ModeType.Gibrid: ['gibrid', 'гибриды'],
            ModeType.Meta: ['meta', 'метаграммы'],
            ModeType.Logo: ['logo', 'логогрифы']
            }

class SettingsHolder:
    def __init__(self):
        self.settings_by_id = {}

    def add(self, id):
        self.settings_by_id[id] = Settings()

    def get(self, id):
        return self.settings_by_id[id]

class Settings:
    def __init__(self):
        self.current_mode = ModeType.Disabled

    def next_mode(self):
        self.current_mode = self.current_mode.next()
        return self.current_mode

#class TestGame:
#    def __init__(self):
#        self.words = []
#        self.found = []

#class Holder(object):
#	def __init__(self):
#		self.players = {}
#		self.games_count = 3   
#		self.games_score = [7,1,1]

#	def set_nickname(self, id, nick):
#		self.players[id].nickname = nick

#	def show_stat(self):
#		result = []
#		for key in self.players:
#		    player = self.players[key]
#		    player_res = player.nickname + ':'
#		    for i in range(self.games_count):
#		        player_res=player_res+'\ngame #' + str(i+1) + ': '
#		        if player.gamestats[i] is None:
#		            player_res=player_res+'-%'
#		        else:
#		            player_res=player_res+'{0:.2f}%'.format(100.0*player.gamestats[i]/self.games_score[i])
#		    result.append(player_res)
#		return result

#	def play(self, id, gamenum):
#		if gamenum>self.games_count or gamenum<1:
#		    return 'game does not exist'
#		if self.players[id].gamestats[gamenum - 1] is None:
#		    return 'you are not authorized to this game'
#		self.players[id].currgame = gamenum
#		return 'game # ' + str(gamenum)
		    
#	def game(self, id, message):
#		if self.players[id].currgame == 1:
#		    return self.__game1(id, message)
#		return ['choose game with ''/play N'' command, where N - game number']
		    
#	def gamehelp(self, id):
#		if self.players[id].currgame == 1:
#		    return [
#                'available commands:',
#                ' ''0'' - reset state',
#                ' ''NN''(N - number from 1 to 7) - make a move. after this you receive two messages: first - state after your move, second - state after the rabbit actions']
#		return ['choose game with ''/play <N>'' command']
		
#	def __game1(self, id, message):
#		vals = self.players[id].game1
#		if message=="show":
#		    return [self.__game1_show(id)]
#		if not len(message)==2:
#		    if message=="0":
#		        for i in range(7):
#		            vals[i] = True
#		        return ['reseted']
#		    return ['not valid input']
#		try:
#		    i1 = int(message[0])
#		    i2 = int(message[1])
#		    if i1>7 or i1<1 or i2>7 or i2<1 or i1==i2:
#		        return ['not valid input']
#		    vals[i1-1]=False
#		    vals[i2-1]=False
#		    first_result = self.__game1_show(id)
#		    tmp = [False, False, False, False, False, False, False]
#		    for i in range(7):
#		        if vals[i]:
#		            if i == 0:
#		                tmp[1]=True
#		                tmp[6]=True
#		                continue
#		            if i == 6:
#		                tmp[0]=True
#		                tmp[5]=True
#		                continue
#		            tmp[i-1]=True
#		            tmp[i+1]=True
#		    self.players[id].game1 = tmp
#		    empty_count = 0#self.players[id].gamestats[0]
#		    for i in range(7):
#		        if not tmp[i]:
#		            empty_count = empty_count + 1
#		    if empty_count > self.players[id].gamestats[0]:
#		        self.players[id].gamestats[0] = empty_count
#		    return [first_result, self.__game1_show(id)]
#		except:
#		    return ['not valid input']

#	def __game1_show(self, id):
#		strr = ''
#		for i in range(7):
#		    if self.players[id].game1[i]:
#		        strr=strr+str(i+1)
#		    else:
#		        strr=strr+'x'
#		return strr
		
#class Player(object):
#	def __init__(self, id):
#		self.id = id
#		self.nickname = id
#		self.gamestats = [0, None, None]
#		self.currgame = 0
#		self.game1 = [True, True, True, True, True, True, True]
