import random
class elosystem():
    def __init__(self):
        self.startelo = 1200
        self.Nscale = 0.5 # does it need chaning?
        self.scorescale = 1
        self.players = []

    def Ngames(self, player): # function of N games per player
        factor = 20
        if player[1]< 30*self.Nscale and player[1]<2300*self.scorescale: # N must be scaled. prob of
            factor = 40
        elif player[0]<2400*self.scorescale:
            factor = 20
        elif player[0]>2400*self.scorescale and player[1]>30*self.Nscale:
            factor = 10
        return factor

    def rating(self, a, b, choice): # player = [rating, Ngames], choice=[a,b] 0-1
        rb = b[0]
        ra = a[0]

        calc = 1/(1+10**((rb-ra)/400))
        if ra == 0:
            ra = self.startelo
        if rb == 0:
            rb = self.startelo

        ra += self.Ngames(a)*(choice[0]-calc)
        rb += self.Ngames(b)*(choice[1]+calc-1)
        a[1] += 1
        b[1] += 1

        a[0] = ra
        b[0] = rb
        return [a,b]
z = elosystem()
#a = ["app utvikling", "intrastructure as code", "application security", "game development", "computer vision"]
#a += ["software design", "AI", "Matte3"]
#a = ["app utvikling", "application security", "AI", "sivilingeniør"]
players = {}
for p in a:
    players[p] = [1200, 0]
for iter in range(round(len(a)**2/2)):
    playing = [a[i] for i in random.sample(range(0,len(a)), 2)]
    print(playing, iter)
    first = int(input("first playerscore: "))
    second = 1-first

    p1 = players[playing[0]]
    p2 = players[playing[1]]
    players[playing[0]], players[playing[1]]  = z.rating(p1, p2, [first, second])
    print(players[playing[0]], players[playing[1]])

    if iter%5 == 0:
        print(players)
print(players)
