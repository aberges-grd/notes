---
title: Plantilla _Clean Architecture_
abstract: |
    Se trata de anotar el uso de la plantilla creada por Diego, 
    ya que parece ser que tiene una curva de aprendizaje algo alta.
header-includes: |
    \usepackage{dirtree}
pandoc-options:
  - --filter=pandoc-include
---

# Explicación de _Clean Architecture_

Se trata de una arquitectura por capas tal y como describe el siguiente diagrama[^1]:

![diagrama clean architecture por Robert C. Martin](media/CleanArchitecture.jpg){ width=80% #fig:clean_arch }

La arquitectura es una variación barra unificación de otras previas como _Screaming
Architecture_, _Onion Architecture_ o _Hexagonal Architecture_. Dichas arquitecturas
tienen por objetivo producir sistemas que sean independientes de la elección del
framework, UI o BBDD y testables. Se destila en el concepto de _Clean Architecture_
propuesto por Robert C. Martin (Uncle Bob) en su libro homónimo [@martin2017clean].

El principio fundamental de cualquiera de ellas es: las dependencias de código apuntan
hacia el centro de la [@fig:clean_arch]. Esto es, ningún elemento de un círculo interno
puede saber nada de lo que hay en un círculo externo, o dicho de otro modo: nada
declarado en un círculo externo debe aparecer en un círculo interno.

[^1]: visto en [@martin2012blog].

## Estructura

La estructura de la arquitectura se basa en 4 capas (de "más interno" a "más externo"):
_Entities_, _Use Cases_, _Interface Adapters_ y _Frameworks and Drivers_. Paso a
explicar brevemente cada una:

##### Entidades
En el círculo más interno estaría la "lógica de negocio" (Martin las llama "_Entities_",
Entidades). En teoría es la capa de abstracción más alta y por tanto reusable del
código; en el caso de tener una aplicación sencilla se trataría de objetos simples (por
ejemplo una `dataclass` en Python). En sus palabras:

> _If you don’t have an enterprise, and are just writing a single application, then these
> entities are the business objects of the application. They encapsulate the most
> general and high-level rules._

En el caso de _ML_, pienso que se identificarían con conceptos fundamentales como
_Tensor_, _Espacio de Hiperparámetros_ o _Modelo_. De hecho, si tenemos una entidad
_Modelo_ podríamos hacer que nuestro código fuese independiente de la librería
(e.g. scikit-learn o TensorFlow) sin problemas, por lo que parece acertado. Aunque sea
un poco "verboso", lo ideal es mantener la disciplina de no implementar lógica en las
entidades puesto que la siguiente capa es la que contendrá eso.

##### Casos de uso
El siguiente círculo (_Use Cases_), tendría los casos de uso específicos al negocio o
aplicación. Probablemente se corresponde con las "especificaciones de cliente", es
decir, lo que se pretende que haga la aplicación de cara al usuario.

> _These use cases orchestrate the flow of data to and from the entities, and direct
> those entities to use their enterprise wide business rules to achieve the goals of the
> use case._

En una app de _ML_ podríamos estar hablando de hacer un caso de uso que sea
_entrenamiento_ y otro que sea _inferencia_, por ejemplo. Entiendo que estos casos de
uso implementarían la lógica de, por ejemplo, cómo entrenar un modelo (sin entrar a si
la librería es una u otra, aunque ahora mismo no veo cómo deshacerse de ello).

##### Adaptadores de interfaces
Como tercera capa, los _Interface Adapters_ serían el código que une las
partes internas y las externas de la aplicación. Esta capa contiene lógica de
transformación de formatos y estructuras de datos entre unas y otras. Según Martin:

> _It is this layer, for example, that will wholly contain the MVC architecture of a
> GUI. The Presenters, Views, and Controllers all belong in here. The models are likely
> just data structures that are passed from the controllers to the use cases, and then
> back from the use cases to the presenters and views._

Otro ejemplo sería convertir de SQL a nuestras entidades o viceversa (aunque a día de
hoy eso puede delegarse en frameworks externos fácilmente). O también, cómo transformar
un modelo de TensorFlow a nuestra "representación interna" para que sea usable por los
casos de uso definidos.

##### Frameworks y Drivers
La última capa de la arquitectura se compone principalmente de las librerías externas y
quizás algo de código pegamento para que los adaptadores puedan trabajar, en caso de ser
necesario.

## La regla de dependencia y los principios _SOLID_

Sea como sea y se hagan los cambios sobre esa estructura "referencia" que se hagan, la
regla principal de la arquitectura es:

> _Ningún nombre en una capa externa puede aparecer en una capa interna._

También se conoce como el [Principio de Inversión de
Dependencia](http://en.wikipedia.org/wiki/Dependency_inversion_principle), en el que se
explica que las interfaces deben actuar como punto de contacto entre las distintas capas[^2].

Los datos que crucen la frontera entre 2 capas deben ser transformados al formato de la
capa más interna (especialmente en el flujo de información de lo externo a lo interno).

De hecho la arquitectura se basa mucho en los principios SOLID:

- _**S**ingle-responsibility_, 
- _**O**pen-closed_, 
- _**L**iskov substitution_, 
- _**I**nterface segregation_ y
- _**D**ependency inversion_.

No obstante, no es objeto de estos apuntes extenderse en esto. El libro
[@martin2017clean] versa principalmente sobre cómo la arquitectura emerge de estos
principios y los describe en profundidad.

[^2]: Este concepto es probablemente el más costoso de comprender ahora mismo.

## Otros conceptos

Cabe incidir en algunos conceptos que aparecen dentro de las capas pero no son
explicados en _Clean Architecture_ (porque no son parte de la arquitectura _per se_),
sin embargo algunos pueden encontrarse en el _Domain-Driven Design_[^3] (ver
[@fig:ddd_concepts]).

![Diagrama con constructos del _DDD_](media/1hRO2rc9ybLM8WDYK4prwJA.png){ width=80% #fig:ddd_concepts }

[^3]: Creo que un buen artículo de blog al respecto de DDD y CA es [@stemmler2019].

##### Repositorios
Este constructo se refiere a clases o interfaces que acceden a o persisten datos.

##### Servicios
En _Clean Architecture_ no se hace mencion a los servicios, mientras que en _DDD_
existen los _Application Services_ y los _Domain Services_. En _CA_, es posible un
paralelismo entre los _Use Cases_ y los _Application Services_, mientras que no existe
el _Domain Service_.

##### Presentadores

##### Controladores


# Plantilla `PythonBase`

Disponible en [el siguiente enlace](https://github.com/diegoreico/PythonBase).

Pasemos a ver su estructura general:

\input{notes/includes/tree_general.tex}

A este nivel, ...

\input{notes/includes/tree_module_detail.tex}

# Ejemplo de aplicación concreta (proyecto PYCTO)

Tras una exploración inicial de los datos, se produjo un notebook con diversos pipelines
para obtener datos de una tabla previamente construida y procesarlos.

Para transformarlo a esta arquitectura, se tendrán un módulo (`analytics`) para las
pipelines de datos con un segundo módulo (`data_wrangling`) que se encargue
exclusivamente de crear las tablas `student_exercises_master_table` y
`first_last_performance`.

## Módulo analytics

#### Casos de uso

El cliente pide las siguientes funcionalidades:

- Obtener porcentaje de alumos que mejoran en alguna habilidad.
- Obtener alumnos tipo A y tipo B (mejoran en todas las habilidades / mejoran en ninguna
  habilidad).
- Obtener frecuencia de realización de las actividades.

#### Infraestructura

En `infrastructure` tendría que ir una adaptación de código de `common` para acceder al
repositorio de datos y extraer los datos para los casos de uso.  En `common` tendrá que
ir el acceso a una BBDD postgres o mysql.

#### Dominio

Los servicios encapsulan la lógica:

- pipeline first_last_performance
- pipeline A/B
- pipeline alumnos que mejoran
- pipeline frecuencia de realización.

Las entidades son clases que modelan el dominio. En este caso:

- SQLResult contiene una dataframe que es el punto de partida para las pipelines de los
  servicios.
- Resumen crosstab
- Resumen general (porcentajes)
- Gráficas (opcional)

#### Controlador

TODO

## Módulo Data Wrangling

TODO

# Referencias

::: {#refs}
:::
