#!/bin/bash
# AdNexus Tracker Launcher Script
# Makes it easy to run the investment tracker

echo "================================================"
echo "   AdNexus - Vinmo Investment Tracker v1.0     "
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    echo "   Download from: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if Streamlit is installed
if ! pip show streamlit &> /dev/null; then
    echo "📥 Installing required packages..."
    pip install streamlit pandas numpy plotly
    echo "✅ Packages installed"
    echo ""
fi

# Launch the app
echo "🚀 Launching AdNexus Tracker..."
echo "   The app will open in your browser at http://localhost:8501"
echo "   Press Ctrl+C to stop the server"
echo ""
echo "================================================"
echo ""

# Run Streamlit
streamlit run adnexus_tracker_app.py --server.port 8501 --server.address localhost

# Deactivate virtual environment when done
deactivate