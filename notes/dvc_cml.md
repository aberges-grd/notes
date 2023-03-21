---
title: _Iterative_ Tools for Data Scientists & Analysts
subtitle: MLOps with tools DVC & CML
header-includes: |
    \usepackage{dirtree}
abstract: |
  Undertook a course by Iterative (authors of DVC + other tools such as CML), since I found it 
  interesting to learn more about these tools and the company's approach to MLOps. Also, it's free!
  
  The structure of the document is\: each section is a lesson (totalling 7), inside the section
  there are notes and code snippets for each lesson.
---

# Introduction

The introduction goes on about statubg 5 phases of a _typical_ ML development workflow:

* Data management and analysis,
* Experimentation,
* Solution development and testing,
* Deployment and serving,
* Monitoring and maintenance.

The course will focus on data management, pipelines and experiments (primarily contained
in the first 2 points mentioned).

To better understand their take, I've snatched a graphic from the course's notes
([@fig:ml_workflow_diagram]). The blue dashed box in [@fig:ml_workflow_diagram] marks
the scope of the course, i.e. what's referenced in the first 2 points of the list.

![ML Project workflow diagram](media/06e09a75585dd540ca5f10eb58ce7291.png "ML Workflow Diagram"){ width=90% #fig:ml_workflow_diagram }

Worth of noting is that the course has a repository at
[github](https://github.com/iterative/course-ds-base). The repo structure is:

- Two branches per "exercise" (not lesson)
- one branch is the initial state for the exercise, another (with suffix 'SOLVED') holds
  the solution.

# Practices and Tools for Efficient Collaboration in ML projects

This lesson is basically about basic use of `git` and Python virtual environments.

# Pipelines Automation and Configuration

The lesson starts talking about the classic workflow we all know: working in a (jupyter)
notebook. As projects grow, this approach becomes clumsy because it is hard to reproduce
and automate (well, there are tools like `papermill` etc.) So the next step is to
transform these notebooks into code.

They point to maturity models such as [Microsoft's][ms-maturity] in order to argue for
the need of "pipelinization" of notebooks and ML workflow in general, so that we can
execute it with one command. It should be reliable and reproducible, requiring minimal
human interaction.

Instead of executing each stage of a pipeline individually, we want to run the pipeline
as a whole, especially when running experiments with different parameter settings. An
automated pipeline should notice where runs diverge and only rerun necessary stages.

Benefits of codified pipelines include efficiency, collaboration, and scalability.
Moreover, reproducibility is crucial for ML projects. We want experiments to produce the
same outcomes regardless of when or where we run them.

It is also very important to track and properly manage the configuration and data in
machine learning projects to achieve reproducibility of experiments.

## First steps towards automation

For the practice, we start with the branch `step-1-organize-ml-project`, in which they
extract `LogisticRegression` parameters to a dictionary, also save the feature
engineered train and test data to a folder, and use a random seed to make it fully
reproducible. Plus, they dump the metrics to a JSON and the confusion matrix to a PNG
file.

Next is the branch `step-2-create-config-file` extracts most of the configuration to a
YAML file, including random state, model hyperparameters, paths for datasets, and also
the location of metrics and confusion matrix.

For the branch `step-3-reusable-code` simply extracts the visualization function (the
one that plots the confusion matrix) to a Python file.

## Modularization of code & DVC

The next step is to build an experiment pipeline in branch `step-4-build-ml-pipeline`.
They explain the steps they need (`data_load`, `featurize`, `data_split`, `evaluate` and
`train`). They create four modules under the `src/` folder: `report`, `stages`, `train`,
`utils`, stages hosts the most code (see [@fig:dirtree-4]).

\begin{figure}
\dirtree{%
.1 src.
.2 utils.
.3 logs.py.
.2 stages.
.3 data\_load.py\DTcomment{load the data from our data sources{.}}.
.3 train.py\DTcomment{defiles a wrapper that loads training data and uses train function{.}}.
.3 evaluate.py\DTcomment{evaluate the model on the test data{.}}.
.3 data\_split.py\DTcomment{create a train/test split{.}}.
.3 featurize.py\DTcomment{create features from raw data{.}}.
.2 report.
.3 visualize.py.
.2 train.
.3 train.py\DTcomment{actually implements training code{.}}.
}
\caption{\label{fig:dirtree-4} Directory tree of source code.}
\end{figure}

They opt for giving each stage file a function with the functionality and a `__main__`
block so that you can import the code in a notebook or run each step in the command
line.

In the branch `step-5-automate-ml-pipeline`, we go for DVC to automate the pipeline!
Initially, just install DVC and use it on the command line like so:

```bash
conda install -c conda-forge dvc # or pip
dvc init
git add . # or list the files that the previous command outputs
git commit -m "Initialized DVC"
```

[ms-maturity]: <https://learn.microsoft.com/en-us/azure/architecture/example-scenario/mlops/mlops-maturity-model>
