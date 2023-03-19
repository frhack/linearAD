class Tape:
    def __init__(this, direction):
        this.direction = direction 
        this.list = [] 

    def clear(this): this.list.clear()

    def append(this,a): this.list.append(a) if(this.direction) else this.list.insert(0, a )
