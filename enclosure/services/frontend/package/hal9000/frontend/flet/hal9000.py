#!/usr/bin/env python3

import os
import math
import json
import datetime
import fastapi
import flet_core
import flet_core.alignment
import flet_core.border
import flet_core.colors
import flet
import flet.canvas
import flet.fastapi

import asyncio

from hal9000.frontend import Frontend

class HAL9000(Frontend):

	def __init__(self, app: fastapi.FastAPI):
		super().__init__()
		self.flet_app = app
		self.command_listener_task = None
		self.session_queues = {}


	async def configure(self, filename) -> bool:
		if await super().configure(filename) is False:
			print(f"[frontend:flet] parsing '{filename}' failed")
			return False
		self.flet_app.mount('/', flet.fastapi.app(self.flet, route_url_strategy='path', assets_dir=f'{os.getcwd()}/assets'))
		return True


	async def run_command_listener(self):
		while True:
			command = await self.commands.get()
			if len(self.session_queues) == 0:
				if command['topic'] == 'status':
					self.events.put_nowait({'topic': 'interface/state', 'payload': 'offline'})
			else:
				for session_queue in self.session_queues.values():
					session_queue.put_nowait(command.copy())


	async def run_session_listener(self, session_queue, display):
		while True:
			command = await session_queue.get()
			print(command)
			if command['topic'] == 'application/runtime':
				if 'condition' in command['payload']:
					if command['payload']['condition'] == "asleep":
						self.show_none(display)
					if command['payload']['condition'] == "awake":
						self.show_idle(display)
			if command['topic'] == 'status':
				self.events.put_nowait({'topic': 'interface/state', 'payload': 'online'})
			elif command['topic'] == 'gui/screen':
				for screen in command['payload'].keys():
					if screen == 'idle':
						self.show_idle(display)
					elif screen == 'hal9000':
						self.show_hal9k(display, command['payload']['hal9000'])
					elif screen == 'menu':
						self.show_menu(display, command['payload']['menu'])
					else:
						print(json.dumps(command['payload'])) ##TODO
			elif command['topic'] == 'gui/overlay':
				for overlay in command['payload'].keys():
					display.content.shapes = list(filter(lambda shape: shape.data!='overlay', display.content.shapes))
					if overlay == 'volume':
						radius = display.radius
						for level in range(0, int(command['payload']['volume']['level'])):
							dx = math.cos(2*math.pi * level/100 * 6/8 + (2*math.pi*3/8));
							dy = math.sin(2*math.pi * level/100 * 6/8 + (2*math.pi*3/8));
							display.content.shapes.append(flet.canvas.Line(radius/2+(dx*radius*0.9), radius/2+(dy*radius*0.9),
							                                               radius/2+(dx*radius*0.99), radius/2+(dy*radius*0.99),
							                                               paint=flet.Paint(color='white'), data='overlay'))
						display.content.update()
					elif overlay == 'none':
						display.content.update()
					else:
						self.show_menu(display, json.dumps(command['payload']))


	async def run_gui_screen_idle(self, display):
		while True:
			if display.data['idle_clock'].current is not None:
				now = datetime.datetime.now()
				if now.second % 2 == 0:
					display.data['idle_clock'].current.text = now.strftime('%H:%M')
				else:
					display.data['idle_clock'].current.text = now.strftime('%H %M')
				display.content.update()
			await asyncio.sleep(1)


	async def run_gui_screen_hal9k(self, display):
		while True:
			if len(display.data['hal9k_queue']) > 0:
				sequence = display.data['hal9k_queue'].pop(0)
				if sequence['name'] in ['wakeup', 'active', 'sleep']:
					display.content.shapes = list(filter(lambda shape: shape.data=='overlay', display.content.shapes))
					for nr in range(0,10):
						display.background_image_src = f'/sequences/{sequence["name"]}/0{nr}.jpg'
						display.update()
						await asyncio.sleep(0.2)
				if sequence['name'] == 'sleep':
					display.background_image_src = '/sequences/init/00.jpg'
					display.update()
					self.show_idle(display)
			await asyncio.sleep(0.1)


	def show_none(self, display):
		display.content.shapes = list()
		display.content.update()


	def show_idle(self, display):
		display.content.shapes = list(filter(lambda shape: shape.data=='overlay', display.content.shapes))
		display.content.shapes.append(flet.canvas.Text(ref=display.data['idle_clock'],
		                                               x=int(display.radius/2), y=int(display.radius/2),
		                                               style=flet.TextStyle(color='white'),
		                                               alignment=flet_core.alignment.center))
		display.content.update()


	def show_hal9k(self, display, data):
		display.content.shapes = list(filter(lambda shape: shape.data=='overlay', display.content.shapes))
		if 'queue' in data:
			if data['queue'] == 'replace':
				display.data['hal9k_queue'].clear()
				display.data['hal9k_queue'].append(data['sequence'])
			elif data['queue'] == 'append':
				display.data['hal9k_queue'].append(data['sequence'])


	def show_menu(self, display, data):
		display.content.shapes = list(filter(lambda shape: shape.data=='overlay', display.content.shapes))
		display.content.shapes.append(flet.canvas.Text(text=data['title'],
		                                               x=int(display.radius/2), y=int(display.radius/4*1),
		                                               style=flet.TextStyle(color='white'),
		                                               alignment=flet_core.alignment.center))
		display.content.shapes.append(flet.canvas.Text(text=data['text'],
		                                               x=int(display.radius/2), y=int(display.radius/4*3),
		                                               style=flet.TextStyle(color='white'),
		                                               alignment=flet_core.alignment.center))
		display.content.update()


	def on_control_up(self, event):
		self.events.put_nowait({'topic': 'rotary/control', 'payload': 'rotary:control delta=+1'})

	def on_control_down(self, event):
		self.events.put_nowait({'topic': 'rotary/control', 'payload': 'rotary:control delta=-1'})

	def on_control_select(self, event):
		self.events.put_nowait({'topic': 'button/control', 'payload': 'button:control status=clicked'})

	def on_volume_up(self, event):
		self.events.put_nowait({'topic': 'rotary/volume', 'payload': 'rotary:volume delta=+1'})

	def on_volume_down(self, event):
		self.events.put_nowait({'topic': 'rotary/volume', 'payload': 'rotary:volume delta=-1'})

	def on_volume_mute(self, event):
		self.events.put_nowait({'topic': 'button/volume', 'payload': 'button:volume status=clicked'})


	def flet_on_disconnect(self, event):
		for task in ['session_task', 'gui_idle_task', 'gui_hal9k_task']:
			if event.page.session.contains_key(task):
				event.page.session.get(task).cancel()
				event.page.session.remove(task)
		if event.page.session_id in self.session_queues:
			del self.session_queues[event.page.session_id]
		

	async def flet(self, page: flet.Page):
		page.on_disconnect = self.flet_on_disconnect
		page.title = "HAL9000"
		page.theme_mode = flet.ThemeMode.DARK
		scale = 1.0
		if page.height < 1000:
			scale = page.height / 1000
		display = flet.CircleAvatar(radius=scale*120, bgcolor='black')
		display.content = flet.canvas.Canvas(width=scale*120, height=scale*120)
		display.background_image_src = '/sequences/init/00.jpg'
		display.data = {}
		display.data['idle_clock'] = flet.Ref[flet.canvas.Text()]
		display.data['hal9k_queue'] = []
		page.add(flet.Row(controls=[flet.Column(controls=[
		                                                  flet.TextButton("Ctrl+", on_click=self.on_control_up),
		                                                  flet.TextButton("Select", on_click=self.on_control_select),
		                                                  flet.TextButton("Ctrl-", on_click=self.on_control_down),
		                                                 ]),
		                            flet.Container(width=scale*328, height=scale*960,
		                                           content=flet.Column(controls=[flet.Row(height=scale*425),
		                                                                         flet.Row(controls=[display], alignment=flet.MainAxisAlignment.CENTER)
		                                                                        ]),
		                                           image_src="/HAL9000.jpg", image_fit=flet.ImageFit.FILL),
		                            flet.Column(controls=[
		                                                  flet.TextButton("Vol+", on_click=self.on_volume_up),
		                                                  flet.TextButton("Mute", on_click=self.on_volume_mute),
		                                                  flet.TextButton("Vol-", on_click=self.on_volume_down),
		                                                 ]),
		                           ], alignment=flet.MainAxisAlignment.CENTER))
		page.update()
		if self.command_listener_task is None:
			self.command_listener_task = asyncio.create_task(self.run_command_listener())
		session_queue = asyncio.Queue()
		page.session.set('session_task', asyncio.create_task(self.run_session_listener(session_queue, display)))
		page.session.set('gui_idle_task',asyncio.create_task(self.run_gui_screen_idle(display)))
		page.session.set('gui_hal9k_task', asyncio.create_task(self.run_gui_screen_hal9k(display)))
		self.session_queues[page.session_id] = session_queue
		self.show_idle(display)
