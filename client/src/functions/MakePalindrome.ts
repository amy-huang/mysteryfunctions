import ListOfInteger from "./ListOfInteger";
import Integer from "./Integer";

class MakePalindrome {
  static description(): string {
    return "MakePalindrome"
  }

  static function(items: any[]): any[] {
    var newItems = Array.from(items)
    if (newItems.length < 2) {
      return newItems
    }
    var i = 0
    var j = newItems.length - 1
    while (i < j) {
      newItems[j] = newItems[i]
      i += 1
      j -= 1
    }
    return newItems
  }

  static inputGenerators(): Function[] {
    return [() => { return [333] }, () => { return [0, 0] }, () => { return [9, 9, 8] }, () => { return [-3, 0, 0, -3] }, () => { return [5, 3, 1, -1, 4] }, () => { return [-8, 3] }]
  }

  static answerText(): string {
    return "This function transforms any list of items into a palindromic one by changing the second half of it to mirror the first. The output list is the same whether or not you reverse it.";
  }

  static inputPlaceHolderText(): string {
    return ListOfInteger.placeholderText()
  }

  static inputDescription(): string {
    return ListOfInteger.longDescription()
  }

  static outputDescription(): string {
    return ListOfInteger.longDescription()
  }

  static validInput(input: any): boolean {
    return ListOfInteger.valid(input)
  }

  static validOutput(input: any): boolean {
    return ListOfInteger.valid(input)
  }

  static parseInput(input: any): any[] {
    return ListOfInteger.parse(input)
  }

  static parseOutput(output: any): any[] {
    return ListOfInteger.parse(output);
  }

  static equivalentOutputs(first: any[], second: any[]): boolean {
    return ListOfInteger.areEquivalent(first, second)
  }

  static inputStr(input: number[]): string {
    return ListOfInteger.asString(input)
  }

  static outputStr(output: number[]): string {
    return ListOfInteger.asString(output)
  }
}

export default MakePalindrome