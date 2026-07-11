import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        voti = self._model.getAllVoti()

        for g in voti:
            g_str = str(g)
            # self._view._ddGenre.options.append( g_str)
            self._view._ddrating1.options.append(ft.dropdown.Option(key=g_str, text=g_str))
            self._view._ddrating2.options.append(ft.dropdown.Option(key=g_str, text=g_str))

        self._view.update_page()


    def handleCreaGrafo(self, e):
        self._model.buildGraph(self._view._ddrating1.value, self._view._ddrating2.value)
        Nnodes, Nedges = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grapfo correttamente creato. "
                                                      f"Il grafo contiene {Nnodes} nodi e {Nedges} archi"))


    def handleCammino(self, e):
        pass