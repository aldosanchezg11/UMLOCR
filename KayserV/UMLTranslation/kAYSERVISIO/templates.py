import cv2

# Load your template images for each symbol
templates = {
    "decisionm": cv2.imread('C:/Users/p.calidadoperaciones/ProyectosAldo/P1/Templates/Symbols.png', 0),
    "decisionx": cv2.imread('C:/Users/p.calidadoperaciones/ProyectosAldo/P1/Templates/Symbols.png', 0),
    "eventoI": cv2.imread('C:/Users/p.calidadoperaciones/ProyectosAldo/P1/Templates/Symbols.png', 0),
    "eventoP": cv2.imread('C:/Users/p.calidadoperaciones/ProyectosAldo/P1/Templates/Symbols.png', 0),
    "eventoF": cv2.imread('C:/Users/p.calidadoperaciones/ProyectosAldo/P1/Templates/Symbols.png', 0),
    "flujosequencia": cv2.imread('C:/Users/p.calidadoperaciones/ProyectosAldo/P1/Templates/Symbols.png', 0),
    "almacenamientodatos": cv2.imread('C:/Users/p.calidadoperaciones/ProyectosAldo/P1/Templates/Symbols.png', 0),
}

# Load template for small marks
mark_templates = {
    "servicio": cv2.imread('C:/Users/p.calidadoperaciones/ProyectosAldo/P1/Templates/subsection_mark_template.png', 0),
    "mensaje": cv2.imread('C:/Users/p.calidadoperaciones/ProyectosAldo/P1/Templates/Marks.png', 0),
    "usuario": cv2.imread('C:/Users/p.calidadoperaciones/ProyectosAldo/P1/Templates/Marks.png', 0),
    "documento": cv2.imread('C:/Users/p.calidadoperaciones/ProyectosAldo/P1/Templates/Marks.jpg', 0)
}
