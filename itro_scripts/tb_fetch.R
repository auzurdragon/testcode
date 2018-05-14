library(ggplot2)
library(party)

td <- read.csv('tmp/tb_fetch.csv')
levels(td$size) <- c("NB", "S", "M", "L", "XL", "XXL", "XXXL")
ggplot(td)+geom_point(aes(x=size, y = users))
tree_td <- ctree(check_users ~ product_price + product_num + product_brand + product_size, data =td)