---
title: "Configuración"
---

- Por favor, asegúrese de tener a mano un editor de hojas de cálculo, como LibreOffice, Microsoft Excel o Google Sheets.

- Instale R, RStudio y los paquetes (consulte más abajo).

### R y RStudio

- R y RStudio se descargan e instalan por separado. R es el entorno de computación estadística subyacente, pero usar R por sí solo no es muy interesante. RStudio es un entorno de desarrollo integrado (IDE) gráfico que hace que el uso de R sea mucho más sencillo e interactivo. Es necesario instalar R antes de instalar RStudio. Tras instalar ambos programas, deberá instalar algunos paquetes específicos de R dentro de RStudio. Siga las instrucciones a continuación según su sistema operativo y, a continuación, siga las instrucciones para instalar los paquetes.

### Está utilizando Windows

<br>

:::::::::::::::  solution

## Si ya tiene instalados R y RStudio

- Abra RStudio y haga clic en "Help" > "Check for updates". Si hay una versión nueva disponible, cierre RStudio y descargue la versión más reciente de RStudio.

- Para comprobar qué versión de R está utilizando, inicie RStudio; lo primero que aparece en la consola indicará la versión de R que está ejecutando. Alternativamente, puede escribir `sessionInfo()`, lo que también mostrará qué versión de R está ejecutando. Acceda al [sitio web de CRAN](https://cran.r-project.org/bin/windows/base/) y compruebe si hay una versión más reciente disponible. Si es así, descargue e instale la misma. Puede [consultar aquí](https://cran.r-project.org/bin/windows/base/rw-FAQ.html#How-do-I-UNinstall-R_003f) para obtener más información sobre cómo eliminar versiones antiguas de su sistema si así lo desea.

- Siga los pasos de las instrucciones [para todos](#for-everyone) al final de esta página.


:::::::::::::::::::::::::

:::::::::::::::  solution

## Si no tiene instalados R y RStudio

- Descargue R desde el [sitio web de CRAN](https://cran.r-project.org/bin/windows/base/release.htm).

- Ejecute el archivo `.exe` que acaba de descargar

- Vaya a la [página de descargas de RStudio](https://www.rstudio.com/products/rstudio/download/#download)

- En *All Installers*, seleccione **RStudio xxxx.yy.zz-uuu.exe - Windows 10/11** (donde x, y, z y u representan los números de versión)

- Haga doble clic en el archivo para instalarlo

- Una vez instalado, abra RStudio para asegurarse de que funcione y de que no aparezcan mensajes de error.

- Siga los pasos de las instrucciones [para todos](#for-everyone) al final de esta página.


:::::::::::::::::::::::::

### Está utilizando macOS

<br>

:::::::::::::::  solution

## Si ya tiene instalados R y RStudio

- Abra RStudio y haga clic en "Help" > "Check for updates". Si hay una versión nueva disponible, cierre RStudio y descargue la versión más reciente de RStudio.

- Para comprobar la versión de R que está utilizando, inicie RStudio; lo primero que aparece en la terminal indicará la versión de R que está ejecutando. Alternativamente, puede escribir `sessionInfo()`, lo que también mostrará qué versión de R está ejecutando. Acceda al [sitio web de CRAN](https://cran.r-project.org/bin/macosx/) y compruebe si hay una versión más reciente disponible. Si es así, por favor descargue e instale la misma.

- Siga los pasos de las instrucciones [para todos](#for-everyone) al final de esta página.


:::::::::::::::::::::::::

:::::::::::::::  solution

## Si no tiene instalados R y RStudio

- Descargue R desde el [sitio web de CRAN](https://cran.r-project.org/bin/macosx/).

- Seleccione el archivo `.pkg` para la versión más reciente de R

- Haga doble clic en el archivo descargado para instalar R

- También es recomendable instalar [XQuartz](https://www.xquartz.org/) (necesario para algunos paquetes)

- Vaya a la [página de descargas de RStudio](https://www.rstudio.com/products/rstudio/download/#download)

- En *All Installers*, seleccione **RStudio xxxx.yy.zz-uuu.dmg - macOS 10.15+** (donde x, y, z y u representan los números de versión)

- Haga doble clic en el archivo para instalar RStudio

- Una vez instalado, abra RStudio para asegurarse de que funcione y de que no aparezcan mensajes de error.

- Siga los pasos de las instrucciones [para todos](#for-everyone) al final de esta página.


:::::::::::::::::::::::::

### Está utilizando Linux

<br>

:::::::::::::::  solution

## Instale R con su gestor de paquetes e instale RStudio

- Siga las instrucciones de [CRAN](https://cloud.r-project.org/bin/linux) para su distribución; estas proporcionan información para obtener la versión más reciente de R para las distribuciones comunes. Para la mayoría de las distribuciones, podría utilizar su gestor de paquetes (por ejemplo, para Debian/Ubuntu ejecute `sudo apt-get install r-base`, y para Fedora `sudo yum install R`), pero no recomendamos este enfoque ya que las versiones proporcionadas por este suelen estar desactualizadas. En cualquier caso, asegúrese de tener al menos R 4.2.0.
- Vaya a la [página de descargas de RStudio](https://www.rstudio.com/products/rstudio/download/#download)
- En *All Installers*, seleccione la versión que coincida con su distribución e instálela con el método de su preferencia (por ejemplo, con Debian/Ubuntu `sudo dpkg -i rstudio-xxxx.yy.zz-uuu-amd64.deb` en la terminal).
- Una vez instalado, abra RStudio para asegurarse de que funcione y de que no aparezcan mensajes de error.
- Siga los pasos de las [instrucciones para todos](#for-everyone)


:::::::::::::::::::::::::

### Para todos {#for-everyone}

Tras instalar R y RStudio, deberá instalar un par de paquetes que se utilizarán durante el taller. También aprenderemos sobre la instalación de paquetes a lo largo del curso para explicar los siguientes comandos. Por ahora, simplemente siga las instrucciones a continuación:

- Inicie RStudio haciendo doble clic en el icono y luego escriba:

```r
install.packages(c("BiocManager", "remotes"))
BiocManager::install(c("tidyverse", "SummarizedExperiment", "hexbin",
                       "patchwork", "gridExtra", "lubridate"))
```
