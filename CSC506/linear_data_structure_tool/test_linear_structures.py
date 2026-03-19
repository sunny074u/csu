
from stack_ds import Stack, is_balanced
from queue_ds import Queue, bfs_order
from deque_ds import Deque, is_palindrome
from linked_list_ds import LinkedList, move_to_front_search


def demo_stack() -> None:
    print("\n=== STACK DEMO (LIFO) ===")
    s = Stack[int]()
    for x in [10, 20, 30]:
        s.push(x)
        print("push:", x, "->", s)

    print("peek:", s.peek())
    print("pop :", s.pop(), "->", s)
    print("balanced check:", "([{}])", "=>", is_balanced("([{}])"))
    print("balanced check:", "([)]", "=>", is_balanced("([)]"))


def demo_queue() -> None:
    print("\n=== QUEUE DEMO (FIFO) ===")
    q = Queue[str]()
    for name in ["ticket#1", "ticket#2", "ticket#3"]:
        q.enqueue(name)
        print("enqueue:", name, "->", q)

    print("front:", q.front())
    print("dequeue:", q.dequeue(), "->", q)

    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F"],
        "D": [],
        "E": ["F"],
        "F": [],
    }
    print("BFS order from A:", bfs_order(graph, "A"))


def demo_deque() -> None:
    print("\n=== DEQUE DEMO (BOTH ENDS) ===")
    d = Deque[int]()
    d.add_rear(2)
    d.add_rear(3)
    d.add_front(1)
    print("after add_front/add_rear:", d)

    print("remove_front:", d.remove_front(), "->", d)
    print("remove_rear :", d.remove_rear(), "->", d)

    print("palindrome:", "Never odd or even", "=>", is_palindrome("Never odd or even"))
    print("palindrome:", "Data structures", "=>", is_palindrome("Data structures"))


def demo_linked_list() -> None:
    print("\n=== LINKED LIST DEMO ===")
    ll = LinkedList[str]()
    for song in ["Intro", "Track1", "Track2", "Track3"]:
        ll.insert(song)
    print("playlist:", ll.display())

    print("search Track2:", ll.search("Track2"))
    print("delete Track1:", ll.delete("Track1"))
    print("after delete:", ll.display())

    # move-to-front heuristic demo
    print("move-to-front search Track3:", move_to_front_search(ll, "Track3"))
    print("after move-to-front:", ll.display())


def main() -> None:
    demo_stack()
    demo_queue()
    demo_deque()
    demo_linked_list()
    print("\nAll demos completed.")


if __name__ == "__main__":
    main()