class Tape:
    def __init__(this, direction):
        this.direction = direction 
        this.list = [] 


    def clear(this):
        this.list.clear()

    def append(this,a):
        if(this.direction):
            this.list.append(a)
        else:
            this.list.insert(0, a )


    def get_transpose(this):
        obj =  Tape(this.list)
        obj.old = this
        obj.list = this.list
        obj.direction = not this.direction
        obj.list.reverse()
        return obj



#t = Tape([1])
#t.append(2)
#t.append(3)
#print(t.list)
#t = Tape([])
#t = t.get_transpose()
#t.append(1)
#t.append(2)
#t.append(3)
#print(t.list)
#t = Tape([])
#t = t.get_transpose()
#t = t.get_transpose()
#t.append(1)
#t.append(2)
#t.append(3)
#print(t.list)
