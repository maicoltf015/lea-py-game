from graphics import *

def direction_window(title='Decision Window', width=100, height=150, text_opt1="Upstairs", text_opt2="Left", text_opt3="Right"):
    # Crea una ventana gráfica
    window = GraphWin(title, width, height)
    options = []

    # Crea dos opciones en la ventana
    opcion1 = Rectangle(Point(50, 50), Point(140, 100))
    opcion1.setFill("blue")
    opcion1.draw(window)
    opcion1_text = Text(Point(90, 75), text_opt1)
    opcion1_text.setTextColor('white')
    opcion1_text.draw(window)

    opcion2 = Rectangle(Point(150, 50), Point(240, 100))
    opcion2.setFill("red")
    opcion2.draw(window)
    opcion2_text = Text(Point(190, 75), text_opt2)
    opcion2_text.setTextColor('white')
    opcion2_text.draw(window)

    opcion3 = Rectangle(Point(250, 50), Point(340, 100))
    opcion3.setFill("purple")
    opcion3.draw(window)
    opcion3_text = Text(Point(290, 75), text_opt3)
    opcion3_text.setTextColor('white')
    opcion3_text.draw(window)

    selected_option = 0

    while True:
        try :
            p = window.getMouse()

            if opcion1.getP1().getX() <= p.getX() <= opcion1.getP2().getX() and \
                opcion1.getP1().getY() <= p.getY() <= opcion1.getP2().getY(): 
                selected_option = 1
                break

            elif opcion2.getP1().getX() <= p.getX() <= opcion2.getP2().getX() and \
                opcion2.getP1().getY() <= p.getY() <= opcion2.getP2().getY(): 
                selected_option = 2
                break

            elif opcion3.getP1().getX() <= p.getX() <= opcion3.getP2().getX() and \
                opcion3.getP1().getY() <= p.getY() <= opcion3.getP2().getY(): 
                selected_option = 3 
                break

            else:
                selected_option = 0
                
        except GraphicsError:
            return 0

    window.close()
    return selected_option


def game_over_window(): 

    try :
        # Crear una ventana
        win = GraphWin("Game Over", 200, 200)
        
        # Crear un círculo para la cabeza
        head = Circle(Point(100, 100), 70)
        head.setFill("yellow")
        head.draw(win)

        # Crear dos círculos para los ojos
        left_eye = Circle(Point(70, 70), 10)
        left_eye.setFill("black")
        left_eye.draw(win)
        right_eye = Circle(Point(130, 70), 10)
        right_eye.setFill("black")
        right_eye.draw(win)

        # Crear una línea para la boca
        mouth = Line(Point(70, 130), Point(130, 130))
        mouth.setWidth(10)
        mouth.draw(win)

        title = Text(Point(100, 10), "Game Over")
        title.setSize(20)
        title.draw(win)

        # Mostrar la ventana
        win.getMouse()
        win.close()
    except GraphicsError:
        return 0


def winner_window(window_title="Treasure box", action='You level up', prize="+50 points"): 

    try :
        # Crear una ventana flotante con un tamaño específico
        win = GraphWin(window_title, 400, 400)

        # Crear un rectángulo para la base de la caja
        rect = Rectangle(Point(50, 50), Point(350, 350))
        rect.setFill("saddlebrown")
        rect.draw(win)

        # Crear una tapa triangular para la caja
        tapa = Polygon(Point(50, 50), Point(350, 50), Point(200, 250))
        tapa.setFill("goldenrod")
        tapa.draw(win)

        # Agregar etiquetas de texto con la información de la caja
        title = Text(Point(200, 20), action)
        title.setSize(20)
        title.draw(win)

        etiqueta1 = Text(Point(200, 80), "You have obtained a:")
        etiqueta1.draw(win)

        text1 = Text(Point(200, 100), "Treasure 💎")
        text1.setStyle("bold")
        text1.draw(win)

        etiqueta2 = Text(Point(200, 150), "You've won:")
        etiqueta2.draw(win)

        text2 = Text(Point(200, 170), prize)
        text2.setStyle("bold")
        text2.draw(win)

        # Mantener la ventana abierta
        win.getMouse()
        win.close()
    except GraphicsError:
        return None
        