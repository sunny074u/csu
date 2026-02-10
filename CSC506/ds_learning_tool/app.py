from __future__ import annotations
import random
import streamlit as st

from structures import Stack, Queue, SinglyLinkedList
from complexity import COMPLEXITIES, predict


st.set_page_config(page_title="Data Structure Learning Tool", layout="wide")

st.title("Data Structure Learning Tool")
st.write("Hands-on: operate on a Stack, Queue, and Linked List. See behavior, use-cases, and predicted complexity.")

left, right = st.columns([1, 1])

if "stack" not in st.session_state:
    st.session_state.stack = Stack()
if "queue" not in st.session_state:
    st.session_state.queue = Queue()
if "ll" not in st.session_state:
    st.session_state.ll = SinglyLinkedList()

with left:
    st.subheader("Pick a data structure")
    ds = st.radio("Data Structure", ["Stack", "Queue", "Linked List"], horizontal=True)

    st.subheader("Operation panel")
    value = st.text_input("Value", value=str(random.randint(1, 99)))

    if ds == "Stack":
        op = st.selectbox("Operation", ["insert (push)", "delete (pop)", "peek", "search"])
        if st.button("Run"):
            s = st.session_state.stack
            try:
                if op == "insert (push)":
                    s.push(value)
                    st.success(f"Pushed {value}")
                elif op == "delete (pop)":
                    out = s.pop()
                    st.success(f"Popped {out}")
                elif op == "peek":
                    out = s.peek()
                    st.info(f"Top is {out}")
                elif op == "search":
                    found = value in s.to_list()
                    st.info(f"Found? {found}")
            except Exception as e:
                st.error(str(e))

    elif ds == "Queue":
        op = st.selectbox("Operation", ["insert (enqueue)", "delete (dequeue)", "peek", "search"])
        if st.button("Run"):
            q = st.session_state.queue
            try:
                if op == "insert (enqueue)":
                    q.enqueue(value)
                    st.success(f"Enqueued {value}")
                elif op == "delete (dequeue)":
                    out = q.dequeue()
                    st.success(f"Dequeued {out}")
                elif op == "peek":
                    out = q.peek()
                    st.info(f"Front is {out}")
                elif op == "search":
                    found = value in q.to_list()
                    st.info(f"Found? {found}")
            except Exception as e:
                st.error(str(e))

    else:
        op = st.selectbox("Operation", ["insert front", "insert back", "delete (by value)", "search"])
        if st.button("Run"):
            ll = st.session_state.ll
            if op == "insert front":
                ll.insert_front(value)
                st.success(f"Inserted {value} at front")
            elif op == "insert back":
                ll.insert_back(value)
                st.success(f"Inserted {value} at back")
            elif op == "delete (by value)":
                ok = ll.delete_value(value)
                st.info(f"Deleted? {ok}")
            elif op == "search":
                found = ll.search(value)
                st.info(f"Found? {found}")

    st.subheader("Complexity prediction (Big-O)")
    # Show predicted complexity for chosen op if available
    t, sp = predict(ds, op)
    st.write(f"**Time:** {t}")
    st.write(f"**Extra Space:** {sp}")

with right:
    st.subheader("Live visualization")
    if ds == "Stack":
        st.write("**Stack = LIFO** (last in, first out). Good for undo, backtracking, parsing.")
        st.code("Top\n ↓\n" + "\n".join(reversed([f"[ {x} ]" for x in st.session_state.stack.to_list()])) if len(st.session_state.stack) else "[ empty ]")
    elif ds == "Queue":
        st.write("**Queue = FIFO** (first in, first out). Good for task scheduling, buffering, breadth-first search.")
        items = st.session_state.queue.to_list()
        st.code("Front → " + "  ".join([f"[ {x} ]" for x in items]) + " ← Rear" if items else "[ empty ]")
    else:
        st.write("**Linked List** stores nodes that point to the next node. Good when inserts/removals are frequent and random access isn't needed.")
        items = st.session_state.ll.to_list()
        st.code("HEAD → " + " → ".join([f"({x})" for x in items]) + " → None" if items else "HEAD → None")

    st.subheader("When to use it (quick guide)")
    if ds == "Stack":
        st.markdown("- **Use when:** you need reverse order processing, undo, nesting, DFS/backtracking.\n- **Avoid when:** you need fast search by value.")
    elif ds == "Queue":
        st.markdown("- **Use when:** fair ordering matters (first come, first served), buffering work.\n- **Avoid when:** you need random access.")
    else:
        st.markdown("- **Use when:** inserts/removals in the middle matter and you can walk nodes.\n- **Avoid when:** you need fast indexing like `arr[i]`.")

    st.subheader("Complexity table")
    st.table({k: {op: f"{c.time}, {c.space}" for op, c in v.items()} for k, v in COMPLEXITIES.items()})
