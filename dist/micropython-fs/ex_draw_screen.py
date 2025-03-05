from badge import Screen

s = Screen()
s.draw_point(20, 100)
s.draw_point(30, 100)
s.draw_point(40, 100)
s.draw_point(50, 100)
s.draw_circle(150, 60, 20, filled=True)
s.draw_line(1, 1, 200, 89)
s.draw_rectangle(10, 10, 200, 20, color=Screen.Red, filled=True)
s.draw_string(10, 56, "hello world", 16, color=Screen.Red)
s.update()
