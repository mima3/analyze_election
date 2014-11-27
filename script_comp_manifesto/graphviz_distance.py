# -*- coding: utf-8 -*-
import pydot


def draw_distance(distance_result, output_file, font_path):
    """
    •¶ÍŠÔ‚Ì‹——£‚ðGraphViz‚Å•\Œ»‚·‚é
    @param distance_result •¶ÍŠÔ‚Ì‹——£
    @param output_file o—Íæ
    """
    cnt = 0
    sum = 0.0
    for f, dic in distance_result.items():
        max = -99999.99
        min = 9999.99
        max_node = ""
        min_node = ""

        for t, d in dic.items():
            print ("%s -> %s : %f" % (f, t, d))
            if max < d:
                max = d
                max_node = t
            if min > d:
                min = d
                min_node = t
            cnt = cnt + 1
            sum = sum + d
        print ("....... max:%s(%f) min:%s(%f)" % (max_node, max, min_node, min))

    avg = sum / cnt
    print "average %f" % (avg)
    graph = pydot.Dot(graph_type='graph')
    nodes = {}
    for f, dic in distance_result.items():
        nodes[f] = pydot.Node(f, label=f, style="filled", fillcolor="white", fontname=font_path, shape="box")
        graph.add_node(nodes[f])

    records = []
    for f, dic in distance_result.items():
        for t, d in dic.items():
            nf = nodes[f]
            nt = nodes[t]
            if (t + f) in records:
                graph.add_edge(pydot.Edge(nf, nt, len=(d / avg * 10)))
                print "%s - %s - %f" % (f, t, d / avg * 10)
            records.append(f + t)
    graph.write_png(output_file, prog='neato')
