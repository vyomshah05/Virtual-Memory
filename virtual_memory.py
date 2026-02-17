from collections import deque

PM_SIZE = 524288
FRAME_SIZE = 512
NUM_FRAMES = PM_SIZE // FRAME_SIZE
MASK9 = 0x1FF

def decode_va(va: int):
    s = (va >> 18) & MASK9
    p = (va >> 9)  & MASK9
    w = va & MASK9
    return s, p, w

def parse_triples(line: str):
    nums = list(map(int, line.split()))
    assert len(nums) % 3 == 0
    return [(nums[i], nums[i+1], nums[i+2]) for i in range(0, len(nums), 3)]

def init_memory(PM, init_line1: str, init_line2: str):
    """
    Returns: used_frames set
    """
    used = set()

    for s, z, f_pt in parse_triples(init_line1):
        PM[2*s] = z
        PM[2*s + 1] = f_pt
        if f_pt > 0:
            used.add(f_pt)

    for s, p, f_page in parse_triples(init_line2):
        f_pt = PM[2*s + 1]
        if f_pt > 0:
            PM[f_pt * FRAME_SIZE + p] = f_page
        if f_page > 0:
            used.add(f_page)

    return used

def build_free_frames(used):
    free = [f for f in range(NUM_FRAMES) if f not in used]
    return deque(free)

def load_block_into_frame(PM, D, block_idx: int, frame: int):
    base = frame * FRAME_SIZE
    PM[base:base+FRAME_SIZE] = D[block_idx][:]

def translate_va(va, PM, D, free_frames: deque, demand_paging: bool):
    s, p, w = decode_va(va)

    z = PM[2*s]
    if z <= 0:
        return -1

    if p * FRAME_SIZE + w >= z:
        return -1

    pt = PM[2*s + 1]
    if pt < 0:
        if not demand_paging:
            return -1
        # page fault on PT
        if not free_frames:
            raise RuntimeError("No free frames (shouldn't happen per spec).")
        newf = free_frames.popleft()
        load_block_into_frame(PM, D, -pt, newf)
        PM[2*s + 1] = newf
        pt = newf
    elif pt == 0:
        return -1

    pte_addr = pt * FRAME_SIZE + p
    page = PM[pte_addr]
    if page < 0:
        if not demand_paging:
            return -1
        # page fault on page
        if not free_frames:
            raise RuntimeError("No free frames (shouldn't happen per spec).")
        newf = free_frames.popleft()
        load_block_into_frame(PM, D, -page, newf)
        PM[pte_addr] = newf
        page = newf
    elif page == 0:
        return -1

    return page * FRAME_SIZE + w

def run(init_path, va_path, out_path, demand_paging: bool, D):
    PM = [0] * PM_SIZE

    with open(init_path) as f:
        line1 = f.readline().strip()
        line2 = f.readline().strip()

    used = init_memory(PM, line1, line2)
    free_frames = build_free_frames(used)

    with open(va_path) as f:
        vas = []
        for token in f.read().split():
            vas.append(int(token))

    outputs = []
    for va in vas:
        outputs.append(str(translate_va(va, PM, D, free_frames, demand_paging)))

    with open(out_path, "w") as f:
        f.write(" ".join(outputs))
