import streamlit as st
import numpy as np
import plotly.graph_objects as go

class Superficie3D:
    def __init__(self, x_range, y_range):
        self.x_range = x_range
        self.y_range = y_range
        self.x, self.y = np.meshgrid(np.linspace(x_range[0], x_range[1], 100), 
                                     np.linspace(y_range[0], y_range[1], 100))

    def calcular_z(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")

    def generar_datos(self):
        self.z = self.calcular_z()
        return self.x, self.y, self.z

class Plano(Superficie3D):
    def __init__(self, x_range, y_range, pendiente):
        super().__init__(x_range, y_range)
        self.pendiente = pendiente

    def calcular_z(self):
        return self.pendiente * self.x

class Paraboloide(Superficie3D):
    def __init__(self, x_range, y_range, coef):
        super().__init__(x_range, y_range)
        self.coef = coef

    def calcular_z(self):
        return self.coef * (self.x**2 + self.y**2)

class Sinusoide(Superficie3D):
    def __init__(self, x_range, y_range, frecuencia):
        super().__init__(x_range, y_range)
        self.frecuencia = frecuencia

    def calcular_z(self):
        return np.sin(self.frecuencia * np.sqrt(self.x**2 + self.y**2))

class Visualizador3D:
    def __init__(self, superficie):
        self.superficie = superficie

    def mostrar_con_plotly(self):
        x, y, z = self.superficie.generar_datos()
        fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
        fig.update_layout(title='Superficie 3D', autosize=False, width=800, height=800)
        return fig

def main():
    st.title("Visualización de Superficies 3D")
    
    superficie_tipo = st.selectbox("Seleccione el tipo de superficie:", ["Plano", "Paraboloide", "Sinusoide"])
    
    if superficie_tipo == "Plano":
        pendiente = st.slider("Ingrese la pendiente del plano:", -10.0, 10.0, 1.0)
        superficie = Plano((-5, 5), (-5, 5), pendiente)
    elif superficie_tipo == "Paraboloide":
        coef = st.slider("Ingrese el coeficiente del paraboloide:", 0.1, 10.0, 1.0)
        superficie = Paraboloide((-5, 5), (-5, 5), coef)
    elif superficie_tipo == "Sinusoide":
        frecuencia = st.slider("Ingrese la frecuencia de la sinusoide:", 0.1, 10.0, 1.0)
        superficie = Sinusoide((-5, 5), (-5, 5), frecuencia)
    
    visualizador = Visualizador3D(superficie)
    fig = visualizador.mostrar_con_plotly()
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
