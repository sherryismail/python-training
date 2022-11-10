from scribes.terminalScribe import TerminalScribe

class PlotScribe(TerminalScribe):

    def __init__(self, domain, **kwargs):
        self.x = domain[0]
        self.domain = domain
        super().__init__(**kwargs)

    def toDict(self):
        data = super().toDict()
        data['x'] = self.x 
        data['domain'] = self.domain
        return data

    def fromDict(data, g):
        scribe = g[data.get('classname')](
            color=data.get('color'),
            mark=data.get('mark'),
            trail=data.get('trail'),
            trailColor=data.get('trailColor'),
            pos=data.get('pos'),
            domain=data.get('domain'),
        )
        scribe.moves = scribe._movesFromDict(data.get('moves'))
        scribe.x = data.get('x')
        return scribe

    def _plotX(self, pos, canvas):
        if canvas.hitsWall(pos): 
            try:
                super().bounce(pos, canvas)
                if int(pos[0]/canvas._x) % 2 == 0: #if y=0, bounce forwards
                    horizontal = pos[0] % canvas._x
                    self.x = horizontal # back to normal
                else: #or if y=MAX wall, bounce backwards
                    horizontal = int(canvas._x - (pos[0] %canvas._x) -1)
                new_pos = [horizontal, pos[1]]
                self.draw(new_pos, canvas)
            except Exception as e:
                print(e)
        else:
            self.draw(pos, canvas)
        # self.x = self.x + 1 #remove this because x is incremented from plotX()

    def plotX(self, function):
        self.x = self.domain[0]
        for x in range(self.domain[0], self.domain[1]):
            pos = [x, function(x)]
            self.moves.append((self._plotX, [pos]))# not (self._plotX, [function(x)]))
        #TypeError: Object of type function is not JSON serializable if [function] or function[(x)]