# ODRL Vocabulary


## Policies

| **Policies** | **Identification**      | **Description**                                                   |
|:-------------|:------------------------|:------------------------------------------------------------------|
| Request      | `urn:request:service`   | Client asking for remote service access                           |
| Offer        | `urn:offer:service`     | Server offering service hosting                                   |
| Agreement    | `urn:agreement:service` | Acknowledgment between client and server send by the orchestrator |

## Capacities

| **Capacities** | **Identification**   | **Description**    |
|:---------------|:---------------------|:-------------------|
| Capacity 1     | `urn:capacity:cap-1` | Receive video flow |
| Capacity 2     | `urn:capacity:cap-2` | AI recognition     |
| Capacity 3     | `urn:capacity:cap-3` | Data storage       |
| Capacity 4     | `urn:capacity:cap-4` | Route calculation  |
| Capacity 5     | `urn:capacity:cap-5` | Compute behaviour  |
| Capacity 6     | `urn:capacity:cap-6` | Aggregate          |

## Services

| **Services**   | **Identification**           | **Description**                      |
|:---------------|:-----------------------------|:-------------------------------------|
| Navigation     | `urn:service:navigation`     | Shortest path determination          |
| Identification | `urn:service:identification` | Computer vision for object detection |
| Decision       | `urn:service:decision`       | Next move decision                   |

## Metrics

| **Metrics** | **Identification**      | **Description**                        |
|:------------|:------------------------|:---------------------------------------|
| Latency     | `urn:metric:latency`    | Minimum latency that can be requested  |
| Encryption  | `urn:metric:encryption` | Need to encrypt message or not         |
| Frequency   | `urn:metric:frequency`  | Minimum delay between successive calls |
| Flow rate   | `urn:metric:flow-rate`  | Maximum flow rate allowed              |
---- MAYBE PLUS TARD ----
| Bandwith        | `urn:metric:bandwith`   | Maximum bandwith amount that can be filled |

## Entities

| **Entities** | **Identification** |
|:-------------|:-------------------|
| Server       | `urn:node`         |
| Client       | `urn:client`       |

---

## Actuators 

| **Actuators** | **Identification**           | **Default** |
|:--------------|:-----------------------------|:------------|
| Engine        | `urn:vehicle:engine`         | float       |
| Steering arm  | `urn:vehicle:steering-arm`   | float       |
| Left blinker  | `urn:vehicle:left-blinker `  | bool        |
| Right blinker | `urn:vehicle:right-blinker ` | bool        |

## Sensors

| **Sensor**        | **Identification**     | **Default** |
|:------------------|:-----------------------|:------------|
| Camera            | `urn:sensors:camera`   | detections  |
| Distance detector | `urn:sensors:distance` | float       |
| Cliff detector    | `urn:sensors:cliff`    | bool        |

---

## Actions 

| **Actions**                         | **Identification**                                           | **Description**           |
|:------------------------------------|:-------------------------------------------------------------|:--------------------------|
| Increase engine torque              | `urn:action:longitudinal-monitoring:increase-engine-torque`  | Speed up                  |
| Decrease engine torque              | `urn:action:longitudinal-monitoring:decrease-engine-torque`  | Slow down                 |
| Increase brake pressure             | `urn:action:longitudinal-monitoring:increase-brake-pressure` | Brake                     |
| Decrease brake pressure             | `urn:action:longitudinal-monitoring:decrease-engine-torque`  | Stop braking              |
| Nothing                             | `urn:action:longitudinal-monitoring:nothing`                 | Do nothing                |
| Increase steering angle             | `urn:action:lateral-control:increase-steering-angle`         | Turn left/right           |
| Decrease steering angle             | `urn:action:lateral-control:decrease-steering-angle`         | Stop turning              |
| Engage forward                      | `urn:action:transmission:engage-forward`                     | Move forward              |
| Engage backward                     | `urn:action:transmission:engage-backward`                    | Move backward             |
| Shift to neutral                    | `urn:action:transmission:shift-neutral`                      | Shift to neutral          |
| Apply parking brake                 | `urn:action:transmission:enter-parking-mode`                 | Enter parking mode        |
| Turn on left turn signal            | `urn:action:signaling:turn-on-left-signal`                   | Signal a left turn        |
| Turn off left turn signal           | `urn:action:signaling:turn-off-left-signal`                  | Signal end of left turn   |
| Turn on right turn signal           | `urn:action:signaling:turn-on-right-signal`                  | Signal a right turn       |
| Turn off right turn signal          | `urn:action:signaling:turn-off-right-signal`                 | Signal end of right turn  |
| Turn on low beams                   | `urn:action:signaling:turn-on-low-beams`                     | Turn on low beams         |
| Turn off low beams                  | `urn:action:signaling:turn-off-low-beams`                    | Turn off low beams        |
| Turn on high beams                  | `urn:action:signaling:turn-on-high-beams`                    | Turn on high beams        |
| Turn off high beams                 | `urn:action:signaling:turn-off-high-beams`                   | Turn off high beams       |
| Sound the horn                      | `urn:action:signaling:honk`                                  | Honk                      |
| Increase windshield wipers pressure | `urn:action:signaling:increase-windshield-wipers-pressure`   | Put on windshield wipers  |
| Decrease windshield wipers pressure | `urn:action:signaling:decrease-windshield-wipers-pressure`   | Put off windshield wipers |

--- 