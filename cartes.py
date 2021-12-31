from PyQt5 import QtWidgets
from PyQt5 import QtCore
import folium
import io
import json
import sys
import math
import random
import os
import psycopg2
from folium.plugins import Draw, MousePosition, MeasureControl
from jinja2 import Template
from branca.element import Element
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(600, 600)

        # create the main window
        main = QWidget()
        self.setCentralWidget(main)
        main.setLayout(QHBoxLayout())
        main.setFocusPolicy(Qt.StrongFocus)

        self.webView = myWebView()

        controls_panel = QtWidgets.QGridLayout()
        mysplit = QSplitter(Qt.Vertical)

        # adding the map
        mysplit.addWidget(self.webView)

        # create the USER dropdown box
        _label_user = QLabel('User: ', self)
        _label_user.setFixedSize(40, 20)
        self.user_box = QComboBox()
        self.user_box.setEditable(True)
        self.user_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.user_box.setInsertPolicy(QComboBox.NoInsert)

        # create the ADD USER button
        self.add_user_button = QPushButton("Add user")
        # self.add_user_button.setGeometry(4, 4, 4, 4)
        self.add_user_button.clicked.connect(self.add_user)

        # create the delete history button
        self.delete_history_button = QPushButton("Delete history")
        # self.delete_history_button.setGeometry(4, 4, 4, 4)
        self.delete_history_button.clicked.connect(self.delete_history)

        # create the show history button
        self.show_history_button = QPushButton("Show history")
        # self.show_history_button.setGeometry(4, 4, 4, 4)
        self.show_history_button.clicked.connect(self.show_history)

        # create the Go button
        self.go_button = QPushButton("Find \n a \n way !")
        self.go_button.setGeometry(4, 4, 4, 4)
        self.go_button.clicked.connect(self.button_Go)

        # create the FROM dropdown box
        _label_from = QLabel('From: ', self)
        _label_from.setFixedSize(40, 20)
        self.from_box = QComboBox()
        self.from_box.setFixedSize(250, 25)
        self.from_box.setEditable(True)
        self.from_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.from_box.setInsertPolicy(QComboBox.NoInsert)

        # create the TO dropdown box
        _label_to = QLabel('To: ', self)
        _label_to.setFixedSize(25, 20)
        self.to_box = QComboBox()
        self.to_box.setFixedSize(250, 25)
        self.to_box.setEditable(True)
        self.to_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.to_box.setInsertPolicy(QComboBox.NoInsert)

        # create the results table widget
        self.tableWidget = QTableWidget()
        self.tableWidget.doubleClicked.connect(self.table_Click)
        self.rows = []

        # "###################"###################""###################"###################"
        # Laying out the previously created widgets
        # "###################"###################"###################"###################"###################"

        ############################################# ROW 1 ############################################################
        # User
        controls_panel.addWidget(
            _label_user, 1, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        controls_panel.addWidget(self.user_box, 1, 1,
                                 QtCore.Qt.AlignmentFlag.AlignLeft)

        # Show history
        controls_panel.addWidget(self.show_history_button, 1, 2,
                                 QtCore.Qt.AlignmentFlag.AlignLeft)

        # Delete history
        controls_panel.addWidget(self.delete_history_button, 1, 3,
                                 QtCore.Qt.AlignmentFlag.AlignLeft)

        # Add user
        controls_panel.addWidget(self.add_user_button, 1, 4,
                                 QtCore.Qt.AlignmentFlag.AlignLeft)

        ############################################# ROW 2 ############################################################

        # From
        controls_panel.addWidget(
            _label_from, 2, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        controls_panel.addWidget(
            self.from_box, 2, 1, QtCore.Qt.AlignmentFlag.AlignLeft)

        ############################################# ROW 3 ############################################################

        # To
        controls_panel.addWidget(
            _label_to, 3, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        controls_panel.addWidget(
            self.to_box, 3, 1, QtCore.Qt.AlignmentFlag.AlignLeft)

        # Go button
        controls_panel.addWidget(self.go_button, 2, 2, 2, 1)

        ############################################# ROW 4 ############################################################

        # Table
        controls_panel.addWidget(self.tableWidget, 4, 0, 1, 5)

        main.layout().addLayout(controls_panel)
        main.layout().addWidget(mysplit)

        # create the HOPS dropdown box
        # _label = QLabel('Hops: ', self)
        # _label.setFixedSize(20,20)
        # self.hop_box = QComboBox()
        # self.hop_box.addItems( ['1', '2', '3', '4', '5'] )
        # self.hop_box.setCurrentIndex( 2 )
        # controls_panel.addWidget(_label)
        # controls_panel.addWidget(self.hop_box)

        # create the GO button
        # self.go_button = QPushButton("Go!")
        # self.go_button.clicked.connect(self.button_Go)
        # controls_panel.addWidget(self.go_button)

        # create the Clear button
        # self.clear_button = QPushButton("Clear")
        # self.clear_button.clicked.connect(self.button_Clear)
        # controls_panel.addWidget(self.clear_button)

        # Add Folium map types options
        self.maptype_box = QComboBox()
        self.maptype_box.addItems(self.webView.maptypes)
        self.maptype_box.currentIndexChanged.connect(self.webView.setMap)
        # controls_panel.addWidget(self.maptype_box)

        # opening window in maximized size
        self.showMaximized()

        # call function to connect to database
        self.connect_DB()
        self.show_stations_in_lists()
        self.show_users()
        self.startingpoint = True
        self.show()

    # show users in the list

    def show_users(self):
        self.cursor.execute(
            """SELECT name FROM users ORDER BY name""")
        self.conn.commit()
        rows_name = self.cursor.fetchall()

        for row in rows_name:
            self.user_box.addItem(str(row[0]))

    # connect to the Data Base

    def connect_DB(self):
        self.conn = psycopg2.connect(
            database="metro", user="postgres", host="localhost", password="password")

    # show the stations in the list
    def show_stations_in_lists(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """SELECT distinct nom_long FROM metros ORDER BY nom_long""")
        self.conn.commit()
        rows = self.cursor.fetchall()
        for row in rows:
            self.from_box.addItem(str(row[0]))
            self.to_box.addItem(str(row[0]))

    def table_Click(self):
        k = 0
        prev_lat = 0
        for col in self.rows[self.tableWidget.currentRow()]:
            if (k % 3) == 0:
                lst = col.split(',')
                lat = float(lst[0])
                lon = float(lst[1])

                if prev_lat != 0:
                    self.webView.addSegment(prev_lat, prev_lon, lat, lon)
                prev_lat = lat
                prev_lon = lon

                self.webView.addMarker(lat, lon)
            k = k + 1
        # showing each station and the time it takes
        # clear table
        # while (self.tableWidget.rowCount() > 0) :
            #  self.tableWidget.removeRow(0)

        # self.tableWidget.setRowCount(0)
        # self.tableWidget.setColumnCount(0)

        # show time in each transport type
        # i = 0
        # j = 0
        # p = 0
        # for col in self.rows[self.tableWidget.currentRow()]:
        #     if j % 3 == 0:
        #         p = p + 1
        #     # if j-p == 3:
        #     #     i = i + 1
        #     #     j = 0
        #     else:
        #         if j + 1 - p == 4 and j == 5:
        #             i = i + 1
        #             j = 0
        #             p = 1
        #         self.tableWidget.setItem(
        #             i, j + 1 - p, QTableWidgetItem(str(col)))
        #     j = j + 1
        self.tableWidget.clear()
        i = 0
        j = 0
        p = 0
        for col in self.rows[self.tableWidget.currentRow()]:
            if j % 3 == 0:
                j = j + 1
            # if j-p == 3:
            #     i = i + 1
            #     j = 0
            else:
                if j == 4 :
                    self.tableWidget.setItem(
                    i, j - 1 , QTableWidgetItem(str(col)))
                    i = i + 1
                    j = 1
                    self.tableWidget.setItem(
                    i, j , QTableWidgetItem(str(col)))
                    j = j + 1

                else :        
                    self.tableWidget.setItem(
                        i, j , QTableWidgetItem(str(col)))
                    j = j + 1
        _current_user = str(self.user_box.currentText())
        if _current_user != "anonymous" :

            self.cursor.execute(
            f"""SELECT id FROM users WHERE name = '{_current_user}'""")
            self.conn.commit()
            _current_user_id = self.cursor.fetchall()
               
            m = str(self.rows[self.tableWidget.currentRow()])
            m2 = m.replace("'","$")
            itineraire = m2.replace(",","£")

            print(itineraire)
            self.cursor.execute(
                f"""INSERT INTO user_history VALUES ('{_current_user_id[0][0]}','{itineraire}')""")
            self.conn.commit()
            
        

    # just a simple dialog box that asks for the name, maybe we'll add home address ? to be discussed if we still have time
    def add_user(self):
        name, done1 = QtWidgets.QInputDialog.getText(
            self, 'Input Dialog', 'Enter your name:')

        if done1:
            self.cursor.execute(
                f"""INSERT INTO users(name) VALUES ('{name}')""")
            self.conn.commit()
            self.user_box.addItem(f"""{name}""")

    def show_history(self):
        # clear map
        self.webView.clearMap(self.maptype_box.currentIndex())
        self.startingpoint = True
        self.update()
        # clear table
        self.tableWidget.clear()

        # complete code => get history from user history table

    def delete_history(self):
        # remove all rows for a certain user
        return

    def button_Go(self):
        self.tableWidget.clearContents()

        _fromstation = str(self.from_box.currentText())
        _tostation = str(self.to_box.currentText())
        _hops = 10  # int(self.hop_box.currentText())

        self.rows = []

        if _hops >= 1:
            self.cursor.execute(
                ""f" SELECT distinct A.geo_point_2d, A.nom_long, A.res_com, B.geo_point_2d, B.nom_long FROM metros as A, metros as B WHERE A.nom_long = $${_fromstation}$$ AND B.nom_long = $${_tostation}$$ AND A.res_com = B.res_com""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()

        if _hops >= 2:
            self.cursor.execute(
                ""f" SELECT distinct A.geo_point_2d, A.nom_long, A.res_com, B.geo_point_2d, B.nom_long, C.res_com, D.geo_point_2d, D.nom_long FROM metros as A, metros as B, metros as C, metros as D WHERE A.nom_long = $${_fromstation}$$ AND D.nom_long = $${_tostation}$$ AND A.res_com = B.res_com AND B.nom_long = C.nom_long AND C.res_com = D.res_com AND A.res_com <> C.res_com AND A.nom_long <> B.nom_long AND B.nom_long <> D.nom_long""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()

        if _hops >= 3:
            self.cursor.execute(
                ""f" SELECT distinct A.geo_point_2d, A.nom_long, A.res_com, B2.geo_point_2d, B2.nom_long, B2.res_com, C2.geo_point_2d, C2.nom_long, C2.res_com, D.geo_point_2d, D.nom_long FROM metros as A, metros as B1, metros as B2, metros as C1, metros as C2, metros as D WHERE A.nom_long = $${_fromstation}$$ AND A.res_com = B1.res_com AND B1.nom_long = B2.nom_long AND B2.res_com = C1.res_com AND C1.nom_long = C2.nom_long AND C2.res_com = D.res_com AND D.nom_long = $${_tostation}$$ AND A.res_com <> B2.res_com AND B2.res_com <> C2.res_com AND A.res_com <> C2.res_com AND A.nom_long <> B1.nom_long AND B2.nom_long <> C1.nom_long AND C2.nom_long <> D.nom_long""")
            self.conn.commit()
            self.rows += self.cursor.fetchall()

        if len(self.rows) == 0:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return

        numrows = len(self.rows)
        numcols = len(self.rows[-1]) - math.floor(len(self.rows[-1]) / 3.0) - 1
        # print("type(self.rows)" + str(type(self.rows)))
        # print(self.rows)
        # print("len(self.rows) "+ str(len(self.rows)))
        # print("len(self.rows[-1]) = " + str(len(self.rows[-1])))
        # print("numrows = " + str(numrows))
        # print("numcols = " + str(numcols))
        self.tableWidget.setRowCount(numrows)
        self.tableWidget.setColumnCount(numcols)

        i = 0
        for row in self.rows:
            j = 1
            k = 0
            for col in row:
                # if j % 3 == 0:
                if len(row) == 5:
                    if col == row[0] or col == row[1] or col == row[3] or col == row[4]:
                        k = k + 1
                    else:
                        self.tableWidget.setItem(
                            i, j-k, QTableWidgetItem(str(col)))
                    j = j + 1

                if len(row) == 8:
                    if col == row[0] or col == row[1] or col == row[3] or col == row[4] or col == row[6] or col == row[7]:
                        k = k + 1
                    else:
                        self.tableWidget.setItem(
                            i, j-k, QTableWidgetItem(str(col)))
                    j = j + 1

                if len(row) == 11:
                    if col == row[0] or col == row[1] or col == row[3] or col == row[4] or col == row[6] or col == row[7] or col == row[9] or col == row[10]:
                        k = k + 1
                    else:
                        self.tableWidget.setItem(
                            i, j-k, QTableWidgetItem(str(col)))
                    j = j + 1
            i = i + 1

        header = self.tableWidget.horizontalHeader()
        j = 0
        while j < numcols:
            header.setSectionResizeMode(j, QHeaderView.ResizeToContents)
            j = j+1

        self.update()

    def mouseClick(self, lat, lng):
        self.webView.addPointMarker(lat, lng)

        print(f"Clicked on: latitude {lat}, longitude {lng}")
        self.cursor.execute(
            ""f" WITH mytable (distance, name) AS (SELECT ( ABS(latitude-{lat}) + ABS(longitude-{lng}) ), nom_long FROM metros) SELECT A.name FROM mytable as A WHERE A.distance <=  (SELECT min(B.distance) FROM mytable as B)  """)
        self.conn.commit()
        rows = self.cursor.fetchall()
        #print('Closest STATION is: ', rows[0][0])
        if self.startingpoint:
            self.from_box.setCurrentIndex(
                self.from_box.findText(rows[0][0], Qt.MatchFixedString))
        else:
            self.to_box.setCurrentIndex(
                self.to_box.findText(rows[0][0], Qt.MatchFixedString))
        self.startingpoint = not self.startingpoint


class myWebView (QWebEngineView):
    def __init__(self):
        super().__init__()

        self.maptypes = ["OpenStreetMap", "Stamen Terrain",
                         "stamentoner", "cartodbpositron"]
        self.setMap(0)

    def add_customjs(self, map_object):
        my_js = f"""{map_object.get_name()}.on("click",
                 function (e) {{
                    var data = `{{"coordinates": ${{JSON.stringify(e.latlng)}}}}`;
                    console.log(data)}}); """
        e = Element(my_js)
        html = map_object.get_root()
        html.script.get_root().render()
        html.script._children[e.get_name()] = e

        return map_object

    def handleClick(self, msg):
        data = json.loads(msg)
        lat = data['coordinates']['lat']
        lng = data['coordinates']['lng']

        window.mouseClick(lat, lng)

    def addSegment(self, lat1, lng1, lat2, lng2):
        js = Template(
            """
        L.polyline(
            [ [{{latitude1}}, {{longitude1}}], [{{latitude2}}, {{longitude2}}] ], {
                "color": "red",
                "opacity": 1.0,
                "weight": 4,
                "line_cap": "butt"
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude1=lat1, longitude1=lng1, latitude2=lat2, longitude2=lng2)

        self.page().runJavaScript(js)

    def addMarker(self, lat, lng):
        js = Template(
            """
        L.marker([{{latitude}}, {{longitude}}] ).addTo({{map}});
        L.circleMarker(
            [{{latitude}}, {{longitude}}], {
                "bubblingMouseEvents": true,
                "color": "#3388ff",
                "popup": "hello",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": "#3388ff",
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 5
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)

    def addPointMarker(self, lat, lng):
        js = Template(
            """
        L.circleMarker(
            [{{latitude}}, {{longitude}}], {
                "bubblingMouseEvents": true,
                "color": 'green',
                "popup": "hello",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": 'green',
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 5
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)

    def setMap(self, i):
        self.mymap = folium.Map(location=[
                                48.8619, 2.3519], tiles=self.maptypes[i], zoom_start=12, prefer_canvas=True)

        self.mymap = self.add_customjs(self.mymap)

        page = WebEnginePage(self)
        self.setPage(page)

        data = io.BytesIO()
        self.mymap.save(data, close_file=False)

        self.setHtml(data.getvalue().decode())

    def clearMap(self, index):
        self.setMap(index)


class WebEnginePage(QWebEnginePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        # print(msg)
        if 'coordinates' in msg:
            self.parent.handleClick(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
