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

Because the stages were defined with a CLI in them, we can easily add steps to DVC like
so:

```bash
dvc run -n data_load python -m src.stages.data_load --config=params.yaml
```

> Note the `python -m` usage. This is far better than running `python path/to/script`
> because it lets you run code without having to `pip install -e .` first.

Having run this, a `dvc.yaml` file has been created. It has a register of the necessary
information for running your pipelines.

> You can also use `dvc add`.

For example, after using this command:

```bash
dvc run -n data_load \
        --deps src/stages/data_load.py \
        --outs data/raw/iris.csv \
        --params data_load \
        python -m src.stages.data_load --config=params.yaml
```

the file `dvc.yaml` will look like:

```yaml
stages:
  data_load:
    cmd: python -m src.stages.data_load --config=params.yaml
    deps:
    - src/stages/data_load.py
    params:
    - data_load
    outs:
    - data/raw/iris.csv
```

This informs DVC that the stage `data_load` has some dependences in code, parameters and
data (as an output in this case).

This file can of course be edited manually. The point of this file is to track changes
and interdependences (and version control them) and to be explicit/declarative about it.

After we add every stage, `dvc repro` will run everything if there have been changes:
for example any of the deps, or parameters, or having new stages.

The complete `dvc.yaml` file is:

```yaml
stages:
  data_load:
    cmd: python -m src.stages.data_load --config=params.yaml
    deps:
    - src/stages/data_load.py
    params:
    - base
    - data_load
    outs:
    - data/raw/iris.csv
  featurize:
    cmd: python -m src.stages.featurize --config=params.yaml
    deps:
    - data/raw/iris.csv
    - src/stages/featurize.py
    params:
    - base
    - featurize
    outs:
    - data/processed/featured_iris.csv
  data_split:
    cmd: python -m src.stages.data_split --config=params.yaml
    deps:
    - data/processed/featured_iris.csv
    - src/stages/data_split.py
    params:
    - base
    - data_split
    - featurize
    outs:
    - data/processed/train_iris.csv
    - data/processed/test_iris.csv
  train:
    cmd: python -m src.stages.train --config=params.yaml
    deps:
    - data/processed/train_iris.csv
    - src/stages/train.py
    params:
    - base
    - train
    outs:
    - models/model.joblib
  evaluate:
    cmd: python -m src.stages.evaluate --config=params.yaml
    deps:
    - data/processed/test_iris.csv
    - src/stages/evaluate.py
    - models/model.joblib
    params:
    - evaluate
    outs:
    - reports/metrics.json
    - reports/confusion_matrix.png
```

[ms-maturity]: <https://learn.microsoft.com/en-us/azure/architecture/example-scenario/mlops/mlops-maturity-model>

# Versioning Data & Models

This lesson deals with using DVC for its original purpose: versioning data.  The classic
commands are `dvc add`, `dvc remote add` (to add remotes) and `dvc pull`, `dvc push` to
download/upload local changes.

This lesson is essentially just DVC's documentation so it's not very interesting to me.

> Note: because DVC focus so much on git worklow and "GitOps", it becomes really
> important to get used to utilizing tags in most commits.

# Visualize metrics & compare experiments with DVC and Studio

Metrics and plots are an integral part of the ML lifacycle. With DVC we can add
metainformation to the `dvc.yaml` file in order to track them.

## Metrics tracking

> check out to branch `step-7-metrics-and-experiments`.

By modifying `dvc.yaml` and adding a `metrics` section, we can unlock DVC tracking of
metrics. Re-run the pipeline (`dvc repro`) and check metrics on the command line using
`dvc metrics show` (or `diff` to compare).

```yaml
evaluate:
[...]
metrics:
- reports/metrics.json:
    cache: false  # disable DVC tracking so it's tracked with git (small file).
```

> Aside: it is becoming clearer to me that ML needs a "configuration language" that
> makes it easier to reason about configurations. The problem of YAML is that it's fully
> unstructured, and "anything goes". Moving forward, we should define Python modules
> that fully and explicitly define the configuration.

##### Experiment tracking.

By changing model parameters in `params.yaml` we can make DVC track experiments and
compare results. Not only that, parameter grids defined with more than 1 parameter will
automatically perform Grid Search over the combinations. As an example, change Logistic
Regression hyperparameter C from 0.001 to 0.1 and use `dvc repro` to execute. If
everything goes as expected, `dvc metrics diff` should show you the old F1 score and
compare it to the newest one.

> Note: for me it didn't work! I'm still at a loss as to why DVC ignored the previous
> metric. I did everything as in the video.

## Plots

> check out to branch `step-8-metrics-and-plots`.

Run `dvc repro`.

One of our steps produces a confusion matrix PNG. But DVC has the capability of using
Vega (or Vega-Lite) to plot directly from a CSV.

If you use `dvc plots show` in the command line, you'll get a path to an HTML file that
DVC generated for you. However, as of now, it will show nothing. Instead, we have to use this command:

```
dvc plots show reports/confusion_matrix_data.csv \
    --template confusion \
    -x predicted \
    -y y_true
```

which will tell DVC to plot from said CSV and use the Vega template passed, and also
name the axes as indicated. In order to save this plotting recipe for future use, we can
run the previous command with `dvc plots modify` instead of `dvc plots show` or directly
modify `dvc.yaml`. The `plots` section of our `evaluate` stage will now look like this:

```yaml
    plots:
    - reports/confusion_matrix_data.csv:
        template: confusion
        x: predicted
        y: y_true
```

If we change hyperparameters like in the previous subsection, we can see the plot diff
as 2 plots in the same HTML. Sadly, as in the previous example, it didn't work for me.

## DVC tools for Deep Learning

When defining a DVC pipeline stage, you can add a checkpoints flag that and enable
dvclive logging in order to have checkpointing during training. This enables for finer
DL training process.

However, you will have to use `dvclive.Live` in your code to log the training
process. Basically, `dvclive` is "just" a logger for DVC to track the evolution of a
model during epochs and to create snapshots if need be (for example large models whose
training could fail midway due to them taking too long -- think about an externally
managed supercomputer where you need to allocate X hours of computing time and if you
get past that allocated time +5 min your job gets terminated; much like the CESGA).

I won't delve further into it.

## Studio

Finally, Iterative Studio lets you have an integrated development environment (IDE) with
the previous tools, on the web. I haven't used it because it asks to "act on my behalf"
GitHub permissions, and I didn't like it (through it's almost surely all legit).

In the end, it's just a front end for a (managed & cloud-hosted) toolset like we have
already seen.

# Experiments management and collaboration

Next up is learning about the `dvc exp` set of commands. DVC experiments can be set from
pipelines and run in new branches. Also, it lets you to set parameters from the command
line (with the `-S` argument).

> I don't think this plays too well with Auto ML. Also, how to really integrate this
> with Hydra?

# Review and Advanced Topics and Use Cases

Create a data registry and use CML to set up cloud experimentation. Note: this lesson
uses another repo, [linked here][lesson7repo].

Go into the `.github/workflows/cml.yaml` file and look at the GitHub workflow for CML.
This workflow triggers on push and runs a (pretrained) model on data, generating a
report that goes into the pull request comments (for example, the metrics of said
experiment).

Honestly, the lesson doesn't go much further on CML than that (the rest of the lesson is
for iterative tools).

[lesson7repo]: <https://github.com/iterative/course-checkpoints-project>
