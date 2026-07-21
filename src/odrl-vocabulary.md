# ODRL Vocabulary

## Actuators 

| **Actuators**     | **Nom**        | **Identification**       | **Default** |
|-------------------|----------------|--------------------------|-------------|
| Moteur            | `engine`       | urn:vehicle:engine       | float       |
| Bras de direction | `steering-arm` | urn:vehicle:steering-arm | float       |
| Clignotant gauche | `left-signal`  | urn:vehicle:left-signal  | bool        |
| Clignotant droit  | `right-signal` | urn:vehicle:right-signal | bool        |

## Sensors

| **Sensor**        | **Nom**    | **Identification**   | **Default** |
|-------------------|------------|----------------------|-------------|
| Camera            | `camera`   | urn:sensors:camera   | detections  |
| Distance detector | `distance` | urn:sensors:distance | float       |
| Cliff detector    | `cliff`    | urn:sensors:cliff    | bool        |

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

| **Name**       | **Identification**            | **Description**                      |
|----------------|-------------------------------|--------------------------------------|
| Navigation     | `urn:services:navigation`     | Shortest path determination          |
| Identification | `urn:services:identification` | Computer vision for object detection |
| Decision       | `urn:services:decision`       | Next move decision                   |

## Constraints

| **Name**   | **Identification**          | **Description**                            |
|------------|-----------------------------|--------------------------------------------|
| Latency    | `urn:constraint:latency`    | Minimum latency that can be requested      |
| Encryption | `urn:constraint:encryption` | Need to encrypt message or not             |
------------------------------- (À VOIR MAYBE PLUS TARD) --------------------------------
| Bandwith   | `urn:constraint:bandwith`   | Maximum bandwith amount that can be filled |
| Frequency  | `urn:constraint:frequency`  | Minimum delay between successive calls     |

## Remote computing environment

| **Name** | **Identification** |
|----------|--------------------|
| Cloud    | urn:host:cloud     |
| Edge     | urn:host:edge      |

---

## Actions 
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