T = 10
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
dc = [-2,-1,1,2]

def check(r,c,L):
    for i in range(4):
        nc = c + dc[i]
        if 0 <= nc < L and graph[r][nc]:
            return False
    return True

for test_case in range(1, T + 1):
    N = int(input())
    heights = list(map(int,input().split()))
    L = max(max(heights)*2,len(heights))
    graph = [[0]*L for _ in range(L)]
    for c,height in enumerate(heights):
        if height == 0:
            continue
        for h in range(0,height):
            graph[h][c] = 1
    answer = 0
    for r in range(L):
        for c in range(L):
            if graph[r][c] and check(r,c,L):
                answer += 1            
    print(f"#{test_case} {answer}")