def fifo(pages, capacity):
    page_faults = 0
    memory = []
    for page in pages:
        if page not in memory:
            if len(memory) < capacity:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            page_faults += 1
        print("Memory: ", memory)
    print("Total Page Faults:", page_faults)


def main():
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    capacity = 3
    print("Page reference sequence:", pages)
    print("Capacity of memory:", capacity)
    fifo(pages, capacity)


if __name__ == "__main__":
    main()
