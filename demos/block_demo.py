from projcoin import Block

def main():
    block = Block()
    block.time = "2021-01-04 09:38:22.163432" #hard coding the timestamp to make the demo determenistic

    print(block)

if __name__ == "__main__":
    main()