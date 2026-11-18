# -*- coding: utf-8 -*-
"""Plus court chemin documenté entre deux fiches. Chaque étape est un lien déjà sourcé."""
from collections import deque


def shortest_path(edges, start, end):
    """Retourne la liste des liens, ou None s'il n'y a pas de chemin. start == end : liste vide."""
    if not start or not end:
        return None
    if start == end:
        return []
    adj = {}
    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if not src or not tgt or src == tgt:
            continue
        adj.setdefault(src, []).append((tgt, edge))
        adj.setdefault(tgt, []).append((src, edge))
    seen = {start}
    queue = deque([start])
    prev = {}
    while queue:
        cur = queue.popleft()
        for nxt, edge in adj.get(cur, []):
            if nxt in seen:
                continue
            seen.add(nxt)
            prev[nxt] = (cur, edge)
            if nxt == end:
                queue.clear()
                break
            queue.append(nxt)
    if end not in prev:
        return None
    steps = []
    node = end
    while node != start:
        cur, edge = prev[node]
        steps.append(edge)
        node = cur
    steps.reverse()
    return steps
