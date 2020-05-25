import ListOfInteger from "../types/ListOfInteger";
import Float from "../types/Float";

class Dummy {
  static numArgs = 1
  static inputType = ListOfInteger
  static outputType = Float

  static description(): string {
    return "Dummy"
  }

  static function(items: number[]): number {
    var sum = 0
    for (var i = 0; i < items.length; i++) {
        sum += items[i]
    }
    return Math.abs(sum)
  }

  static inputGenerators(): Function[] {
    return [() => { return [8, 3, 11] }, () => { return [-4, 1] }, () => { return [-10, -2, 0, 0] }]
  }

  static answerText(): string {
    return "This function returns the median of the input list of numbers. If the size of the list is odd, it is the middle element of the list when sorted; if the size is even, it is the average of the middle two elements of the list when sorted."
  }

  static inputPlaceHolderText(): string {
    return this.inputType.placeholderText()
  }

  static outputPlaceHolderText(): string {
    return this.outputType.placeholderText()
  }

  static inputDescription(): string {
    return this.inputType.longDescription()
  }

  static outputDescription(): string {
    return this.outputType.longDescription()
  }

  static validInput(input: any): boolean {
    var as_list;
    try {
      // Parse string as a list, with brackets required
      if (input.trim()[0] !== "[") {
        // console.log("no starting bracket")
        return false;
      }
      as_list = JSON.parse(input);
      if (as_list.length > 0) {
        return this.inputType.valid(input)
      } else {
        return false
      }
    } catch (e) {
      console.log("error: ", e)
      return false;
    }
  }

  static validOutput(input: any): boolean {
    return this.outputType.valid(input)
  }

  static parseInput(input: any): any[] {
    return this.inputType.parse(input)
  }

  static parseOutput(output: any): number {
    return this.outputType.parse(output);
  }

  static equivalentInputs(first: any, second: any): boolean {
    return this.inputType.areEquivalent(first, second)
  }

  static equivalentOutputs(first: any, second: any): boolean {
    return this.outputType.areEquivalent(first, second)
  }

  static inputDisplayStr(input: number[]): string {
    return this.inputType.displayString(input)
  }

  static outputDisplayStr(output: number): string {
    return this.outputType.displayString(output)
  }

  static inputDBStr(input: number[]): string {
    return this.inputType.dbString(input)
  }

  static outputDBStr(output: number): string {
    return this.outputType.dbString(output)
  }
}

export default Dummy