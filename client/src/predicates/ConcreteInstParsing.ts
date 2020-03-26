class ConcreteInstParsing {
    // Checks if inst declaration is correct, though doesn't check
    // for validity of the items within each set, just set names


    static setDefs(instance: string): Map<string, Array<string>> {
        var defs = new Map<string, Array<string>>()
        var spaceTokens = instance.trim().split(/\s+/)
        if (spaceTokens.length < 4) {
          alert("Malformed concrete instance")
          // console.log("less than 4 space tokens")
          return defs
        }
        if (spaceTokens[0] !== "inst") {
          alert("Malformed concrete instance")
          // console.log("inst keyword missing")
          return defs
        }
        if (spaceTokens[2] !== "{") {
          alert("Malformed concrete instance")
          console.log("no start bracket")
          return defs
        }
        if (spaceTokens[spaceTokens.length - 1] !== "}") {
          alert("Malformed concrete instance")
          // console.log("no end bracket")
          return defs
        }
  
        // Get each line within brackets
        var onBracks = instance.split(/{|}/)
        var lines = onBracks[1].split(/\n|and/)
        var successFul = true
        var setName = ""
        for (var i = 0; i < lines.length; i++) {
          var line = lines[i].trim()
          if (line === "") {
            continue
          }
  
          var items = Array<String>()
          if (line.split(/\s+/)[0] !== "+") {
            // New set name
            var onEqual = lines[i].split("=")
            if (onEqual.length !== 2) {
              alert("Malformed concrete instance - need exactly 1 equals sign")
              return new Map<string, Array<string>>()
            }

            setName = onEqual[0].trim()
            if (!setName.match(/^[A-Za-z0-9]+$/)) {
              alert("Malformed concrete instance - set name should be alphanumeric")
              return new Map<string, Array<string>>()
            }
            // Setname already exists
            if (defs.has(setName)) {
              alert("Malformed concrete instance - repeated set name")
              return new Map<string, Array<string>>()
            }
            items = onEqual[1].split("\+")
          } else {
            // Continued set definition from line before
            // Since + is at beginning of line, omit first item after split
            items = line.split("\+").slice(1)
          }

          for (var j = 0; j < items.length; j++) {
            var item = items[j].trim()
            if (item === "") {
              alert("Malformed concrete instance")
              return new Map<string, Array<string>>()
            }
  
            if (defs.has(setName)) {
              // Check if item already exists
              if (defs.get(setName)?.includes(item)) {
                alert("Malformed concrete instance - repeated item name")
                return new Map<string, Array<string>>()
              }
            } else {
              defs.set(setName, [])
            }

            var newSet = defs.get(setName)
            if (newSet !== undefined) {
              newSet.push(item)
              defs.set(setName, newSet)
            }
          }
        }  
        return defs
    }
}

export default ConcreteInstParsing