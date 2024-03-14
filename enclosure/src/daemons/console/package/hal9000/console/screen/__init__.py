import time
import flet


class Screen(flet.Container):

	def __init__(self) -> None:
		super().__init__(width=750, height=500)
		self.padding = flet.padding.all(15)
		self.screen_page = None
		self.screen_parent = None


	def setContext(self, page: flet.Page, parent: flet.AnimatedSwitcher):
		self.screen_page = page
		self.screen_parent = parent


	def on_show(self, e: flet.ContainerTapEvent):
		if self.screen_parent is not None:
			self.screen_parent.content = flet.Image(width=750, height=500, src=e.control.content.src, fit=flet.ImageFit.FILL, border_radius=flet.border_radius.all(10))
		if self.screen_page is not None:
			screen_page = self.screen_page
			self.screen_page = None
			screen_page.update()
			self.screen_page = screen_page
		time.sleep(1)
		if self.screen_parent is not None:
			self.screen_parent.content = self
		if self.screen_page is not None:
			screen_page = self.screen_page
			self.screen_page = None
			screen_page.update()
			self.screen_page = screen_page


	def build(self):
		super().build()
		self.screen = flet.Column()
		self.screen.controls.append(flet.Row(controls=[flet.Text("TODO (functionality not yet implemented)", size=20)], alignment=flet.MainAxisAlignment.CENTER))
		self.content = self.screen

