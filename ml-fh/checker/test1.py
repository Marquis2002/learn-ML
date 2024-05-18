# 读入地图的行数和列数
rows, cols = map(int, input().split())

# 初始化地图
map_data = []
for _ in range(rows):
    line = input().strip()  # 读入每行地图数据
    map_data.append(line)