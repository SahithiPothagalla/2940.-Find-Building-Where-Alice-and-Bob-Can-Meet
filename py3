class Solution:
    def leftmostBuildingQueries(self, heights: List[int], queries: List[List[int]]) -> List[int]:
        n = len(heights)
        # Initialize Sparse Table and Log table
        st = [[0] * 20 for _ in range(n)]
        Log = [-1] * (n + 1)
        
        # Compute Log values
        for i in range(1, n + 1):
            Log[i] = Log[i >> 1] + 1
        
        # Build the Sparse Table
        for i in range(n):
            st[i][0] = heights[i]
        for i in range(1, 20):
            for j in range(n):
                if j + (1 << i) <= n:
                    st[j][i] = max(st[j][i - 1], st[j + (1 << (i - 1))][i - 1])

        # Range Maximum Query using Sparse Table
        def Ask(l, r):
            k = Log[r - l + 1]
            return max(st[l][k], st[r - (1 << k) + 1][k])

        # Process queries
        res = []
        for l, r in queries:
            # Swap to ensure l < r for simplicity
            if l > r:
                l, r = r, l
            # Case 1: Same building
            if l == r:
                res.append(l)
                continue
            # Case 2: Alice can directly move to Bob
            if heights[r] > heights[l]:
                res.append(r)
                continue
            # Case 3: Binary search for the leftmost valid building
            max_height = max(heights[r], heights[l])
            left, right = r + 1, n
            while left < right:
                mid = (left + right) // 2
                if Ask(r + 1, mid) > max_height:
                    right = mid
                else:
                    left = mid + 1
            # Append result
            res.append(left if left != n else -1)
        return res
