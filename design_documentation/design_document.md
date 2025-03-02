# Introduction

## Name

## Description

GAMENAME is a non-traditional roguelike auto battler with the customizability of a collectable card game. Design a team of robots out of procedurally-generated modifications and battle commands. Whether you create a massive battlecruiser mecha or a swarm of exploding nanobots is up to you.

## Tags

`procedurally generated`, `roguelike`, `auto battler`, `deckbuilding`, `roguelike deckbuilder`, `rpg`, `strategy rpg`, `broken build`, `busted build`


## Player Experience

The goal core player experience is of creative expression through designing the player's robots and accomplishment through optimizing the robots' modifications under the chosen strategy to defeat enemies. The game will achieve this by eliminating tedious tactical decisions through automated battles which are driven by elements determined by the player's modifications to their robots.

## Gameplay

--Player and enemy units exist on a procedurally generated hexagonal grid. The player engages enemy units in combat and gets rewards from defeating enemy units in the form of in-game currency and dropped upgrades. The currency is used to level up the player's units in the form of an increased number of slots to apply the acquired upgrades.--


Don't randomize the deck / the whole deck. Since the player isn't playing during combat, there's no need to make each experience feel so different.
- counter spell
- empty resource pool
- shuffle

Don't need to make players choose between items. Since the units have a cap on items they can equip, more items doesn't automatically make the units stronger.

## Game Loop

Units take turns in a set turn order during which their owner decides which actions the unit performs. Actions may include attacking, charging up shields, or delaying the unit's turn in the turn order. The turn order is visible to the player so they can strategize with consideration to what actions will be available to them before enemy units take actions.

In order to prevent strategically changing a unit?s badge configuration between moves, which would be optimally strategic yet extremely tedious and unfun, units can only be edited at the beginning of the unit's turn.


# Battle System

## Basic Unit


| Stat         | Base Value |
|--------------|------------|
| HP           | 0          |
| AP           | 0          |
| Attack       | 0          |
| Accuracy     | 95%        |
| Armor        | 0          |
| Max Shields  | 0          |
| Evasion      | 0%         |


## Combat Styles


## Offense-Defense Table

The three main defense categories are Armor, Shields, and Evasion. Armor passively reduces damage taken from an attack. Shields are one-time-use chargeable states which negate an attack. Evasion reduces the chance that an attack will hit the unit.

The tree main weapon categories are Railgun, Missile, and Laser. The Railgun is a weak, low energy cost weapon, good for making a large number of attacks per turn which can break through Shields but are ineffective at piercing Armor. Missiles are a medium strength, medium energy cost weapon, good for dealing large chunks of damage and getting through Armor but are inaccurate against evasive enemies. The Laser is a strong, high energy cost weapon with very high accuracy, good for hitting highly Evasive enemies but which are wasteful against shields.

Combined, these offensive and defensive abilities create the Offense-Defense Table.

|         | Armor   | Shields | Evasion |
|---------|---------|---------|---------|
| Railgun | weak    | strong  | neutral |
| Missile | strong  | neutral | weak    |
| Laser   | neutral | weak    | strong  |

Note that while each of these weapons and defensive techniques have strengths and weaknesses, no direct bonus or penalty is calculated between the pair. The matchups are emergent to how the techniques work and are left to players to discover. An explicit damage modifier to the offense-defense pairs may become necessary in the future if balancing the pairs proves impossible


## Balancing

With nine offense-defense matchups, it isn’t trivial to balance all these stats such that one isn’t clearly superior to the rest in all cases. All six technologies should be useful against an “average” enemy.


# Resource System



## Scrap

## Gaining Scrap

bonus scrap for meeting objectives

objectives may as well be constant since player can't change behavior

- fast clear
- all allies alive
- high max damage
- high total damage
- lots of actions in a turn

## Unit Modifications

## Buying and Selling Modifications

duplicate owned modification

sell owned modification

duplicate unit

# Upgrade System


## Encouraging Strategic Diversity

As a roguelike, a key goal for the enjoyability of the game is replayability. To make replays enjoyable, it is necessary to make the player have multiple and diverse play styles they aspire to try out. Two separate challenges arise from this goal. The first is to make there be diverse play styles worth trying out, and the second is making the player aware of those possibilities. 

~~It is not trivial to make wide teams as good as tall teams, as wide teams get more AP per turn.~~


- Don’t punish experimentation.
- Low punishment for failure.
- Low/no cost to reconfigure units.
- Make threats diverse to require diverse strategies.
- Make diversity fun with unique animations/sounds/achievements/shareable content.

# UI

## Preparation Scene

### Units

### Modifications

### Badges

### Programs

### Current Unit

### Current Modification

## Enemy Unit Stat UI


