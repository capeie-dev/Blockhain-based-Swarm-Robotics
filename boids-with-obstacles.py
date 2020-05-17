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
web3.eth.defaultAccount = web3.eth.accounts[2]

abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"GetUserInfo","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"Name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"passedName","type":"string"}],"name":"SetUserInfo","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
bytecode = '608060405234801561001057600080fd5b506040518060400160405280600581526020017f48656c6c6f0000000000000000000000000000000000000000000000000000008152506000908051906020019061005c929190610062565b50610107565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106100a357805160ff19168380011785556100d1565b828001600101855582156100d1579182015b828111156100d05782518255916020019190600101906100b5565b5b5090506100de91906100e2565b5090565b61010491905b808211156101005760008160009055506001016100e8565b5090565b90565b61043c806101166000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c80635119a342146100465780638052474d146100c9578063ef2ceea51461014c575b600080fd5b61004e610207565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561008e578082015181840152602081019050610073565b50505050905090810190601f1680156100bb5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6100d16102a9565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156101115780820151818401526020810190506100f6565b50505050905090810190601f16801561013e5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6102056004803603602081101561016257600080fd5b810190808035906020019064010000000081111561017f57600080fd5b82018360208201111561019157600080fd5b803590602001918460018302840111640100000000831117156101b357600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290505050610347565b005b606060008054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561029f5780601f106102745761010080835404028352916020019161029f565b820191906000526020600020905b81548152906001019060200180831161028257829003601f168201915b5050505050905090565b60008054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561033f5780601f106103145761010080835404028352916020019161033f565b820191906000526020600020905b81548152906001019060200180831161032257829003601f168201915b505050505081565b806000908051906020019061035d929190610361565b5050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106103a257805160ff19168380011785556103d0565b828001600101855582156103d0579182015b828111156103cf5782518255916020019190600101906103b4565b5b5090506103dd91906103e1565b5090565b61040391905b808211156103ff5760008160009055506001016103e7565b5090565b9056fea264697066735822122056ec9c7c911b5e661422ec3b06af98b53b2315aa715828afa9c2cfc347f83e6d64736f6c63430006060033'

greeter = web3.eth.contract(abi=abi,bytecode=bytecode)

#initialize the blockchain with a contruct
tx_hash=greeter.constructor().transact() 
tx_recipt = web3.eth.waitForTransactionReceipt(tx_hash)
contract = web3.eth.contract(address=tx_recipt.contractAddress, abi=abi)
print(contract.functions.GetUserInfo().call())

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
                100, 40, 5, 10, 100, 60, MAX_BOID_VELOCITY, "resources/img/boid.png")
    # Add the boid to the lists of objects
    id = str(random.random())
    tx_hash=contract.functions.SetUserInfo(id).transact() 
    tx_recipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(contract.functions.GetUserInfo().call())
    boid_list.add(boid)
    all_sprites_list.add(boid)

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
