class Node {
    name = ""
    to = new Array<Node>()
    from = new Array<Node>()

    constructor(name: string) {
        this.name = name
    }

    printout(): string {
        var print = this.name + "\n"
        print += "  to:\n" 
        for (var i = 0; i < this.to.length; i++) {
            print += "  " + this.to[i].name + "\n"
        }
        print += "  from:\n" 
        for (var i = 0; i < this.from.length; i++) {
            print += "  " + this.from[i].name + "\n"
        }
        return print
    }

    addDest(n: Node) {
        this.to.push(n)
    }

    addSrc(n: Node) {
        this.from.push(n)
    }

    dests(): Node[] {
        return this.to
    }

    srcs(): Node[] {
        return this.from
    }

    cycle() {
        console.log("doing cycle")
        console.log(this.printout())
        var seen = new Array<Node>()
        for (var i = 0; i < this.to.length; i++) {
            var toNode = this.to[i]
            if (toNode.cycleHelper(seen) === true) {
                console.log(toNode.name, "cycle found")
                return true
            }
        }
        return false
    }

    // Returns the empty set if cycle detected, otherwise
    // returns all nodes reachable from this one by DFS
    // including itself
    // Needs to pass in a list of seen nodes, check against that instead
    cycleHelper(seen: Array<Node>): boolean {
        console.log("doing cycle helper")
        console.log(this.printout())
        var newSeen = Array<Node>()
        for (var i = 0; i < seen.length; i++) {
            if (seen[i].name === this.name) {
                return true
            }
            newSeen.push(seen[i])
        }
        newSeen.push(this)

        for (var i = 0; i < this.to.length; i++) {
            var toNode = this.to[i]
            if (toNode.cycleHelper(newSeen) === true) {
                console.log(toNode.name, "cycle found")
                return true
            }
        }
        return false
    }

    // For these 2, do the same list thing, and check length of cycle

    // Find a 3 cycle
    threeCycle() {
        var seen = new Array<Node>()
        for (var i = 0; i < this.to.length; i++) {
            var toNode = this.to[i]
            if (toNode.threeCycleHelper(seen) === true) {
                return true
            }
        }
        return false
    }

    // 0 1 2 3 4
    // any of these could be the repeat
    // 0 -> length is 5
    // 4 -> length is 1
    // so...length of array - index
    threeCycleHelper(seen: Array<Node>): boolean {
        var newSeen = Array<Node>()
        for (var i = 0; i < seen.length; i++) {
            if (seen[i].name === this.name) {
                if (seen.length - i === 3) {
                    return true
                }
                // Saw a cycle but wasn't a 3 cycle
                return false
            }
            newSeen.push(seen[i])
        }
        newSeen.push(this)
        for (var i = 0; i < this.to.length; i++) {
            var toNode = this.to[i]
            if (toNode.threeCycleHelper(newSeen) === true) {
                return true
            }
        }
        return false
    }

    // is bipartite graph - can't have odd sized cycle
    oddCycle() {
        var seen = new Array<Node>()
        for (var i = 0; i < this.to.length; i++) {
            var toNode = this.to[i]
            if (toNode.oddCycleHelper(seen) === true) {
                return true
            }
        }
        return false
    }

    oddCycleHelper(seen: Array<Node>): boolean {
        var newSeen = Array<Node>()
        for (var i = 0; i < seen.length; i++) {
            if (seen[i].name === this.name) {
                if (seen.length - i % 2 === 1) {
                    return true
                }
                // Saw a cycle that was even
                return false
            }
            newSeen.push(seen[i])
        }
        newSeen.push(this)
        for (var i = 0; i < this.to.length; i++) {
            var toNode = this.to[i]
            if (toNode.oddCycleHelper(newSeen) === true) {
                return true
            }
        }
        return false
    }
}
export default Node