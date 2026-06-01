---
title: "Phuket Bus Routing Application"
date: "2024-01-23"
tags: [python, pyqt5, transport, application, algorithms, buses]
summary: "A breakdown of my high school science project - a bus route finding app in Phuket, Thailand using a specialized version of Dijkstra's algorithm."
---

![Image of a Phothong bus in Phuket, Thailand](/static/img/phothong-bus.jpg)
_Image of a Phothong bus in Phuket, Thailand. Source: Phuket One Map_

## Overview

This project was developed to address the inconvenience of traveling on the Phothong bus in Phuket, which is caused by a lack of easily accessible information regarding stops, routes, fares, and schedules. To solve this, me and my friend Pacharakamon Wattanasiri at Mahidol Wittayanusorn School (MWIT) developed a Python-based program that identifies the optimal bus route and calculates the fare for commuters.

This project was an eye-opening experience to create applications as solutions to real-world problems, in the end, I have learned many lessons on how to overcome certain limitations and how to process real-world data which is often times inconsistent. This would be my beginning to pursue studies in Computer Science later on.

## Data Processing

At first, the data was decentralized and inconsistent across different operators and websites. We had to manually search for the data and combine them into a single source of truth for the procedures afterwards.

![Image of a graph consisting of all bus stops in Phuket, drawn on drawio.](/static/img/phothong-map.png)
_Image of a graph consisting of all bus stops in Phuket, drawn on drawio._

## Algorithmic Optimization

The Phothong map in Phuket contains over 125 stops. Running a standard pathfinding algorithm across a graph of this size can be inefficient, so we adapted Dijkstra's algorithm as our core route-finding method, along with a procedure to decrease the size of the graph required for computation to minimize overall runtime.

Our architectural approach involved decoupling the transit network:

- We categorized the network into **"main stops"** and **"sub-stops"**.
- A sub-stop was defined as a bus stop where the bus routes passing by it are identical to those of the connected stops.
- Main stops were defined as points where a Phothong line diverges or terminates.
- The program calculates **the shortest path within the main graph**, which consists of only 34 main stops, significantly reducing the time spent searching the same subgraph.
- The program calculates the shortest route between the starting node and connected main stops, as well as the ending node and its connected main stops separately.
- The `PriorityQueue` library was implemented in the program to find the shortest route in the graph according to Dijkstra's algorithm.

## Line Assignment

After calculating the shortest distance, we also implemented a system to assign bus routes the user needs to take to travel along the finalized route, and constant fare rate calculation. Once the shortest physical path is found, the program determines which buses to board.

- The program creates a list of all bus lines passing through each stop on the route is created.
- It filters these lists to remove lines that don't continue to the next stop, keeping the lines with the cheapest fares.
- If a stop's list becomes empty during filtering, the program identifies that stop as a mandatory "Transfer" point.

## User Interface

To make this program accessible for users, we built a **graphical user interface** prototype using the `PyQt5` module. Users can input their starting point and destination into the application. The program subsequently provides the **shortest route** (using the algoriths mentioned above), along with **fare details and recommended lines** to take.

![Phothong App Screen](/static/img/phothong-app-screen.png)
_Image of the graphical user interface prototype._

## Computational Results

By restructuring the graph topology and limiting the execution of Dijkstra's algorithm only to the main stops, the program saw a massive increase in computational efficiency. The runtimes of the application using our modified algorithm were approximately 25,000x less than the runtime using a standard Dijkstra's algorithm implementation.

## Awards

This project was awarded the "Best Oral Presentation Award" at the STT49 Conference at Prince of Songkhla University, Thailand. Please see the full conference paper [here](https://drive.google.com/file/d/1xII83ddFJk44DrPCMfu0_OaPCiO37_Po/view?usp=sharing).

## Limitations & Future Considerations

This project's main goal is to showcase a modified version of Dijkstra's algorithm by cutting out inefficient bus stops for more efficient calculation. In real-life use cases, there are still clearly some limitations and points to improve in the future.

- The application currently finds the most efficient route by only considering physical distance, completely ignoring real-world constraints like bus schedules, live traffic data, waiting times at transfer points, and the sheer number of transfers a user might have to make. A route that is physically shorter but requires three transfers might take an hour longer than a slightly longer direct route.

- The algorithm connects the source and destination to "their nearest main stops". If a user is at a sub-stop where the nearest main stop is in the opposite direction of their actual destination, the algorithm will mathematically force them to travel backward to that main stop before turning around, resulting in an inefficient real-world itinerary.

- The program relies on statically collected fare data and distances from various existing sources. If the operators of these different bus routes change a route or update ticket prices, the application's underlying dictionaries would have to be manually hard-coded and updated. A great lesson for me to learn from that point onwards is to create apps that are scalable and can adapt to changes.

## Links

- [STT49 Conference Paper](https://drive.google.com/file/d/1xII83ddFJk44DrPCMfu0_OaPCiO37_Po/view?usp=sharing)

---
