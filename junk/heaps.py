
def xor_swap(arr, idx1, idx2):
    "Why not?"
    if idx1 != idx2:
        arr[idx1] = arr[idx1] ^ arr[idx2]
        arr[idx2] = arr[idx1] ^ arr[idx2]
        arr[idx1] = arr[idx1] ^ arr[idx2]


def swap(arr, idx1, idx2):
    "Less lines, less fun."
    temp = arr[idx1]
    arr[idx1] = arr[idx2]
    arr[idx2] = temp


def get_parent_idx(idx):
    if idx != 0:
        return (idx - 1) // 2


def get_left_child_idx(idx):
    return 2 * idx + 1


def get_right_child_idx(idx):
    return 2 * idx + 2


def get_swap_idx(semiheap, idx, bound=None):
    # returns None when the node passed no longer needs to be swapped.
    # hm the question here is should these out of range checks be factored out?
    left_idx = get_left_child_idx(idx)
    if bound is not None:
        lh = bound
    else:
        lh = len(semiheap)

    if left_idx < lh:
        parent = semiheap[idx]
        left = semiheap[left_idx]

        # we'll always need this.
        right_idx = get_right_child_idx(idx)
        if left > parent:
            if right_idx < lh and semiheap[right_idx] > left:
                return right_idx
            else:
                return left_idx
        elif right_idx < lh and semiheap[right_idx] > parent:
            return right_idx


def insert(heap, element):
    heap.append(element)
    curr_idx = len(heap) - 1
    parent_idx = get_parent_idx(curr_idx)

    while heap[parent_idx] < heap[curr_idx]:
        xor_swap(heap, parent_idx, curr_idx)
        curr_idx = parent_idx
        parent_idx = get_parent_idx(curr_idx)


# now that this is defined we can define sift_down
def sift_down(arr, idx, bound=None):
    curr_idx = idx
    swap_idx = get_swap_idx(arr, curr_idx, bound=bound)
    while swap_idx is not None:
        xor_swap(arr, curr_idx, swap_idx)
        curr_idx = swap_idx
        swap_idx = get_swap_idx(arr, curr_idx, bound=bound)


def heapify(arr):
    # the last half we initially preserve, including the middle (if it exists)
    idx = len(arr) // 2
    # resist the temptation to use some array slicing mechanism, as
    # that creates a copy and this is an in place sort :)
    # we want to decrement until -1
    while idx >= 0:
        sift_down(arr, idx)
        idx -= 1


def pop_max(heap, bound=None):
    if heap == []:
        raise IndexError("pop_max called on an empty heap")
    elif len(heap) == 1:
        return heap.pop()
    else:
        if bound is not None:
            lh = bound
        else:
            lh = len(heap) - 1
        xor_swap(heap, 0, lh)
        out = heap.pop()

        # now bubble down the inaccurate value at the top
        sift_down(heap, 0, bound)
        # heap is balanced
        return out


def heapsort_in_place(arr):
    heapify(arr)
    for bound in reversed(range(len(arr))):
        arr.append(
            pop_max(arr, bound=bound))


def heapsort(arr):
    heapify(arr)
    out = []
    for _ in range(len(arr)):
        out.append(pop_max(arr))
    arr.extend(out)

