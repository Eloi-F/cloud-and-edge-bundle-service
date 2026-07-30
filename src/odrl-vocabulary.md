# ODRL Vocabulary

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

## States
```(à faire:)
| **States**         | **Nom**        | **Identification**                   | **Default**  |
| ------------------ | -------------- | ------------------------------------ | ------------ |
| En défaut          | `default`      |                                      |              |
| Niveau batterie    | `battery`      |                                      |              |
| Météo              | `weather`      |                                      |              |
| Statut warning     | `warning`      |                                      |              |
```
---

## Services

| **Services**   | **Identification**            | **Description**                      |
|:---------------|:------------------------------|:-------------------------------------|
| Navigation     | `urn:services:navigation`     | Shortest path determination          |
| Identification | `urn:services:identification` | Computer vision for object detection |
| Decision       | `urn:services:decision`       | Next move decision                   |

## Constraints

| **Metrics** | **Identification**          | **Description**                        |
|:------------|:----------------------------|:---------------------------------------|
| Latency     | `urn:constraint:latency`    | Minimum latency that can be requested  |
| Encryption  | `urn:constraint:encryption` | Need to encrypt message or not         |
| Frequency   | `urn:constraint:frequency`  | Minimum delay between successive calls |
| Flow rate   | `urn:constraint:flow-rate`  | Maximum flow rate allowed              |
---- MAYBE PLUS TARD ----
| Bandwith        | `urn:constraint:bandwith`   | Maximum bandwith amount that can be filled |

## Remote computing environment

| **Remote computing environment** | **Identification** |
|:---------------------------------|:-------------------|
| Cloud                            | `urn:host:cloud`   |
| Edge                             | `urn:host:edge`    |

---

## Actions 

| **Actions**             | **Identification**                                           | **Description** |
|:------------------------|:-------------------------------------------------------------|:----------------|
| Increase engine torque  | `urn:action:longitudinal-monitoring:increase-engine-torque`  | Speed up        |
| Decrease engine torque  | `urn:action:longitudinal-monitoring:decrease-engine-torque`  | Slow down       |
| Increase brake pressure | `urn:action:longitudinal-monitoring:increase-brake-pressure` | Brake           |
| Decrease brake pressure | `urn:action:longitudinal-monitoring:decrease-engine-torque`  | Stop braking    |
| Nothing                 | `urn:action:longitudinal-monitoring:nothing`                 | Do nothing      |

```(à faire:)
### Contrôle longitudinal

* Augmenter le couple moteur
* Diminuer le couple moteur
* Augmenter la pression des freins
* Diminuer la pression des freins
* Ne rien faire (ne rien changer à l'état actuel)

### Contrôle latéral

* Augmenter l'angle de braquage (droite/gauche)
* Diminuer l'angle de braquage (droite/gauche)

### Transmission

* Engager la marche avant (D)
* Engager la marche arrière (R)
* Passer au point mort (N)
* Engager le mode parking (P)

### Signalisation

* Activer le clignotant gauche
* Désactiver le clignotant gauche
* Activer le clignotant droit
* Désactiver le clignotant droit
* Activer les feux de détresse
* Désactiver les feux de détresse
* Allumer les feux de croisement
* Éteindre les feux de croisement
* Klaxonner

### Divers

* Augmenter d'un niveau l'action des essuies glaces
* Diminuer d'un niveau l'action des essuies glaces
```
--- 