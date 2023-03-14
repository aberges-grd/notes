---
title: _Iterative_ Tools for Data Scientists & Analysts
subtitle: MLOps with tools DVC & CML
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

In this lesson we start with the branch 
