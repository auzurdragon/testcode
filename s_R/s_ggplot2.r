library(ggplot2)

# mt
mt <- data.frame(id=c(1:dim(mtcars)[1]),brand=row.names(mtcars), mtcars)

# 
p <- ggplot(mt)+
     geom_bar(aes(x=brand, y=cyl, fill=brand),stat='identity')+
     coord_flip()+
     coord_polar(theta='x')
