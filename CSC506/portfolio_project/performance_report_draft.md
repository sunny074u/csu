# Portfolio System for Sets, Sorting Algorithms, and Core Data Structures

## Introduction
This project was designed to bring together the main topics covered in the course into one working system instead of leaving them as separate exercises. The goal was not just to make each algorithm run, but to show how the concepts connect. That includes sorting, set operations, and several core data structures such as stacks, queues, trees, graphs, and hash tables.

I approached the project as a portfolio system rather than a collection of isolated scripts. That mattered because in real programming work, developers rarely use one data structure or one algorithm by itself. Most problems require a combination of structures and operations. A good solution depends on picking the right tool for the right task.

The final system includes a bubble sort implementation with step-by-step output, a quickselect implementation for finding the kth smallest value, a custom Set class, several core data structures, a menu-driven interface, and simple performance analysis tools. Together, these parts show both correctness and trade-offs. That trade-off discussion is important because efficiency is not just about speed. It is also about memory use, simplicity, maintainability, and whether a solution fits the actual problem being solved.

## Project Objectives
The first objective was to implement bubble sort and make the process visible. Bubble sort is not the most efficient sorting algorithm, but it is easy to follow and useful for understanding how repeated comparison and swapping gradually move values into order. Showing each pass helps make the logic clear.

The second objective was to implement quickselect. This algorithm solves a different problem. Instead of sorting the entire list, quickselect focuses on finding the kth smallest element. That makes it a good example of solving a problem more directly instead of doing extra work.

The third objective was to build a Set class from scratch. The class supports union, intersection, difference, and symmetric difference. This part of the project matters because sets model a very common type of problem: comparing groups, removing duplicates, and identifying overlap or exclusion.

The fourth objective was integration. The project includes a stack, queue, binary search tree, graph, and hash table. These structures were added because they represent different ways of organizing and accessing data. A stack is useful for last-in-first-out behavior, a queue fits first-in-first-out behavior, a tree supports hierarchical storage and searching, a graph models relationships, and a hash table gives fast average lookup.

The last objective was evaluation. I added a basic performance analysis section so the project does more than just work. It also gives some evidence about when one method is more practical than another.

## Bubble Sort Analysis
Bubble sort repeatedly compares adjacent elements and swaps them when they are out of order. After each full pass, the largest unsorted value moves toward its correct position at the end of the list. The process continues until the list is sorted.

The main strength of bubble sort is that it is easy to understand and easy to trace. That is why it works well in a teaching context. The visualization feature in this project makes that even more useful because it shows every comparison and swap. A student can see the movement of values across the list instead of treating the algorithm as a black box.

The weakness of bubble sort is efficiency. Its time complexity is generally O(n^2), which means performance drops quickly as the input grows. For very small lists, that may not matter. For larger lists, it becomes a poor choice compared with more advanced algorithms. This matches the standard analysis of comparison-based sorts found in data structures literature (Cormen et al., 2022).

## Quickselect Analysis
Quickselect is used to find the kth smallest element in a list. It is related to quicksort because it also uses partitioning around a pivot. The difference is that quickselect does not continue processing both sides of the partition. It only continues on the side that contains the target element.

That design makes it efficient for selection problems. On average, quickselect runs in O(n) time, although its worst case is O(n^2) if bad pivots are repeatedly chosen (Cormen et al., 2022). In practice, it is often much faster than sorting the whole list when the real goal is simply to find one ranked value such as the median or the 5th smallest number.

## Set Class and Set Operations
The custom Set class in this project supports four core operations: union, intersection, difference, and symmetric difference. These operations are central to set theory and also appear often in software problems involving comparison, filtering, and membership testing.

Union combines all unique elements from two sets. Intersection returns only the elements both sets share. Difference returns elements found in one set but not the other. Symmetric difference returns elements that are in either set but not in both. These operations are mathematically simple, but they are powerful in practice.

This also connects to the idea of static versus dynamic set operations. Static operations make sense when the collection does not change often and the main goal is comparison. Dynamic operations matter more when elements are being inserted or removed regularly. In a static case, it may be enough to compute union or intersection once. In a dynamic case, the data structure must support efficient updates over time.

## Integration of Data Structures
The integrated portfolio system also includes a stack, queue, binary search tree, graph, and hash table. Each one serves a different purpose.

The stack demonstrates last-in-first-out behavior. The queue demonstrates first-in-first-out behavior. The binary search tree provides ordered storage and searching. The graph shows how relationships can be modeled beyond simple linear or hierarchical structures. The hash table provides fast average lookup by mapping keys to positions using a hash function (Goodrich et al., 2015).

## Performance Analysis
The performance section compares bubble sort with Python's built-in sorting and compares quickselect with sorting followed by selecting the kth value.

This comparison matters because theory and practice should support each other. The theoretical expectation is that bubble sort will scale poorly compared with optimized sorting algorithms. The tests confirm that. As the input size increases, bubble sort becomes much slower.

Quickselect also performs well when the goal is to find one ranked element instead of fully sorting the list. Sorting the whole list just to find one value is unnecessary work. That is where quickselect shows its strength.

## Design Decisions
One major design decision was to keep the project in a menu-driven form. I chose that because it makes the project easy to demonstrate. A grader can run the program, choose an option, and immediately see the algorithm or data structure in action.

Another design choice was to use only standard Python libraries. That makes the project easier to run in different environments and avoids dependency problems. It also keeps the focus on the data structures and algorithms themselves.

## Conclusion
This portfolio project demonstrates mastery of the course concepts by combining sorting, selection, set operations, and multiple core data structures into one usable system. Bubble sort shows the mechanics of sorting step by step. Quickselect shows a more targeted and efficient way to solve selection problems. The Set class demonstrates core mathematical operations on collections. The stack, queue, tree, graph, and hash table broaden the system and show how different structures support different types of computation.

## References
Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.

Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2015). *Data structures and algorithms in Python*. Wiley.

Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
