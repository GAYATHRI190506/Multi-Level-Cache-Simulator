
from collections import deque
import random

class CacheLevel:
    def __init__(self, name, size_bytes, block_size, associativity, policy,
                 hit_latency, next_level=None):
        self.name = name
        self.num_lines = size_bytes // block_size
        self.block_size = block_size
        self.associativity = associativity
        self.num_sets = max(1, self.num_lines // associativity)
        self.policy = policy.upper()
        self.hit_latency = hit_latency
        self.next_level = next_level
        self.sets = [[] for _ in range(self.num_sets)]
        self.hits = 0
        self.misses = 0
        self.accesses = 0

    def _tag_set(self, address):
        block = address // self.block_size
        set_index = block % self.num_sets
        tag = block // self.num_sets
        return set_index, tag

    def access(self, address):
        self.accesses += 1
        set_index, tag = self._tag_set(address)
        cache_set = self.sets[set_index]

        for i, entry in enumerate(cache_set):
            if entry == tag:
                self.hits += 1
                if self.policy == "LRU":
                    cache_set.pop(i)
                    cache_set.insert(0, tag)
                return True

        self.misses += 1
        return False

    def insert(self, address):
        set_index, tag = self._tag_set(address)
        cache_set = self.sets[set_index]

        if tag in cache_set:
            if self.policy == "LRU":
                cache_set.remove(tag)
                cache_set.insert(0, tag)
            return

        if len(cache_set) >= self.associativity:
            if self.policy == "LRU":
                cache_set.pop()                 # least recently used
            elif self.policy == "FIFO":
                cache_set.pop(0)                # oldest
            elif self.policy == "RANDOM":
                cache_set.pop(random.randrange(len(cache_set)))
            else:
                raise ValueError("Unsupported policy")

        cache_set.insert(0, tag)

    def stats(self):
        hit_rate = (self.hits / self.accesses * 100) if self.accesses else 0
        miss_rate = 100 - hit_rate if self.accesses else 0
        return hit_rate, miss_rate


class MultiLevelCache:
    def __init__(self, policy="LRU"):
        self.l3 = CacheLevel("L3", 64*1024, 64, 4, policy, 30)
        self.l2 = CacheLevel("L2", 16*1024, 64, 4, policy, 8, self.l3)
        self.l1 = CacheLevel("L1", 4*1024, 64, 2, policy, 1, self.l2)
        self.memory_latency = 100
        self.memory_accesses = 0
        self.total_latency = 0

    def access(self, address):
        # Sequential lookup: each level adds its lookup latency.
        for level in (self.l1, self.l2, self.l3):
            if level.access(address):
                self.total_latency += level.hit_latency
                return level.name
            self.total_latency += level.hit_latency

        self.memory_accesses += 1
        self.total_latency += self.memory_latency

        # Fill lower-to-upper after a main-memory miss.
        for level in (self.l3, self.l2, self.l1):
            level.insert(address)
        return "Memory"

    def overall_stats(self):
        total = self.l1.accesses
        overall_hits = total - self.memory_accesses
        hit_rate = overall_hits / total * 100 if total else 0
        miss_rate = 100 - hit_rate if total else 0
        avg_latency = self.total_latency / total if total else 0
        return total, overall_hits, self.memory_accesses, hit_rate, miss_rate, avg_latency


def run_workload(policy, addresses):
    sim = MultiLevelCache(policy)
    for addr in addresses:
        sim.access(addr)

    total, hits, misses, hit_rate, miss_rate, avg_latency = sim.overall_stats()
    return {
        "policy": policy,
        "total": total,
        "l1_hit_rate": sim.l1.stats()[0],
        "l2_hit_rate": sim.l2.stats()[0],
        "l3_hit_rate": sim.l3.stats()[0],
        "overall_hit_rate": hit_rate,
        "overall_miss_rate": miss_rate,
        "avg_latency_ns": avg_latency,
        "memory_accesses": sim.memory_accesses
    }


def make_workload(n=1000):
    # Locality-heavy workload: repeated accesses to a small working set
    # mixed with occasional sequential accesses.
    addresses = []
    hot = [i * 64 for i in range(64)]          # 4 KB hot set
    for i in range(n):
        if i % 10 < 8:
            addresses.append(random.choice(hot))
        else:
            addresses.append((i * 4096) % (512 * 1024))
    return addresses


if __name__ == "__main__":
    random.seed(42)
    addresses = make_workload(1000)

    print("MULTI-LEVEL CACHE SIMULATOR")
    print("=" * 55)
    print("Configuration: L1=4KB/2-way, L2=16KB/4-way, L3=64KB/4-way")
    print("Block size=64B | Latencies: L1=1ns, L2=8ns, L3=30ns, RAM=100ns")
    print()

    results = []
    for policy in ("LRU", "FIFO", "RANDOM"):
        r = run_workload(policy, addresses)
        results.append(r)
        print(f"Policy: {policy}")
        print(f"  L1 Hit Rate      : {r['l1_hit_rate']:.2f}%")
        print(f"  L2 Hit Rate      : {r['l2_hit_rate']:.2f}%")
        print(f"  L3 Hit Rate      : {r['l3_hit_rate']:.2f}%")
        print(f"  Overall Hit Rate : {r['overall_hit_rate']:.2f}%")
        print(f"  Overall Miss Rate: {r['overall_miss_rate']:.2f}%")
        print(f"  Avg Latency      : {r['avg_latency_ns']:.2f} ns")
        print(f"  Memory Accesses  : {r['memory_accesses']}")
        print()

    print("BEST POLICY BY AVERAGE LATENCY:",
          min(results, key=lambda x: x["avg_latency_ns"])["policy"])
