"""
Page Replacement Algorithm Visualizer

Main entry point for the application.

Usage:
    python main.py

Modules:
    constants.py - Configuration and constants  
    models.py - Data models
    algorithms.py - Algorithm implementations
    controllers.py - Animation controller
    windows.py - Visualization windows
    app.py - Main application class
"""

from app import PageReplacementApp


def main():
    """Main entry point"""
    app = PageReplacementApp()
    app.run()


if __name__ == "__main__":
    main()
