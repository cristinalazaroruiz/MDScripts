
################################################################################
#                             Libraries
################################################################################
#install.packages("xvm")
library(dplyr)
library(ggplot2)
library(xvm) #read_xvg
library(gridExtra)
library(cowplot) #get_leyend

################################################################################
#                             Load data
################################################################################

rmsd_data <- read_xvg(c(
  "complex_FADH_NADP_extendido_1100ns_backbone_R1.xvg",
  "complex_FADH_NADP_extendido_1100ns_backbone_R2.xvg"
))

rmsd_data2 <- read_xvg(c(
  "complex_FADH_NADP_extendido_1100ns_backbone_R3.xvg",
  "complex_FADH_NADP_extendido_1100ns_backbone_R4.xvg"
))



################################################################################
#                             Create Plots
################################################################################

#Plot 1
rmsd_plot <- plot_xvg(
  rmsd_data,
  merge = TRUE,
  title = "RMSD",
  subtitle = "Réplicas 1 y 2"
) +
  scale_color_manual(values = c("red", "blue")) +
  labs(x = "Tiempo (ns)", y = "RMSD (Å)") +
  theme_minimal()

#Modify limits
rmsd_plot <- rmsd_plot +
  scale_x_continuous(limits = c(0, 1100), breaks = seq(0, 1100, 200)) +
  scale_y_continuous(limits = c(0, 0.35)) #we can add breaks too

#Change leyend labels and position
rmsd_plot <- rmsd_plot +
  scale_color_manual(
    name = "Réplica",                     # new legend title
    values = c("red", "blue"),            # colors
    labels = c("Réplica 1", "Réplica 2")  # names in the leyend
  ) + theme(legend.position = "none")     # position of the leyend
  
#positions:
#Right (default) > position = "right"
#Left > position = "left"
#Top > position = "top"
#Bottom > position = "bottom"
#without leyend > poosition = "none"



#Adjust size
rmsd_plot <- rmsd_plot +
  theme(
    plot.title = element_text(size = 16, face = "bold"),
    plot.subtitle = element_text(size = 12),
    axis.title = element_text(size = 13),
    axis.text = element_text(size = 11),
    legend.title = element_text(size = 12),
    legend.text = element_text(size = 10)
  )

#view plot
rmsd_plot

#Plot 2
rmsd_plot2 <- plot_xvg(
  rmsd_data2,
  merge = TRUE,
  title = "RMSD",
  subtitle = "Réplicas 3 y 4"
) +
  scale_color_manual(values = c("red", "blue")) +
  labs(x = "Tiempo (ns)", y = "RMSD (Å)") +
  theme_minimal()


rmsd_plot2 <- rmsd_plot +
  scale_x_continuous(limits = c(0, 1100), breaks = seq(0, 1100, 200)) +
  scale_y_continuous(limits = c(0, 0.35))


rmsd_plot2 <- rmsd_plot +
  scale_color_manual(
    name = "Réplica",                     # nuevo título de la leyenda
    values = c("red", "blue"),            # colores
    labels = c("Réplica 3", "Réplica 4")  # nombres dentro de la leyenda
  )+ theme(legend.position = "none")



rmsd_plot2 <- rmsd_plot +
  theme(
    plot.title = element_text(size = 16, face = "bold"),
    plot.subtitle = element_text(size = 12),
    axis.title = element_text(size = 13),
    axis.text = element_text(size = 11),
    legend.title = element_text(size = 12),
    legend.text = element_text(size = 10)
  )


#View plot two
rmsd_plot2

#Get leyend from one plot (if all equal)
#First get this leyend and then put position="none" in individual plots for grid

leyenda <- get_legend(rmsd_plot)


#Grid
grid.arrange(
  arrangeGrob(rmsd_plot, rmsd_plot2, nrow = 1),
  leyenda,
  nrow = 2,
  heights = c(10, 1))# propotion bewteen plot area and leyend area








