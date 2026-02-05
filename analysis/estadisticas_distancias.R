################################################################################
#                             Libraries
################################################################################
#install.packages("xvm")
library(dplyr)
library(ggplot2)
library(xvm) #read_xvg
library(gridExtra)
library(cowplot) #get_leyend
library(tidyr)
library(openxlsx)

################################################################################
#                             Load data
################################################################################

### Load each replica

# PATH to .xvg
ruta <-  "C:/Users/crist/Desktop/trabajo_unizar/MurA_articulo/dinamicas_Diego_MurA/closed+UNAG"
ruta_uni <- "C:/Users/usuario/Desktop/clazaro_files/MurA_articulo/dinamicas_Diego_MurA/closed+UNAG"
ruta_uni2 <-"C:/Users/usuario/Desktop/clazaro_files/MurA_articulo/dinamicas_Diego_MurA/distancias_UNAG"

replicas <- list.files(
  ruta_uni2,
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


# Ahora seleccionamos solo las distancias que nos interesan

distancias_interes <- c(
  "Time(ns)",
  "Asn23(ND2)-UNAG(O4Y)",
  "Asn23(OD1)-UNAG(O4Y)",
  "Asp316(OD2)-UNAG(O3Y)",
  "Asp316(OD1)-UNAG(O3Y)",
  "Gly175(N)-UNAG(O1B)",
  "Val174(N)-UNAG(O1A)",
  "Val172(O)-UNAG(O4B)",
  "Asp134(OD1)-UNAG(O4)",
  "Asp(134(OD2)-UNAG(O4))",
  "Ser173(OG)-UNAG(O4B)",
  "Arg131(NH2)-UNAG(O4)",
  "Leu135(N)-UNAG(O4)"
)


distancias_seleccionadas <- distancias


for (i in seq_along(distancias)) {
  
  df_2 <- distancias[[i]][["data"]]
  
  df_2 <- df_2 %>% select(all_of(distancias_interes))
  df_2 <- df_2[df_2[["Time(ns)"]]>=15, ] #quitamos los primeros 15ns
  
  distancias_seleccionadas[[i]][["data"]] <- df_2
  
}


#Ahora que ya tenemos las distancias que nos interesan, calculamos para cada
# columna la media y la desviacion estandar

#definimos el dataframe con los estadisticos que nos interesan
df_statistics <- data.frame(
  distancia = distancias_interes[distancias_interes != "Time(ns)"],
  media_R1 = rep(0, times=12), sd_R1 = rep(0, times = 12),
  media_R2 = rep(0, times=12), sd_R2 = rep(0, times = 12),
  media_R3 = rep(0, times=12), sd_R3 = rep(0, times = 12),
  media_R4 = rep(0, times=12), sd_R4 = rep(0, times = 12),
  media_R5 = rep(0, times=12), sd_R5 = rep(0, times = 12)
)

#quitamos la variable tiempo, que no interesa para la media y sd
columnas_distancia <- distancias_interes[distancias_interes != "Time(ns)"]

#recorremos las diferentes ditsancias que hay
for (j in seq_along(columnas_distancia)) {
  col_name <- columnas_distancia[j]
  
  #recorremos cada replica
  for (i in seq_along(distancias_seleccionadas)) {
    df_replica <- distancias_seleccionadas[[i]][["data"]]
    
    media <- mean(df_replica[[col_name]], na.rm = TRUE)
    sd_val <- sd(df_replica[[col_name]], na.rm = TRUE)
    
    # Guardar en df_statistics
    df_statistics[j, paste0("media_R", i)] <- media
    df_statistics[j, paste0("sd_R", i)] <- sd_val
  }
}

#cambiamos el formato de la grafica
df_statistics_long <- df_statistics %>%
  pivot_longer(
    cols = -distancia,
    names_to = c(".value", "Replica"),
    names_pattern = "(.*)_R(\\d)"
  )

#barplot
p <- ggplot(df_statistics_long, aes(x = distancia, y = media, fill = Replica)) +
  geom_col(position = position_dodge(width = 0.9)) +
  geom_errorbar(
    aes(ymin = media - sd, ymax = media + sd),
    position = position_dodge(width = 0.9),
    width = 0.2
  ) +
  theme_bw() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1, size = 10)
  ) +
  labs(
    x = "Distance",
    y = "Mean (Å)",
    fill = "Replica",
    title = "Mean and sd per replica and distance (time 15-200ns)"
  )+scale_y_continuous(
    limits = c(0, 16),
    breaks = seq(0, 16, by = 2),
    expand = expansion(mult = c(0, 0.05))
  )+scale_fill_manual(
    values = c(
      "1" = "darkgray",
      "2" = "red",
      "3" = "blue",
      "4" = "green",
      "5" = "purple"
    )
  ) 

p

#ahora preparamos otro plot, donde solo nos quedamos con los frames (tiempos)
#donde la distancia es igual o menor a la media

#primero tenemos que hacer los calculos
#vamos a añadir esta informacion en df_statistics_long

frames <- rep(0, times = length(df_statistics_long$distancia))
frames_porcentaje <- rep(0, times = length(df_statistics_long$distancia))
df_statistics_long$frames <- frames
df_statistics_long$frames_porcentaje <- frames_porcentaje

for (i in seq_along(columnas_distancia)) {
  col_dist <- columnas_distancia[i]  # nombre de la distancia#recorremos las distancias
  for (j in seq_along(distancias_seleccionadas)) {
    df_replica <- distancias_seleccionadas[[j]][["data"]]
    #seleccionamos la media correspondiente
    media_val <- df_statistics_long$media[
      df_statistics_long$distancia == col_dist & df_statistics_long$Replica == as.character(j)
    ]
    #ahora contamos los registros que cumplen dicha condicion
    n_frames <- sum(df_replica[[col_dist]] <= media_val, na.rm = TRUE)
    porcentaje_frames <- (n_frames/18501)*100
    
    # guardar en df_statistics_long
    df_statistics_long$frames[
      df_statistics_long$distancia == col_dist & df_statistics_long$Replica == as.character(j)
    ] <- n_frames
    df_statistics_long$frames_porcentaje[df_statistics_long$distancia == 
    col_dist & df_statistics_long$Replica == as.character(j)] <- porcentaje_frames
    
  }
  
  
}

#plot con los porcentajes
p2 <- ggplot(df_statistics_long, aes(x = distancia, y = frames_porcentaje, fill = Replica))+
  geom_col(position = position_dodge((width = 0.9)))+theme_bw()+
             theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 10)
             ) +
  labs(
    x = "Distance",
    y = "% Frames under mean",
    fill = "Replica",
    title = "% Frames under mean per replica and distance (time 15-200ns)"
  )+scale_y_continuous(
    limits = c(0, 100),
    breaks = seq(0, 100, by = 10),
    expand = expansion(mult = c(0, 0.05))
  )+scale_fill_manual(
    values = c(
      "1" = "darkgray",
      "2" = "red",
      "3" = "blue",
      "4" = "green",
      "5" = "purple"
    )
  ) 

p2


#guardar plots en pdf
pdf("resumen_distancias.pdf", width = 14, height = 8)
p
dev.off()


pdf("porcentaje_frames.pdf",width = 14, height = 8 )
p2
dev.off()


write.xlsx(df_statistics_long, 'estidsticas_distancias.xlsx')


###############################################################################
#Necesitamos preparar los datos para hacer la tabla suplementaria
#Primero, para la tabla, los datos est aran en formato wide, asi que pasamos el
#df en formato lon a formato wide


df_suplementary <- df_statistics_long %>%
  pivot_wider(
    names_from = "Replica",
    values_from = c("media", "sd", "frames","frames_porcentaje"),
  )

#Ahora necesitamos calcular los valores promedio de las cinco replicas

df_summary <- df_statistics_long %>%
  group_by(distancia) %>%
  summarise(
    mean_dist_replicas = mean(media),
    sd_dist_replicas   = sd(media),
    mean_frames        = mean(frames_porcentaje),
    sd_frames          = sd(frames_porcentaje)
  )
  
#Esto lo añadimos a nuestro df_suplementary con un left join

df_suplementary <- df_suplementary%>%
  left_join(df_summary, by = "distancia")

#Ahora queremos que la desviacion estandar aparezca con un +- en la celda de la media

#queremos que la media y la desviacion estandar esten en la misma celda
# Convertir las columnas a numéricas
#primero lo aplicamos a todas las replicas: 

media_cols <- grep("^media_", names(df_suplementary), value = TRUE)
sd_cols    <- grep("^sd_", names(df_suplementary), value = TRUE)

for (i in seq_along(media_cols)) {
  
  new_col <- sub("media_", "", media_cols[i])   # media_1 → 1
  
  # Convertir a numérico antes de redondear
  media_val <- round(as.numeric(df_suplementary[[media_cols[i]]]), 2)
  sd_val    <- round(as.numeric(df_suplementary[[sd_cols[i]]]), 2)
  
  df_suplementary[[paste0(new_col, "_pm")]] <- paste0(media_val, " ± ", sd_val)
}


#ahora lo aplicamos a la media de todas las replicas y y la media de todos los frames


df_suplementary$mean_pm <- NA  # inicializar columna

for (i in seq_len(nrow(df_suplementary))) {
  
  media_val <- round(as.numeric(df_suplementary$mean_dist_replicas[i]), 2)
  sd_val    <- round(as.numeric(df_suplementary$sd_dist_replicas[i]), 2)
  
  df_suplementary$mean_pm[i] <- paste0(media_val, " ± ", sd_val)
}


#y tambien para los frames

df_suplementary$mean_frames_pm <- NA

for (i in seq_len(nrow(df_suplementary))) {
  
  media_val2 <- round(df_suplementary$mean_frames[i], 2)
  sd_val2    <- round(df_suplementary$sd_frames[i], 2)
  
  df_suplementary$mean_frames_pm[i] <- paste0(media_val2, " ± ", sd_val2)
}


#guardamos

write.xlsx(df_suplementary, 'prueba.xlsx')



