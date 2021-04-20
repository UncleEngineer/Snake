from tkinter import *
from PIL import Image, ImageTk
from random import randint

MOVE_INCREMENT = 20
MOVE_PER_SECOND = 15
GAME_SPEED = 1000 // MOVE_PER_SECOND

class Snake(Canvas):
	def __init__(self):
		super().__init__(width=600,height=620,background='black',highlightthickness=0)

		self.reset = [(100,100),(80,100),(60,100)]
		self.snake_positions = [(100,100),(80,100),(60,100)]
		# self.food_position = (200,100)
		#self.food_position = (200,100)
		self.food_position = self.set_new_food_position()
		self.score = 0
		self.direction = 'Right'
		self.bind_all('<Key>', self.on_key_press)
		self.loop = None
		self.starting = True

		self.bind('<F1>',self.perform_actions)

		self.load_assets()
		self.create_objects()
		#print(self.find_withtag('snake'))
		self.perform_actions()
		#self.after(GAME_SPEED, self.perform_actions)
		

	def load_assets(self):
		try:
			self.snake_body_image = Image.open('./assets/snake.png')
			self.snake_body = ImageTk.PhotoImage(self.snake_body_image)
			self.food_image = Image.open("./assets/food.png")
			self.food = ImageTk.PhotoImage(self.food_image)
		except:
			GUI.destroy()

	def create_objects(self):

		self.create_text(45,12,text=f'Score {self.score}',tag='score',fill='#fff',font=(None,14))

		for x_position, y_position in self.snake_positions:
			self.create_image(x_position,y_position,image=self.snake_body,tag='snake')

		self.create_image(self.food_position[0],self.food_position[1],image=self.food,tag="food")
		self.create_rectangle(7,27,593,613, outline='#525d69')


	def move_snake(self):

		head_x_position, head_y_position = self.snake_positions[0]

		if self.direction == "Left":
			new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
		elif self.direction == "Right":
			new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
		elif self.direction == "Down":
			new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
		elif self.direction == "Up":
			new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

		#new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
		#print('NEW HEAD:',new_head_position)
		#print('LSP',self.snake_positions[:-1])
		self.snake_positions = [new_head_position] + self.snake_positions[:-1]
		#print('PS:',self.snake_positions)
		findsnake = self.find_withtag('snake')
		#print(findsnake)
		for segment, position in zip(findsnake,self.snake_positions):
			self.coords(segment, position)


	def perform_actions(self,event=None):
		if self.check_collisions() and self.starting == True:
			self.after_cancel(self.loop)
			self.starting = False
			self.delete('all')
			self.create_text(300,300,justify=CENTER,text=f'GAME OVER\n\nScore: {self.score}\n\nNew Game <F1>',tag='score',fill='#fff',font=(None,30))
			#print('COLLISION')
		elif self.check_collisions() and self.starting == False:
			self.delete('all')
			self.snake_positions = self.reset
			self.food_position = self.set_new_food_position()
			self.create_objects()
			self.starting = True
			self.direction = 'Right'
			self.score = 0
			#print('New')
			self.loop = self.after(GAME_SPEED, self.perform_actions)

		else:
			self.check_food_collistion()
			self.move_snake()
			self.loop = self.after(GAME_SPEED, self.perform_actions)

	def check_collisions(self):
		head_x_position, head_y_position = self.snake_positions[0]

		return (
			head_x_position in (0, 600)
			or head_y_position in (20,620)
			or (head_x_position,head_y_position) in self.snake_positions[1:]

		)

	def on_key_press(self,e):
		new_direction = e.keysym
		#print(new_direction)
		# self.direction = new_direction

		all_direction = ('Up','Down','Left','Right')
		opposites = ({'Up','Down'},{'Left','Right'})

		if (new_direction in all_direction 
			and {new_direction,self.direction} not in opposites):
			self.direction = new_direction
		elif new_direction == 'F1':
			self.perform_actions()



	def check_food_collistion(self):
		if self.snake_positions[0] == self.food_position:
			self.score += 1
			self.snake_positions.append(self.snake_positions[-1]) #เพิ่มเข้าตำแหน่งสุดท้ายของงูแล้วสร้างรูปขึ้นมา


			self.create_image(*self.snake_positions[-1], image=self.snake_body, tag='snake')

			score = self.find_withtag('score')
			self.itemconfigure(score, text=f'Score: {self.score}',tag='score')

			self.food_position = self.set_new_food_position()
			self.coords(self.find_withtag('food'),self.food_position)


	def set_new_food_position(self):
		while True:
			x_position = randint(1,29) * MOVE_INCREMENT
			y_position = randint(3,30) * MOVE_INCREMENT
			food_position = (x_position,y_position)

			if food_position not in self.snake_positions:
				return food_position

GUI = Tk()
GUI.title('Snake Game by Uncle Engineer')
GUI.resizable(False,False)


board = Snake()
board.pack()


GUI.mainloop()