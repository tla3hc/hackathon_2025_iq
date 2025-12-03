# Hackathon 2025 - Executive English Summary

## Overview
The Hackathon 2025 competition involves 4 to 6 teams competing on the same shared map. Each team must develop an intelligent algorithm that controls an autonomous delivery vehicle. The objective is to pick up and deliver virtual packages located across the map and maximize profit:

**Profit = Total Delivery Points – Movement/Energy Cost**

The competition emphasizes strategic decision-making rather than speed or brute-force computation.

---

## Infrastructure and Setup
The organizers provide a centralized playground server. Teams connect their laptops (“player machines”) to this server through a RESTful API.

The server supplies:
- The map layout
- Vehicle’s real-time position and orientation
- The location of package pickup and drop-off points
- The current state of the environment

Teams work only on their algorithm logic; they do **not** modify the server.

---

## Elimination Round (Simulation Phase)
Before the round starts, participants receive:
- A detailed challenge description (Excel format)
- A simulated localization server
- Sample source code containing:
  - API functions for sending and receiving data
  - A basic pathfinding logic (not optimized)

Each virtual package has a point value. A vehicle may carry up to **three packages** at once. After all packages have been delivered, the team with the highest profit advances to the final.

### Key rules:
- Time is **not** a scoring factor.
- Profit is the only metric, based on efficiency and route planning.
- Choosing which packages to pick and in what order is a critical strategy.

---

## Final Round (Real-World Competition)
The final round takes place on a **3m x 3m physical miniature city**. Each team controls a real robot car.

### Important constraints:
- The car does **not** have onboard sensors.
- A camera-based indoor positioning system tracks the vehicle and sends back:
  - Position (millimeter-level accuracy)
  - Orientation (angle in degrees)
  - Virtual radar data for nearby obstacles

Teams must:
1. Use their elimination-round algorithm for route planning
2. Add real-time collision avoidance
3. Send movement commands to the real car using the provided API

### Additional challenge:
- Package pickup points remain constant
- **Drop-off points are randomized** every time the server restarts
- Teams must react dynamically rather than rely on precomputed routes

---

## Winning Criteria
Teams are ranked based on:

1. **Number of delivered packages**
2. If tied → **Shortest total travel distance**

Execution time does not affect ranking. Speed of the vehicle or algorithm runtime is irrelevant; efficiency and correctness are what matter.

---

## Technical Requirements
- Programming language: **Python**
- Teams are given:
  - An emulation server
  - A bot for practice and testing
  - Required libraries and documentation
- Only player-side logic may be modified; server-side code is off-limits

---

## Skills Required for Success
To win, teams must demonstrate:

✔ Sophisticated route optimization (A*, Dijkstra, or improved heuristics)  
✔ Intelligent package selection and delivery order planning  
✔ Real-time reaction capability in the physical round  
✔ Stable and efficient API-driven control logic  

---

## Core Takeaway
This is not a racing competition.  
It is a **strategic logistics optimization challenge**.

Success belongs to the team that can:

- ***Choose the right packages***
- ***Plan efficient delivery sequences***
- ***Adapt dynamically to changing conditions***
- ***Minimize travel cost***

Rather than brute-force coding, **smart decisions and optimized routing** determine the winning team.

---

**Good luck — and deliver smart, not fast!**
