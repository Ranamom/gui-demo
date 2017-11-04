import locale
import logging
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
import app
from app.widgets.proto import MainWindow
from app import helpers


helpers.init_logging()
log = logging.getLogger(__name__)


class Application(QtWidgets.QApplication):

    def __init__(self, args, main_widget=None):
        log.debug('init app')
        super().__init__(args)

        self.setQuitOnLastWindowClosed(False)

        # Initialize application metadata
        locale.setlocale(locale.LC_ALL, '')
        self.setOrganizationName(app.ORG_NAME)
        self.setOrganizationDomain(app.ORG_DOMAIN)
        self.setApplicationDisplayName(app.APP_NAME)
        self.setApplicationName(app.APP_NAME)
        self.setApplicationVersion(app.APP_VERSION)

        # Gui Styles and Fonts
        self.setStyle('fusion')
        font_db = QtGui.QFontDatabase()
        font_db.addApplicationFont(':/fonts/resources/Roboto-Light.ttf')
        font_db.addApplicationFont(':/fonts/resources/RobotoCondensed-Regular.ttf')
        font_db.addApplicationFont(':/fonts/resources/Oswald-Regular.ttf')
        font_db.addApplicationFont(':/fonts/resources/Oswald-SemiBold.ttf')
        app_font = QtGui.QFont("Roboto Light")
        app_font.setStyleStrategy(QtGui.QFont.PreferAntialias | QtGui.QFont.PreferQuality)
        app_font.setHintingPreference(QtGui.QFont.PreferNoHinting)
        self.setFont(app_font)

        # Initialize main window
        self.ui = main_widget() if main_widget else MainWindow()

        self.aboutToQuit.connect(self.cleanup)

        # Shortcuts
        if hasattr(self.ui, 'node'):
            self.ui.debug_shortcut = QtWidgets.QShortcut('Ctrl+K', self.ui, self.ui.node.kill)
            self.ui.debug_shortcut = QtWidgets.QShortcut('Ctrl+S', self.ui, self.ui.node.stop)
            self.ui.debug_shortcut = QtWidgets.QShortcut('Ctrl+R', self.ui, self.ui.node.start)

    @pyqtSlot()
    def cleanup(self):
        """Final application teardown/cleanup"""
        log.debug('init app teardown cleanup')
        if hasattr(self.ui, 'node'):
            try:
                log.debug('attempt gracefull node shuttdown via rpc')
                rpc_result = self.ui.node.stop()
                log.debug('rpc stop returned: %s' % rpc_result)
                assert rpc_result == "MultiChain server stopping"
            except Exception as e:
                log.exception('failed rpc shutdown - try to kill node process')
                self.ui.node.kill()
        self.ui.data_db.close()
        self.ui.profile_db.close()
        log.debug('finished app teardown cleanup - quitting.')
