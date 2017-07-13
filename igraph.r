library(igraph)
g <- graph(c(2,1,3,1,4,1,5,1,6,1,7,1), directed = F)
# par(mfrow=c(2,3))
# plot(g, vertex.size=40, layout=layout_on_grid, main='simple grid layout')
# plot(g, vertex.size=40, layout=layout.auto, main='auto layout')
# plot(g, vertex.size=40, layout=layout_as_star, main='star layout')
# plot(g, vertex.size=40, layout=layout.circle, main='circle layout')
# plot(g, vertex.size=40, layout=layout_randomly, main='randomly layout')
# plot(g, vertex.size=40, layout=layout_as_tree(g), main='tree layout')

library(RColorBrewer)
weight <- seq(1,3,length.out=ecount(g))
V(g)$color <- brewer.pal(9,"Set1")[1:vcount(g)] # 设置填充点的颜色
V(g)$frame.color <- NA  # 不显示点的边框
V(g)$label.color <- "white"  # 设置点标签颜色
V(g)$label.font <- 2         # 设置点标签的字体为粗体
V(g)$label.cex <- 2          # 设置点标签的字号
E(g)$width <- weight         # 根据边的权重设置边的粗细
E(g)$color <- "steelblue4"   # 设置边的颜色
E(g)$lty <- 2                # 设置边为虚线
plot(g, main="beautiful")
