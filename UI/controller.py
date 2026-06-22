import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._anno1 = None
        self._anno2 = None


    def handleCreaGrafo(self,e):
        if self._anno1 is None or self._anno2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegliere anno 1 e anno 2", color="orange"))
            self._view.update_page()
            return

        if self._anno1 > self._anno2:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegliere anno1 in modo tale che sia più piccolo di anno2", color="orange"))
            self._view.update_page()
            return

        self._model.buildGraph(self._anno1, self._anno2)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato.", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))
        self._view.update_page()

    def handleDettagli(self, e):
        self._view.txt_result.controls.append(
            ft.Text("Archi di peso maggiore:", color="red"))
        for a in self._model.getTop3():
            self._view.txt_result.controls.append(ft.Text(f"{a[0].surname} --> {a[1].surname} ({a[2]['weight']})"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumCompConn()} componenti connesse", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"Componente più grande ({self._model.getCompConn()[0]} nodi):", color="red"))
        for e in self._model.getCompConn()[1]:
            self._view.txt_result.controls.append(ft.Text(f"{e.surname} ({e.driverId}) -- DoB: {e.dob}"))
        self._view.txt_result.controls.append(
            ft.Text("Componente connessa in ordine decrescente:", color="red"))
        for e in self._model.getCompConn()[2]:
            self._view.txt_result.controls.append(ft.Text(f"{e[0].surname} ({e[0].driverId}) -- DoB: {e[0].dob} (grado={e[1]})"))
        self._view.update_page()



    def handleCerca(self, e):
        pass

    def fillDDYears(self):
        allYears = self._model.getAllYears()
        for a in allYears:
            self._view._ddAnno1.options.append(
                ft.dropdown.Option(data=a, key=a, on_click=self._choiceDDYear1))
            self._view._ddAnno2.options.append(
                ft.dropdown.Option(data=a, key=a, on_click=self._choiceDDYear2))

    def _choiceDDYear1(self, e):
        self._anno1 = e.control.data
        print(f"hai selezionato {self._anno1}")

    def _choiceDDYear2(self, e):
        self._anno2 = e.control.data
        print(f"hai selezionato {self._anno2}")