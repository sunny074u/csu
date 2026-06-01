# First-Fit Memory Allocation Simulation

def first_fit(memory_blocks, process_sizes):
    allocation = [-1] * len(process_sizes)
    remaining_blocks = memory_blocks.copy()

    for i in range(len(process_sizes)):
        for j in range(len(remaining_blocks)):
            if remaining_blocks[j] >= process_sizes[i]:
                allocation[i] = j
                remaining_blocks[j] -= process_sizes[i]
                break

    return allocation, remaining_blocks


def print_results(memory_blocks, process_sizes, allocation, remaining_blocks):
    print("Initial Memory Blocks:", memory_blocks)
    print("Process Sizes:", process_sizes)
    print("\nProcess No.\tProcess Size\tBlock Allocated")

    for i in range(len(process_sizes)):
        if allocation[i] != -1:
            print(f"{i + 1}\t\t{process_sizes[i]}\t\tBlock {allocation[i] + 1}")
        else:
            print(f"{i + 1}\t\t{process_sizes[i]}\t\tNot Allocated")

    print("\nRemaining Memory Blocks:", remaining_blocks)


# Test Case 1
memory_blocks_1 = [100, 500, 200, 300, 600]
process_sizes_1 = [212, 417, 112, 426]

allocation_1, remaining_1 = first_fit(memory_blocks_1, process_sizes_1)

print("TEST CASE 1")
print_results(memory_blocks_1, process_sizes_1, allocation_1, remaining_1)


# Test Case 2
memory_blocks_2 = [120, 250, 350, 400, 600]
process_sizes_2 = [115, 300, 210, 500]

allocation_2, remaining_2 = first_fit(memory_blocks_2, process_sizes_2)

print("\n\nTEST CASE 2")
print_results(memory_blocks_2, process_sizes_2, allocation_2, remaining_2)