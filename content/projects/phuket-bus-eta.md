---
title: "Phuket Smart Bus ETA API"
date: "2025-12-01"
tags: [python, fastapi, flask, transport, geojson]
summary: "A real-time ETA prediction system for Phuket's SmartBus network, consisting of a FastAPI backend, dynamic ETA calculation, bus fleet dashboard, and accuracy analytics."
image: ""
---

## Overview

This is a full-stack ETA prediction system built during my internship at City Development Solutions, Phuket. This system that I developed calculates the estimated time of arrival (ETA) of the Phuket SmartBus network.

See my full open-source work [here](https://github.com/parinwarishui/bus-eta-prediction).

## Architecture

| Component    | Technology       | Purpose                               |
| ------------ | ---------------- | ------------------------------------- |
| ETA Engine   | FastAPI          | Background worker, prediction logic   |
| Dashboard    | Flask            | Public passenger-facing ETA board     |
| Admin Panel  | Flask            | Route config, status flags, analytics |
| Data Storage | JSON cache + CSV | Fast reads, offline fallback          |

## The Dynamic ETA Prediction Engine

Calculating reliable bus arrival times in a city like Phuket is challenging because standard fixed bus schedules simply fail under real-world traffic variations.

My main duty while doing my internship was to develop a system that can calculate bus ETAs more accurately by using both historical and live data.

### Weighted Calculation

The data of the bus routes were divided into explicit **one-kilometer geographic segments**. For every single segment, the database maintains a historical average velocity of the buses on each specific one-kilometer segment of the route. This will be used for the calculation of the bus ETA.

When a bus updates its coordinates, the algorithm captures its **current live speed** and pairs it with the **historical segment speed** on that segment of the route. By having these speed and distance data, we can calculate the expected ETA of that bus. For the bus's current kilometer block, the algorithm finds a weighted average of the active live speed with the historical segment speed.

### How ETA is calculated - in steps

1. A background thread polls the SmartBus API every **60 seconds**
2. Live vehicle position is snapped to the nearest point on the GeoJSON route geometry
3. Remaining distance is split into **1km segments** beforehand and the bus is mapped to a certain segment.
4. Each segment has a travel time estimate using **historical average speed** for that km interval.
5. Travel times through each segment from where the bus is to a bus stop are summed → predicted arrival time

### Accuracy Validation Loop

To mathematically prove the validity of the predictive framework, an independent validation thread runs on a continuous loop.

When a vehicle is first tracked on a route, the monitor archives snapshot ETA predictions across explicit time-to-arrival windows (ranging from 120 minutes down to the moment of check-in, as T0, T15, T30, and so on). Once the vehicle physically arrives at a stop, the actual arrival time is written to the analytical process to compute ETA prediction variances.

## Dual-Side Dashboard

The front-facing application is segmented into two isolated interfaces tailored to specific users.

### Public User Side

The user-facing dashboard displays live ETA for upcoming buses. To guarantee quick API response times for heavy concurrent traffic, the frontend is completely decoupled from the data-processing pipeline. It queries a JSON cache layer asynchronously populated by the background worker, ensuring the client layer does not bottleneck the server resources.

![Bus ETA Display](/static/img/bus_eta.png)
_The Bus ETA display._

### Administrative Side

The administrative side functions as an operations control dashboard:

- **Automated Spatial Data Parsing:** Administrators can add new transit routes to the system simply by uploading raw spatial datasets in GeoJSON format. The backend applies custom sorting algorithms based on spherical distance geometry, automatically ordering nodes sequentially to build the path of the new route.
- **System State Controls:** Operators can manually add system override flags to flag specific stops or routes as temporarily closed, or certain bus vehicles as not in service.
- **Accuracy Graph Display:** The dashboard shows a graph of the ETA prediction API accuracy plotting the actual time it takes for the bus to arrive at a stop, against the predicted ETA.

![Bus Routes Configure Screen](/static/img/bus_routes.png)
_Bus Routes Configure Screen._

![Bus ETA Prediction Accuracy Graph](/static/img/bus_accuracy.png)
_Bus ETA Prediction Accuracy Graph._

## Links

- [GitHub Repository](https://github.com/parinwarishui/bus-eta-prediction)
