from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainWindow.sizePolicy().hasHeightForWidth())
        mainWindow.setSizePolicy(sizePolicy)
        mainWindow.setMinimumSize(QtCore.QSize(800, 200))
        mainWindow.setMaximumSize(QtCore.QSize(800, 200))
        mainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        mainWindow.setAcceptDrops(False)
        mainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Submit = QtWidgets.QPushButton(self.centralwidget)
        self.Submit.setGeometry(QtCore.QRect(710, 560, 85, 32))
        self.Submit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Submit.setObjectName("Submit")
        self.Cancel = QtWidgets.QPushButton(self.centralwidget)
        self.Cancel.setGeometry(QtCore.QRect(630, 560, 81, 32))
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cancel.setObjectName("Cancel")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(160, 50, 131, 31))
        self.pushButton.setObjectName("pushButton")
       	self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Check = QtWidgets.QCheckBox(self.centralwidget)
        self.Check.setGeometry(QtCore.QRect(180, 510, 40, 20))
        self.Check.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Check.setText("")
        self.Check.setObjectName("Check")
        self.Name = QtWidgets.QLineEdit(self.centralwidget)
        self.Name.setGeometry(QtCore.QRect(62, 20, 721, 21))
        self.Name.setObjectName("Name")
        mainWindow.setCentralWidget(self.centralwidget)

        self.Cancel.clicked.connect(mainWindow.close)
        self.pushButton.clicked.connect(self.running)
        self.Submit.clicked.connect(self.running)
    
    def running(self):
        import nltk
        import sys
        import os
        import re

        TERMINALS = """
        Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
        Adv -> "down" | "here" | "never"
        Conj -> "and" | "until"
        Det -> "a" | "an" | "his" | "my" | "the"
        N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
        N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
        N -> "smile" | "thursday" | "walk" | "we" | "word"
        P -> "at" | "before" | "in" | "of" | "on" | "to"
        V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
        V -> "smiled" | "tell" | "were"
        """

        NONTERMINALS = """
        S -> PN PV | PS | PV PN | PV
        PS -> S Conj S
        PN -> N |Adj N | Det N | Det PN | Adj PN | PN Adj | PN PN | P PN | Adv PN | PN Adv
        PV -> V | V PN | PV Adj | Adv PV | PV Adv
        """

        grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
        parser = nltk.ChartParser(grammar)

        Sentence = self.Name.text()
        
        def main(Sentence):

            # Convert input into list of words
            s = preprocess(Sentence)

            # Attempt to parse sentence
            try:
                trees = list(parser.parse(s))
            except ValueError as e:
                print(e)
                return
            if not trees:
                print("Could not parse sentence.")
                return

            # Print each tree with noun phrase chunks
            for tree in trees:
                tree.pretty_print()

                print("Noun Phrase Chunks")
                for np in np_chunk(tree):
                    print(" ".join(np.flatten()))


        def preprocess(sentence):
            """
            Convert `sentence` to a list of its words.
            Pre-process sentence by converting all characters to lowercase
            and removing any word that does not contain at least one alphabetic
            character.
            """
            sentence = sentence.lower()
            words = nltk.word_tokenize(sentence)
            
            for word in words:
                if re.match('[a-z]', word):
                    continue
                else:
                    words.remove(word)
            return words


        def np_chunk(tree):
            """
            Return a list of all noun phrase chunks in the sentence tree.
            A noun phrase chunk is defined as any subtree of the sentence
            whose label is "NP" that does not itself contain any other
            noun phrases as subtrees.
            """
            chunks = []
            parent_tree = nltk.tree.ParentedTree.convert(tree)

            for subtree in parent_tree.subtrees(lambda t: t.label() == 'N'):
                chunks.append(subtree.parent())
            return chunks

        if __name__ == "__main__":
            main()
 

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())