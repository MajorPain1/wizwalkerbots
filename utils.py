import asyncio
from wizwalker.client import *
from wizwalker.constants import Keycode

potion_ui_buy = [
    "fillallpotions",
    "buyAction",
    "btnShopPotions",
    "centerButton",
    "fillonepotion",
    "buyAction",
    "exit"
]

async def safe_click_window_with_name(client, button):
    try:
        await client.mouse_handler.click_window_with_name(button)
    except ValueError:
        await safe_click_window_with_name(client, button)

async def logout_and_in(client):
    print(f'[{client.title}] Logging out and in')
    await asyncio.sleep(0.6)
    await client.send_key(Keycode.ESC, 0.1)
    await asyncio.sleep(0.4)
    await safe_click_window_with_name(client, 'QuitButton')
    await asyncio.sleep(0.4)
    try:
        await client.mouse_handler.click_window_with_name('centerButton')
    except ValueError:
        await asyncio.sleep(0.01)
    await safe_click_window_with_name(client, 'btnPlay')
    await client.wait_for_zone_change()

async def go_through_dialog(client):
    print(f'[{client.title}] Going through dialogue')
    while not await client.is_in_dialog():
        await asyncio.sleep(0.1)
    while await client.is_in_dialog():
        await client.send_key(Keycode.SPACEBAR, 0.1)

async def auto_buy_potions(client):
    # Head to home world gate
    await asyncio.sleep(0.1)
    await client.send_key(Keycode.HOME, 0.1)
    await client.wait_for_zone_change()
    while not await client.is_in_npc_range():
        await client.send_key(Keycode.S, 0.1)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(1.4)
    # Go to Wizard City
    await safe_click_window_with_name(client, 'wbtnWizardCity')
    await asyncio.sleep(0.15)
    await safe_click_window_with_name(client, 'teleportButton')
    await client.wait_for_zone_change()
    # Walk to potion vendor
    await client.goto(-0.5264079570770264, -3021.25244140625)
    await client.send_key(Keycode.W, 0.5)
    await client.wait_for_zone_change()
    await client.goto(11.836355209350586, -1816.455078125)
    await client.send_key(Keycode.W, 0.5)
    await client.wait_for_zone_change()
    await client.goto(-880.2447509765625, 747.2051391601562)
    await client.goto(-4272.06884765625, 1251.950927734375)
    await asyncio.sleep(0.3)
    if not await client.is_in_npc_range():
        await client.teleport(-4442.06005859375, 1001.5532836914062)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(0.2)
    # Buy potions
    for i in potion_ui_buy:
        await safe_click_window_with_name(client, i)
        await asyncio.sleep(0.1)
    # Return
    await client.send_key(Keycode.PAGE_UP, 0.1)
    await client.wait_for_zone_change()
    await client.send_key(Keycode.PAGE_DOWN, 0.1)

async def safe_tp_to_mana(client):
  try:
    await client.tp_to_closest_mana_wisp()
  except MemoryReadError:
    await safe_tp_to_mana(client)
    
async def safe_tp_to_health(client):
  try:
    await client.tp_to_closest_health_wisp()
  except MemoryReadError:
    await safe_tp_to_health(client) 

async def collect_wisps(client):
    # Head to home world gate
    await client.send_key(Keycode.HOME, 0.1)
    await client.wait_for_zone_change()
    while not await client.is_in_npc_range():
        await client.send_key(Keycode.S, 0.1)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(0.5)
    # Go to Mirage
    for i in range(3):
        await safe_click_window_with_name(client, 'rightButton')
    await asyncio.sleep(0.1)
    await safe_click_window_with_name(client, 'wbtnMirage')
    await asyncio.sleep(0.1)
    await safe_click_window_with_name(client, 'teleportButton')
    await client.wait_for_zone_change()
    # Collecting wisps
    while (await client.stats.current_hitpoints() < await client.stats.max_hitpoints()) and await client.get_health_wisps():
        await safe_tp_to_health(client)
        await asyncio.sleep(0.4)
    while (await client.stats.current_mana() < await client.stats.max_mana()) and await client.get_mana_wisps():
        await safe_tp_to_mana(client)
        await asyncio.sleep(0.4)
    # Return
    await client.send_key(Keycode.PAGE_UP, 0.2)
    await client.wait_for_zone_change()
    await client.send_key(Keycode.PAGE_DOWN, 0.2)

async def low_collect_wisps(client):
    # Head to home world gate
    await client.send_key(Keycode.HOME, 0.1)
    await client.wait_for_zone_change()
    while not await client.is_in_npc_range():
        await client.send_key(Keycode.S, 0.1)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(0.5)
    # Go to Dragonspyre
    await safe_click_window_with_name(client, 'rightButton')
    await asyncio.sleep(0.1)
    await safe_click_window_with_name(client, 'wbtnDragonspyre')
    await asyncio.sleep(0.1)
    await safe_click_window_with_name(client, 'teleportButton')
    await client.wait_for_zone_change()
    # Recover
    while await client.stats.current_hitpoints() < await client.stats.max_hitpoints() and await client.get_health_wisps():
        await safe_tp_to_health(client)
        await asyncio.sleep(0.4)
    while await client.stats.current_mana() < await client.stats.max_mana() and await client.get_mana_wisps():
        await safe_tp_to_mana(client)
        await asyncio.sleep(0.4)
    # Return
    await client.send_key(Keycode.PAGE_UP, 0.1)
    await client.wait_for_zone_change()
    await client.send_key(Keycode.PAGE_DOWN, 0.2)

async def decide_heal(client):
    if await client.needs_potion(health_percent=20, mana_percent=5):
        print(f'[{client.title}] Health is at {round((await client.calc_health_ratio()* 100), 2)}% and mana is at {round((await client.calc_mana_ratio() * 100), 2)}%. Need to recover.')
        if await client.stats.current_gold() >= 25000 and await client.stats.reference_level() >= 5: 
            print(f"[{client.title}] Enough gold, buying potions")
            await auto_buy_potions(client)
        elif await client.stats.reference_level() >= 110:
            print(f"[{client.title}] Low gold, collecting wisps")
            await collect_wisps(client)
        elif await client.stats.reference_level() >= 40:
            print(f"[{client.title}] Collecting wisps")
            await low_collect_wisps(client)

