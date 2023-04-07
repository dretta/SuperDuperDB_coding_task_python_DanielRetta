# I know there aren't any package imports allowed, 
# but how else am I suppose to process command line input? ¯\_(ツ)_/¯
import sys
# In theory this isn't needed, but in practice not using this would  be a challenge of its own!
import json

# Enable for debugging.
PRINT_STATEMENTS = False


# dictionary: dict object to be subsituted.
# depth: integer counting how much more recursion depth can take place.
# if zero, a dict value will not be subsituted and will remain as is.
# by default, depth is at -1, allowing for unlimited depth,
# any negative amount will allow unlimited depth.
def func(dictionary:dict, depth:int=-1) -> dict:
    for key, value in dictionary.items():
        if isinstance(value, dict):
            if depth:
                myPrint(f"Recursive dictionary subsituion on key '{key}' with '{depth-1 if depth >= 0 else 'unlimited'}' depth remaining.")
                dictionary[key] = func(value, depth-int(depth > 0))
            else:
                myPrint("Depth has reached 0, do not recursively call func.")
        else:
            myPrint(f"Subsituting value '{value}' in key '{key}'.")
            dictionary[key] = {'_content': value, '_type': str(type(value))}
    return dictionary


def myPrint(printStr:str) -> None:
    if PRINT_STATEMENTS:
        print(printStr)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Make subsituions on the input json file and write them to the output file.')
    # parser.add_argument('inputFile', type=argparse.FileType(mode='r'), help='Path to the input file that contains the json object.')
    # parser.add_argument('depth', default=-1, type=int, required=False, help='The maximum recusion depth allowed.')
    # parser.add_argument('outputFile', type=argparse.FileType(mode='w'), help='Path to the output file to write the results of the subsituions.')
    # args = parser.parse_args()
    
    argCount = len(sys.argv)
    depth = -1
    
    if argCount == 3:
        _, inputFile, outputFile = sys.argv
    elif argCount == 4:
        _, inputFile, depth, outputFile = sys.argv
        try:
            depth = int(depth)
        except:
            print(f"Input for depth is '{depth}', not an integer. Exiting.")
            sys.exit(1)
    else:
        print(f" {argCount} inputs found, expecting only 3 or 4 inputs, exiting.")
        sys.exit(1)
    
    try:
        with open(inputFile, mode='r') as inputObj:
            inputDict = json.load(inputObj)
    except OSError:
        print(f"Cannot open input file {inputFile}, exiting.")
        sys.exit(1)
    except json.decoder.JSONDecodeError:
        print(f"Cannot make input file {inputFile} into python dict, exiting.")
        sys.exit(1)
    
    outputDict = func(inputDict, depth)
    
    try:
        with open(outputFile, mode='w') as outputObj:
            json.dump(outputDict, outputObj, indent=4)
    except OSError:
        print(f"Cannot open output file {outputFile}, exiting.")
        sys.exit(1)