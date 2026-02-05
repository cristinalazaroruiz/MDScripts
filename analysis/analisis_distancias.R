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

### Load each replica

# PATH to .xvg
ruta <-  "C:/Users/crist/Desktop/trabajo_unizar/MurA_articulo/dinamicas_Diego_MurA/closed+UNAG"
ruta_uni <- "C:/Users/usuario/Desktop/clazaro_files/MurA_articulo/dinamicas_Diego_MurA/closed+UNAG"

replicas <- list.files(
  ruta_uni,
  pattern = "*.xvg$",
  full.names = TRUE
)
  
#Read xvg files
distancias <- read_xvg(replicas)

nombres_distancias <- c( "Time(ns)", "Asn23(ND2)-UNAG(O4Y)", "Asn23(ND2)-UNAG(O3Y)",
                        "Asn23(ND2)-UNAG(O6Y)", "Asn23(ND2)-UNAG(O7Y)",
                        "Asn23(OD1)-UNAG(O4Y)", "Asn23(OD1)-UNAG(O3Y)",
                        "Asn23(OD1)-UNAG(N2Y)", "Asn23(OD1)-UNAG(O7Y)",
                        "Arg102(NE)-UNAG(O7Y)", "Arg102(NH2)-UNAG(O7Y)",
                        "Asp316(OD2)-UNAG(O3Y)", "Asp316(OD2)-UNAG(O4Y)",
                        "Asp316(OD1)-UNAG(O4Y)", "Asp316(OD1)-UNAG(O3Y)",
                        "Arg342(NH2)-UNAG(O4Y)", "Glu201(OE1)-UNAG(O6Y)",
                        "Glu201(OE2)-UNAG(O6Y)", "Arg243(NH2)-UNAG(O6Y)",
                        "Arg131(NH2)-UNAG(O2B)", "Arg131(NE)-UNAG(O2B)",
                        "Ser173(OG)-UNAG(O2A)", "Ser173(OG)-UNAG(O1A)",
                        "Gly175(N)-UNAG(O1B)", "Gly175(N)-UNAG(O2A)",
                        "Val174(N)-UNAG(O1A)", "Lys171(NZ)-UNAG(O3B)",
                        "Lys171(NZ)-UNAG(O2Y)", "Lys(NZ)-UNAG(O2)",
                        "Val172(O)-UNAG(O4B)", "Val172(O)-UNAG(O2Y)",
                        "Asp134(N)-UNAG(O4)", "Asp134(OD1)-UNAG(O4)",
                        "Asp(134(OD2)-UNAG(O4))", "Leu136(N)-UNL(O4)",
                        "Ser173(OG)-UNAG(N1)", "Ser173(OG)-UNAG(O4B)",
                        "Arg131(NH2)-UNAG(O4)", "Arg131(NH2)-UNAG(O2Y)",
                        "Arg131(NH2)-UNAG(O3B)", "Arg131(NE)-UNAG(O2Y)",
                        "Leu135(N)-UNAG(O4)", "Glu340(OE1)-UNAG(O2Y)",
                        "Glu340(OE2)-UNAG(O2Y)", "Glu340(OE1)-UNAG(O3B)",
                        "Glu340(OE2)-UNAG(O3B)", "Pro132(O)-UNAG(O4)",
                        "Ile338(O)-UNAG(O3B)")



for (i in seq_along(distancias)) {
  
  df <- distancias[[i]][["data"]]
  colnames(df) <- nombres_distancias
  
  # Para todas las columnas que NO sean Time(ns)
  columnas_a_multiplicar <- colnames(df) != "Time(ns)"
  
  df[ , columnas_a_multiplicar] <- df[ , columnas_a_multiplicar] * 10
  
  distancias[[i]][["data"]] <- df
}



################################################################################
#                             Plots
################################################################################

#plotear cada tipo de distancia 
plot_distancias_replicas <- function(distancias, 
                                     nombres_distancias,
                                     colores = c("red", "blue", "green", "pink", "orange"),
                                     tiempo_lim = c(0, 200),
                                     rmsd_lim = c(0, 20)) {
  
  plots <- list()  # aquí guardaremos todos los plots
  
  # Iterar por cada distancia (exceptuando "Time(ns)")
  for (distancia in nombres_distancias[-1]) {
    
    # Crear un data frame combinando todas las réplicas
    df_plot <- do.call(rbind, lapply(seq_along(distancias), function(i) {
      df <- distancias[[i]]$data
      data.frame(
        Time = df[["Time(ns)"]],
        Distancia = df[[distancia]],
        Replica = paste0("Réplica ", i)
      )
    }))
    
    # Crear el plot con ggplot
    p <- ggplot(df_plot, aes(x = Time, y = Distancia, color = Replica)) +
      geom_line(size = 1) +
      labs(
        title = paste("Distancia:", distancia),
        x = "Tiempo (ns)",
        y = "Distancia (Å)"
      ) +
      scale_color_manual(values = colores[seq_along(distancias)]) +
      scale_x_continuous(limits = tiempo_lim) +
      scale_y_continuous(limits = rmsd_lim) +
      theme_minimal() +
      theme(
        legend.position = "right",
        plot.title = element_text(size = 16, face = "bold"),
        axis.title = element_text(size = 13),
        axis.text = element_text(size = 11),
        legend.title = element_text(size = 12),
        legend.text = element_text(size = 10)
      )
    
    # Guardar el plot en la lista
    plots[[distancia]] <- p
  }
  
  return(plots)
}


plots_distancias <- plot_distancias_replicas(distancias, nombres_distancias)

# ver cada distancia en R
for (p in plots_distancias) {
  print(p)
}


#imprimir cada grafico en pdf
for (p in plots_distancias) {
  nombre <- paste0("Distancia_", gsub("[^a-zA-Z0-9_]", "_", p[["labels"]][["title"]]), ".pdf")
  
  pdf(nombre, width = 14, height = 8)
  print(p)
  dev.off()
  
}

# En vez de imprimir cada gráfica individualmente, imprimimos en tres pdfs
# fracción de glucosamina, fracción ppi y fracción de UDP 

legend <- get_legend(plots_distancias[[1]])
plots_modificados1 <- lapply(plots_distancias[1:18], function(p) {
  p + 
    theme(
      plot.title = element_text(size = 10, face = "bold"),  # tamaño del título
      axis.title = element_text(size = 8),                  # tamaño de ejes
      axis.text = element_text(size = 7),                   # tamaño de los números
      legend.position = "none"                              # quitar leyenda
    )
})


plots_modificados2 <- lapply(plots_distancias[26:length(plots_distancias)], function(p) {
  p + 
    theme(
      plot.title = element_text(size = 10, face = "bold"),  # tamaño del título
      axis.title = element_text(size = 8),                  # tamaño de ejes
      axis.text = element_text(size = 7),                   # tamaño de los números
      legend.position = "none"                              # quitar leyenda
    )
})

plots_modificados3 <- lapply(plots_distancias[19:25], function(p) {
  p + 
    theme(
      plot.title = element_text(size = 10, face = "bold"),  # tamaño del título
      axis.title = element_text(size = 8),                  # tamaño de ejes
      axis.text = element_text(size = 7),                   # tamaño de los números
      legend.position = "none"                              # quitar leyenda
    )
})



pdf("fraccion_glucosamina_v3.pdf", width = 14, height = 8)
do.call(grid.arrange, c(plots_modificados1, list(legend)))
dev.off()



pdf("fraccion_ppi_v3.pdf", width = 14, height = 8)
do.call(grid.arrange, c(plots_modificados3, list(legend)))
dev.off()

pdf("fraccion_adenina_v3.pdf", width = 14, height = 8)
do.call(grid.arrange, c(plots_modificados2, list(legend)))
dev.off()



  
  