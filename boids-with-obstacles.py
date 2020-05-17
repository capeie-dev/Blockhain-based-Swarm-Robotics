#!/usr/bin/env python
# coding=utf-8
# Boid implementation in Python using PyGame

from __future__ import division  # required in Python 2.7
# Necessary to import modules with relative path
import sys, os.path as path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from modules.boid import *
from modules.obstacle import *
from web3 import Web3
import json
import random

infra_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(infra_url))
print(web3.isConnected())
hash_store=[]
web3.eth.defaultAccount = web3.eth.accounts[1]

abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"posid","type":"uint256"}],"name":"GetPos","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"add","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"displayAll","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"}]')


bytecode = '608060405234801561001057600080fd5b506101ef806100206000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c80631003e2d2146100465780634c9beb5314610074578063ca530361146100d3575b600080fd5b6100726004803603602081101561005c57600080fd5b8101908080359060200190929190505050610115565b005b61007c610141565b6040518080602001828103825283818151815260200191508051906020019060200280838360005b838110156100bf5780820151818401526020810190506100a4565b505050509050019250505060405180910390f35b6100ff600480360360208110156100e957600080fd5b8101908080359060200190929190505050610199565b6040518082815260200191505060405180910390f35b600081908060018154018082558091505060019003906000526020600020016000909190919091505550565b6060600080548060200260200160405190810160405280929190818152602001828054801561018f57602002820191906000526020600020905b81548152602001906001019080831161017b575b5050505050905090565b60008082815481106101a757fe5b9060005260206000200154905091905056fea2646970667358221220bf7a10cc899b81dbb50a3c5b7e739c987aff51bf975b12ef16f4464403745b0d64736f6c63430006060033'


greeter = web3.eth.contract(abi=abi,bytecode=bytecode)
#initialize the blockchain with a contruct
tx_hash=greeter.constructor().transact() 
tx_recipt = web3.eth.waitForTransactionReceipt(tx_hash)
contract = web3.eth.contract(address=tx_recipt.contractAddress, abi=abi)

# === main ===

# --- init ---

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

# Set the title of the window
pygame.display.set_caption('Boids')

# Setup background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLACK)

# --- objects ---

# lists
boid_list = pygame.sprite.Group()
obstacle_list = pygame.sprite.Group()
# This is a list of every sprite.
all_sprites_list = pygame.sprite.LayeredDirty()

# --- create boids and obstacles at random positions on the screen ---

# Place boids
for i in range(NUM_BOIDS):
    boid = Boid(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                100, 40, 5, 10, 100, 60, MAX_BOID_VELOCITY, "resources/img/output.png")
    # Add the boid to the lists of objects
    id = random.randint(0,1000000000)
    tx_hash=contract.functions.add(id).transact() 
    tx_recipt = web3.eth.waitForTransactionReceipt(tx_hash)
    boid_list.add(boid)
    all_sprites_list.add(boid)
print(contract.functions.displayAll().call())
# Place obstacles
for i in range(NUM_OBSTACLES):
    obstacle = Obstacle(random.randint(0 + BORDER, SCREEN_WIDTH - BORDER),
                        random.randint(0 + BORDER, SCREEN_HEIGHT - BORDER))
    # Add the obstacle to the lists of objects
    obstacle_list.add(obstacle)
    all_sprites_list.add(obstacle)

clock = pygame.time.Clock()
running = True

# Clear old sprites and replace with background
all_sprites_list.clear(screen, background)

# --- mainloop ---

while running:

    # --- events ---

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    text = "Boids Simulation with Obstacles: FPS: {0:.2f}".format(clock.get_fps())
    pygame.display.set_caption(text)

    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]
    mouse_y = pos[1]

    # --- updates ---

    # Scan for boids and obstacles to pay attention to
    for boid in boid_list:
        closeboid = []
        visible_obstacles = []
        avoid = False
        for otherboid in boid_list:
            if otherboid == boid:
                continue
            distance = boid.distance(otherboid, False)
            if distance < boid.field_of_view:
                closeboid.append(otherboid)
        for obstacle in obstacle_list:
            distance = boid.distance(obstacle, True)
            if distance <= boid.field_of_view:
                visible_obstacles.append(obstacle)

        # Apply the rules of the boids
        boid.cohesion(closeboid)
        boid.alignment(closeboid)
        boid.separation(closeboid, 20)
        if len(visible_obstacles) > 0:
            for obstacle in visible_obstacles:
                boid.obstacle_avoidance(obstacle)
        boid.goal(mouse_x, mouse_y)
        boid.update(False)

    # Check for collisions
    # TODO Either make this work or add a genetic algorithm and kill them
    for boid in boid_list:
        collisions = pygame.sprite.spritecollide(boid, obstacle_list, False)
        for obstacle in collisions:
            boid.velocityX += -1 * (obstacle.real_x - boid.rect.x)
            boid.velocityY += -1 * (obstacle.real_y - boid.rect.y)

    # --- draws ---

    # Create list of dirty rects
    rects = all_sprites_list.draw(screen)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.update(rects)
    # Used to manage how fast the screen updates
    clock.tick(60)

# --- the end ---
pygame.quit()
sys.exit()
