from pygraph.classes.digraph import digraph
import jieba
from pybloom_live import ScalableBloomFilter
from pygraph.classes.digraph import digraph

from copy import deepcopy
path='D:\BCMyproject\Flask\data\pagerank_seven_nodes.txt'

#path='D:/search_test3/lins.txt'
class PRIterator:
    __doc__ = '''计算一张图中的PR值'''
    def __init__(self, dg):
        self.damping_factor = 0.85  # 阻尼系数,即d
        self.max_iterations = 100 # 最大迭代次数
        self.min_delta = 0.00001  # 确定迭代是否结束的参数,即ϵ
        self.graph = dg

# 要计算的图 需要保证是一个闭环图
    def page_rank(self):
        for node in self.graph.nodes():
            if len(self.graph.neighbors(node)) == 0:# 将图中没有出链的节点改为对所有节点都有出链
                for node2 in self.graph.nodes():
                    if node2 != node:
                        digraph.add_edge(self.graph, (node, node2))#没有链出的节点 让它与其他几点都构建一条边 形成闭环图

        nodes = self.graph.nodes()
        graph_size = len(nodes)
        if graph_size == 0:
            return {}
        page_rank = dict.fromkeys(nodes, 1.0 / graph_size)#给每个节点赋予初始的PR值，此处的page_rank为字典

        damping_value = (1.0 - self.damping_factor) / graph_size#公式中的(1−d)/N部分

        print("初始值", page_rank)
        flag = False   #Flag:迭代结束的标志，初始为false；当为true时迭代结束

        for i in range(self.max_iterations):
            change = 0  # ji
            for node in nodes:
                rank = 0
                for incident_page in self.graph.incidents(node):  # 和他相连接的顶点（它的所有链入节点）
                    rank += self.damping_factor * (page_rank[incident_page] / len(self.graph.neighbors(incident_page)))
                rank += damping_value
                change += abs(page_rank[node] - rank)  # 绝对值
                page_rank[node] = rank
            print("This is NO.%s iteration" % (i + 1))
            print(page_rank)
            if change < self.min_delta:
                flag = True
                break
        if flag:
            print("finished in %s iterations!" % node)
        else:
            print("finished out of 100 iterations!")
        return page_rank

def read_data(path):
    node_list = []
    edge_list = []
    with open(path,encoding='utf8') as f:
        lines = f.readlines()
        nodes = lines[1].split(' ')#从1开始 汉字行不读取
        nodes[-1] = nodes[-1].split('\n')[0]#去除最后一个节点的换行符
        for node in nodes:
            node_list.append(node)
        edges = lines[3:]
        for edge in edges:
            edge = edge.split(' ')
            edge[1] = edge[1].split('\n')[0]#去除行末的换行符
            edge_list.append(edge)
    return node_list,edge_list


if __name__ == '__main__':
    node_list, edge_list = read_data(path)
    print('顶点信息：', node_list)
    print('边信息：', edge_list)
    #pagerank = open('data/summary.txt', 'w+', encoding='utf8')

    dg = digraph()
    dg.add_nodes(node_list)
    for edg in edge_list:
        dg.add_edge(edg)
    pr = PRIterator(dg)
    page_ranks = pr.page_rank()
    print(len(page_ranks))
    #for i in page_ranks:
        #pagerank.write(i+":"+page_ranks[i]+'\n')#字典
    print(page_ranks)



