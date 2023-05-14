---
title: Optimization in Machine Learning
abstract: |
  A take on the role of optimization in Machine Learning. We will be exploring both parameter 
  estimation (_training_) and hyperparameter tuning, plus some other topics.
  
  The document aims to be a brief introduction to both fundamental aspects of model training 
  in machine learning and hyperparameter tuning, as well as a compendium of libraries for the 
  later.
---

# Introduction



# Model Training

## Direct solvers

## Iterative methods

### Gauss-Seidel

### Gradient Descent

### Other

### What to do when Gradient Descent fails

As we already saw, GD can fail to find an optimumeven for the case of a smooth, convex
function where it is suppossed to be guaranteed to converge, simply because of an
ill-choice of the learning rate (which is extremely hard to happen, but still).

In a space with a billion dimensions, one cannot expect the optimization landscape to be
well-behaved, in fact, the occurence of saddle points (in some direction) is almost
guaranteed, additionally there could be many local minima and gratly-varying regions
reminiscent of chaos.

There's also the issue of having millions, billions or even trillions of data points
with which train the model on, which could render the algorithm inviable even with its
memory-efficiency.

This is why pure GD is never used in practice. The reality of model training has led to
a increasingly rich collection of techniques that add to the concept of gradient
descent, making it usable for these difficult problems. Some of these techniques skim in
the field of hyperparameter optimization, such as adaptative optimizers or the use of
schedulers to modify one of the hyperparameters on the fly (usually the learning
rate). Others add new features, steps or computations to the original algorithm in an
attempt to alleviate its shorcomings.

We will focus in two of them, because they are the most fundamental of currently
available gradient based optimizers, gaining the status of "classics": Mini Batch
Gradient Descent and Stochastic Gradient Descent.

# Hyperparameter Optimization

There is the case where one needs to optimize a function that takes a sizable amount of
resources to compute, but depends not on millions/billions of parameters but on a few
dozens, or hundreds perhaps. It could also be the case that the function of interest
mixes real-valued and discrete parameters. Finally, the function might be a complete
black box.

In such cases, gradient based methods (and especially GD) might not be the best choice,
or even a viable choice at all. One must turn to algorithms that take as few evaluations
of the function as possible, while also giving good guarantees of optima-finding. In the
ideal case, support for all types of parameters is desired.

The case of tuning hyperparameters of a ML model is one of these instances. Even in the
case where one is interested in optimizing with respect to more exotic stuff such as
optimizer used, number of layers and/or neurons per layer, structure of the neural
network or the model morphology itself (e.g. try random forest vs neural network), the
number of parameters is never going to be in the same order of magnitude as even the
smallest of neural networks; the parameters are not always real numbers (sometimes not
even integers, such as when the optimizer itself is a parameter), 

## The basics

### Manual search

Perhaps the most popular even today. This simply has a Data Scientist or Machine
Learning practicioner use their experience and domain knowledge to propose some good
parameters that have worked well in the past, then modify them and run a new experiment
with the insights gained from analyzing the model just trained.

A very popular ML library, MLFlow, was created with the sole purpose of making manual
search a more reliable technique: back in the day, scientists and engineers usually
tracked their parameter combinations in an Excel file.

In some cases, when one is not willing to commit the amount of resources automated
hyperparameter tuning requires (including engineering resources, i.e. writing the code
with this kind of automations in mind), it's still the way to go.

Hopefully the reader will break with this old practice once they are done reading the
document!

### Grid Search

In terms of guarantees of optimality and flexibility of parameter tipologies (save for
the need of discretizing real-valued parameters) this is perhaps the best method, at
least in principle: simply evaluate every possible combination of parameters and take
the best one.

This method was popular back when only 2 or 3 hyperparameters were of interest and not
many choices for each one of them were considered. It amounted to a more automated
manual search, it's also very easy to implement for anyone.

Sadly, this method is incredibly inefficient and suffers from a combinatorial scaling in
the number of hyperparameters that is going to be almost exponential. Essentially, with
N hyperparameters and e.g. 2 choices for each of them, one is going to do 2^N
evaluations of the function (training the model and checking its performance).

For this reason, it's never advised to use this algorithm for HPO; not even in the case
where one has very few parameters. The reason is that it's almost inevitable to end up
wanting to tune more hyperparameters. Implementing Grid Search early is a trap in which
you'll find yourself trapped then.

It is better to just use some other algorithm such as Bayesian methods from the get-go,
and force yourself to code in a more modular way so you can switch the algorithm for
other in the future as your need for more sophistication grows.

### Random Search

Random Search is equally easy to implement but offers the promise of slightly better
efficiency in the search (i.e. potentially exploring much more of the search space with
fewer evaluations), although offers absolutely zero guarantees of finding the
optimum. It can also be O(1) in the number of parameters: just fix a number of
evaluations and choose the best.

As its name suggests, you just draw the hyperparameter values at random a number of
times (say, 1000 random combinations of hyperparameters) and evaluate these. Once all
have been evaluated, you choose the best performing one, hoping to have been lucky
enough to be in the proximity of a good optimum.

### Mixed search

Rarely used because there are better algorithms already, this one uses a first round of
Random Search to find a promising zone, then Grid Search in the proximity of the best
evaluated point in hopes to find the true minima.

## Surrogate methods

Surrogate methods try to build a model of the unknown function to be optimized (the
surrogate) from the evaluations performed. They also involve an "acquisition function",
which is used to select where to sample the next point.

### Bayesian optimization

Bayesian optimization uses a Gaussian process as its surrogate function. Gaussian
processes have the advantage to provide uncertainty estimates for the regions far from
the evaluated points, so it can be used as part of the acquisition function sample from
these "unknown" regions (although its' not the only criteria used).

Bayesian Optimization is perhaps the first method to be rightfully called an
"hyperparameter optimization" algorithm, since it at least attempts to minimize the
amount of evaluations and also tries to find the global minima of the function.

Two of the drawbacks of this method are: inability to deal with non-real valued
parameters (but extensions to the algorithm exist) and lack of parallelization (there
are variants of the algorithm allowing for it).

### Tree-Structured Parzen Estimators (TPE)

This algorithm tries to model the function as a collection of Parzen estimators that are
organized as a tree-like structure in the space of parameters. This means that as
hyperparameters are chosen, a new branch of a decision tree is created. At the leaves
there are the estimators (surrogates) of the function.

The aquisition function is in itself the criteria to make the tree grow: it's a ratio
between XXX and YYY.

## Reinforcement Learning methods

### HyperBandit


## Other methods

### Gradient Descent for HPO

### Population Based Training

# Some HPO libraries

# Other topics

## Optimal control

## Multilevel Optimization
