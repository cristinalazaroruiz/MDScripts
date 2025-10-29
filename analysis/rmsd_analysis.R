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

##### FAD extendido ###########

# PATH to .xvg
ruta1 <-  "C:/Users/usuario/Desktop/clazaro_files/FPR/analisis_1100ns/graficas/rmsd_alineado_pdb_FAD_extendido"

# Get files with different patterns
# FAD extendido
replicas_FAD_extendido_backbone <- list.files(
  ruta,
  pattern = ".*.*FAD_extendido_.*rmsd_backbone_r[0-9]+\\.xvg$",
  full.names = TRUE
)

replicas_FAD_extendido_FAD <- list.files(
  ruta,
  pattern = ".*.*FAD_extendido_.*rmsd_FAD_r[0-9]+\\.xvg$",
  full.names = TRUE
)


#Read xvg files
rmsd_FAD_extendido_backbone <- read_xvg(replicas_FAD_extendido_backbone)
rmsd_FAD_extendido_FAD <- read_xvg(replicas_FAD_extendido_FAD)


##### FAD plegado ###########
ruta2 <-  "C:/Users/usuario/Desktop/clazaro_files/FPR/analisis_1100ns/graficas/rmsd_alineado_pdb_FAD_plegado"

replicas_FAD_plegado_backbone <- list.files(
  ruta2,
  pattern = ".*.*FAD_plegado_.*rmsd_backbone_r[0-9]+\\.xvg$",
  full.names = TRUE
)

replicas_FAD_plegado_FAD <- list.files(
  ruta2,
  pattern = ".*.*FAD_plegado_.*rmsd_FAD_r[0-9]+\\.xvg$",
  full.names = TRUE
)

#Read xvg files
rmsd_FAD_plegado_backbone <- read_xvg(replicas_FAD_plegado_backbone)
rmsd_FAD_plegado_FAD <- read_xvg(replicas_FAD_plegado_FAD)


##### FAD - NADPH - plegado###########

ruta3 <- "C:/Users/usuario/Desktop/clazaro_files/FPR/analisis_1100ns/graficas/rmsd_alineado_pdb_FAD_NADPH_plegado"

replicas_FAD_NADPH_plegado_backbone <- list.files(
  ruta3,
  pattern = ".*.*FAD_.*rmsd_backbone_r[0-9]+\\.xvg$",
  full.names = TRUE
)

replicas_FAD_NADPH_plegado_FAD <- list.files(
  ruta3,
  pattern = ".*.*FAD_.*rmsd_FAD_r[0-9]+\\.xvg$",
  full.names = TRUE
)


replicas_FAD_NADPH_plegado_NADP <- list.files(
  ruta3,
  pattern = ".*.*FAD_.*rmsd_NADP_r[0-9]+\\.xvg$",
  full.names = TRUE
)


#Read xvg files
rmsd_FAD_NADPH_plegado_backbone <- read_xvg(replicas_FAD_NADPH_plegado_backbone)
rmsd_FAD_NADPH_plegado_FAD <- read_xvg(replicas_FAD_NADPH_plegado_FAD)
rmsd_FAD_NADPH_plegado_NADP <- read_xvg(replicas_FAD_NADPH_plegado_NADP)


####### FADH - NADP - plegado ###############################################
ruta4 = "C:/Users/usuario/Desktop/clazaro_files/FPR/analisis_1100ns/graficas/rmsd_alineado_pdb_FADH_NADP_plegado"


replicas_FADH_NADP_plegado_backbone <- list.files(
  ruta4,
  pattern = ".*.*FADH_.*rmsd_backbone_r[0-9]+\\.xvg$",
  full.names = TRUE
)

replicas_FADH_NADP_plegado_FAD <- list.files(
  ruta4,
  pattern = ".*.*FADH_.*rmsd_FAD_r[0-9]+\\.xvg$",
  full.names = TRUE
)


replicas_FADH_NADP_plegado_NADP <- list.files(
  ruta4,
  pattern = ".*.*FADH_.*rmsd_NADP_r[0-9]+\\.xvg$",
  full.names = TRUE
)


#Read xvg files
rmsd_FADH_NADP_plegado_backbone <- read_xvg(replicas_FADH_NADP_plegado_backbone)
rmsd_FADH_NADP_plegado_FAD <- read_xvg(replicas_FADH_NADP_plegado_FAD)
rmsd_FADH_NADP_plegado_NADP <- read_xvg(replicas_FADH_NADP_plegado_NADP)


#################### FAD - NADPH - Extendido ############################

ruta5 <- "C:/Users/usuario/Desktop/clazaro_files/FPR/analisis_1100ns/graficas/rmsd_alineado_pdb_FAD_NADPH_ex"

replicas_FAD_NADPH_extendido_backbone <- list.files(
  ruta5,
  pattern = ".*.*FAD_.*rmsd_backbone_r[0-9]+\\.xvg$",
  full.names = TRUE
)

replicas_FAD_NADPH_extendido_FAD <- list.files(
  ruta5,
  pattern = ".*.*FAD_.*rmsd_FAD_r[0-9]+\\.xvg$",
  full.names = TRUE
)

replicas_FAD_NADPH_extendido_NADP <- list.files(
  ruta5,
  pattern = ".*.*FAD_.*rmsd_NADP_r[0-9]+\\.xvg$",
  full.names = TRUE
)

#Read xvg files
rmsd_FAD_NADPH_extendido_backbone <- read_xvg(replicas_FAD_NADPH_extendido_backbone)
rmsd_FAD_NADPH_extendido_FAD <- read_xvg(replicas_FAD_NADPH_extendido_FAD)
rmsd_FAD_NADPH_extendido_NADP <- read_xvg(replicas_FAD_NADPH_extendido_NADP)


#################### FADH - NADP - Extendido ############################
ruta5 <- "C:/Users/usuario/Desktop/clazaro_files/FPR/analisis_1100ns/graficas/rmsd_alineado_pdb"

replicas_FADH_NADP_extendido_backbone <- list.files(
  ruta5,
  pattern = ".*.*FADH_.*rmsd_backbone_r[0-9]+\\.xvg$",
  full.names = TRUE
)

replicas_FADH_NADP_extendido_FAD <- list.files(
  ruta5,
  pattern = ".*.*FADH_.*rmsd_FAD_r[0-9]+\\.xvg$",
  full.names = TRUE
)

replicas_FADH_NADP_extendido_NADP <- list.files(
  ruta5,
  pattern = ".*.*FADH_.*rmsd_NADP_r[0-9]+\\.xvg$",
  full.names = TRUE
)

#Read xvg files
rmsd_FADH_NADP_extendido_backbone <- read_xvg(replicas_FADH_NADP_extendido_backbone)
rmsd_FADH_NADP_extendido_FAD <- read_xvg(replicas_FADH_NADP_extendido_FAD)
rmsd_FADH_NADP_extendido_NADP <- read_xvg(replicas_FADH_NADP_extendido_NADP)





################################################################################
#                             Plots
################################################################################


plot_rmsd_xvg <- function(data_xvg,
                          titulo = "RMSD",
                          subtitulo = "",
                          colores = c("red", "blue", "green", "pink", "orange"),
                          replicas = 5,
                          tiempo_lim = c(0, 1100),
                          rmsd_lim = c(0, 0.4)) {
  
  # Generar el plot base usando plot_xvg de xvm
  p <- plot_xvg(
    data_xvg,
    merge = TRUE,
    title = titulo,
    subtitle = subtitulo
  )
  
  # Añadir estilo y capas personalizadas
  p <- p +
    scale_color_manual(
      name = "Réplica",
      values = colores[seq_len(replicas)],
      labels = paste("Réplica", seq_len(replicas))
    ) +
    labs(x = "Tiempo (ns)", y = "RMSD (nm)") +
    theme_minimal() +
    scale_x_continuous(limits = tiempo_lim, breaks = seq(tiempo_lim[1], tiempo_lim[2], 200)) +
    scale_y_continuous(limits = rmsd_lim) +
    theme(
      legend.position = "right",
      plot.title = element_text(size = 16, face = "bold"),
      plot.subtitle = element_text(size = 12),
      axis.title = element_text(size = 13),
      axis.text = element_text(size = 11),
      legend.title = element_text(size = 12),
      legend.text = element_text(size = 10)
    )
  
  return(p)
}

##### FAD extendido ###########

FAD_extendido_backbone_plot <- plot_rmsd_xvg(rmsd_FAD_extendido_backbone, 
                                             titulo = "RMSD FAD extendido", 
                                             subtitulo = "Backbone",
                                             rmsd_lim = c(0, 0.4))



FAD_extendido_FAD_plot <- plot_rmsd_xvg(rmsd_FAD_extendido_FAD, 
                                             titulo = "RMSD FAD extendido", 
                                             subtitulo = "FAD",
                                             rmsd_lim = c(0, 1.25))




##### FAD plegado ###########

FAD_plegado_backbone_plot <- plot_rmsd_xvg(rmsd_FAD_plegado_backbone, 
                                             titulo = "RMSD FAD plegado", 
                                             subtitulo = "Backbone",
                                             rmsd_lim = c(0, 0.4))



FAD_plegado_FAD_plot <- plot_rmsd_xvg(rmsd_FAD_plegado_FAD, 
                                        titulo = "RMSD FAD plegado", 
                                        subtitulo = "FAD",
                                        rmsd_lim = c(0, 1.25))



##### FAD - NADPH - plegado ###########


FAD_NADPH_plegado_backbone_plot <- plot_rmsd_xvg(rmsd_FAD_NADPH_plegado_backbone, 
                                           titulo = "RMSD FAD - NADPH - plegado", 
                                           subtitulo = "Backbone",
                                           rmsd_lim = c(0, 0.4))



FAD_NADPH_plegado_FAD_plot <- plot_rmsd_xvg(rmsd_FAD_NADPH_plegado_FAD, 
                                      titulo = "RMSD FAD - NADPH - plegado", 
                                      subtitulo = "FAD",
                                      rmsd_lim = c(0, 1.25))



FAD_NADPH_plegado_NADP_plot <- plot_rmsd_xvg(rmsd_FAD_NADPH_plegado_NADP, 
                                            titulo = "RMSD FAD - NADPH - plegado", 
                                            subtitulo = "NADPH",
                                            rmsd_lim = c(0, 4))



####### FADH - NADP - plegado ###############################################

FADH_NADP_plegado_backbone_plot <- plot_rmsd_xvg(rmsd_FADH_NADP_plegado_backbone,
                                                 titulo = "RMSD FADH - NADP - plegado",
                                                 subtitulo = "Backbone",
                                                 rmsd_lim = c(0, 0.4))

FADH_NADP_plegado_FAD_plot <- plot_rmsd_xvg(rmsd_FADH_NADP_plegado_FAD,
                                            titulo = "RMSD FADH - NADP - plegado",
                                            subtitulo = "FADH",
                                            rmsd_lim = c(0, 1.25))

FADH_NADP_plegado_NADP_plot <- plot_rmsd_xvg(rmsd_FADH_NADP_plegado_NADP,
                                             titulo = "RMSD FADH - NADP - plegado",
                                             subtitulo = "NADP",
                                             rmsd_lim = c(0, 4))



#################### FAD - NADPH - Extendido ############################

FAD_NADPH_extendido_backbone_plot <- plot_rmsd_xvg(rmsd_FAD_NADPH_extendido_backbone,
                                                   titulo = "RMSD FAD - NADPH extendido",
                                                   subtitulo = "Backbone",
                                                   rmsd_lim = c(0, 0.4))


FAD_NADPH_extendido_FAD_plot <- plot_rmsd_xvg(rmsd_FAD_NADPH_extendido_FAD,
                                          titulo = "RMSD FAD - NADPH - extendido",
                                          subtitulo = "FAD",
                                          rmsd_lim = c(0, 1.25))




FAD_NADPH_extendido_NADP_plot <- plot_rmsd_xvg(rmsd_FAD_NADPH_extendido_NADP,
                                               titulo = "RMSD FAD - NADPH - extendido",
                                               subtitulo = "NADPH",
                                               rmsd_lim = c(0, 4))




#################### FADH - NADP - Extendido ############################



FADH_NADP_extendido_backbone_plot <- plot_rmsd_xvg(rmsd_FADH_NADP_extendido_backbone,
                                                   titulo = "RMSD FADH - NADP extendido",
                                                   subtitulo = "Backbone",
                                                   rmsd_lim = c(0, 0.4))


FADH_NADP_extendido_FAD_plot <- plot_rmsd_xvg( rmsd_FADH_NADP_extendido_FAD,
                                              titulo = "RMSD FADH - NADP - extendido",
                                              subtitulo = "FADH",
                                              rmsd_lim = c(0, 1.25))




FADH_NADP_extendido_NADP_plot <- plot_rmsd_xvg(rmsd_FADH_NADP_extendido_NADP,
                                               titulo = "RMSD FADH - NADP - extendido",
                                               subtitulo = "NADP",
                                               rmsd_lim = c(0, 4))



################################################################################
#                             Merge
################################################################################

#### Backbone ######
backbone_plots <- grid.arrange(FAD_extendido_backbone_plot, FAD_plegado_backbone_plot,
             FAD_NADPH_extendido_backbone_plot, FAD_NADPH_plegado_backbone_plot,
             FADH_NADP_extendido_backbone_plot, FADH_NADP_plegado_backbone_plot,
             ncol = 3)



FAD_plots <- grid.arrange(FAD_extendido_FAD_plot, FAD_plegado_FAD_plot,
                          FAD_NADPH_extendido_FAD_plot, FAD_NADPH_plegado_FAD_plot,
                          FADH_NADP_extendido_FAD_plot, FADH_NADP_plegado_FAD_plot)



NADP_plots <- grid.arrange(FAD_NADPH_extendido_NADP_plot, FAD_NADPH_plegado_NADP_plot,
                          FADH_NADP_extendido_NADP_plot, FADH_NADP_plegado_NADP_plot,
                          ncol = 2)




################################################################################
#                             Save
################################################################################

pdf("rmsd_backbone_definitivo.pdf", width = 14, height = 8)
grid.arrange(
  backbone_plots
)
dev.off()



pdf("rmsd_FAD_definitivo.pdf", width = 14, height = 8)
grid.arrange(
  FAD_plots
)
dev.off()


pdf("rmsd_NADP_definitivo.pdf", width = 14, height = 8)
grid.arrange(
  NADP_plots
)
dev.off()






