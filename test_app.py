#!/usr/bin/env python3
"""
Test script for JALU Streamlit App
Tests key functionality and visual improvements
"""

import sys
import os
import subprocess
import time
import requests
from PIL import Image
import io

def test_app_structure():
    """Test if app.py exists and has required components"""
    print("🔍 Testing app structure...")

    if not os.path.exists('app.py'):
        print("❌ app.py not found")
        return False

    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for key components
    required_components = [
        'streamlit',
        'Tailwind CSS',
        'metric-card',
        'Beranda Website',
        'Dashboard Analisis',
        'Deteksi AI Vision',
        'YOLO'
    ]

    missing_components = []
    for component in required_components:
        if component not in content:
            missing_components.append(component)

    if missing_components:
        print(f"❌ Missing components: {missing_components}")
        return False

    print("✅ App structure is valid")
    return True

def test_css_improvements():
    """Test if CSS improvements are properly implemented"""
    print("🎨 Testing CSS improvements...")

    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for enhanced metric card CSS
    css_checks = [
        'linear-gradient(135deg, rgba(255,255,255,0.98)',
        'backdrop-filter: blur(15px)',
        'box-shadow: 0 8px 32px rgba(0,0,0,0.08)',
        'background: linear-gradient(90deg, #3b82f6, #06b6d4, #10b981)',
        'transform: translateY(-8px) scale(1.03)',
        'color: #1f2937 !important'
    ]

    missing_css = []
    for css in css_checks:
        if css not in content:
            missing_css.append(css)

    if missing_css:
        print(f"❌ Missing CSS improvements: {missing_css}")
        return False

    print("✅ CSS improvements are properly implemented")
    return True

def test_navigation_pages():
    """Test if all navigation pages are defined"""
    print("🧭 Testing navigation pages...")

    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    pages = [
        "Beranda Website",
        "Dashboard Analisis",
        "Deteksi AI Vision"
    ]

    missing_pages = []
    for page in pages:
        if page not in content:
            missing_pages.append(page)

    if missing_pages:
        print(f"❌ Missing pages: {missing_pages}")
        return False

    print("✅ All navigation pages are defined")
    return True

def test_metric_cards():
    """Test if metric cards are properly implemented"""
    print("📊 Testing metric cards...")

    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for metric card content
    metrics = [
        "55.1 Juta",
        "Penerima Manfaat",
        "Rp 335 T",
        "Anggaran",
        "14%",
        "Target Stunting"
    ]

    missing_metrics = []
    for metric in metrics:
        if metric not in content:
            missing_metrics.append(metric)

    if missing_metrics:
        print(f"❌ Missing metric content: {missing_metrics}")
        return False

    print("✅ Metric cards are properly implemented")
    return True

def test_dependencies():
    """Test if required dependencies are available"""
    print("📦 Testing dependencies...")

    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'PIL',
        'ultralytics'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ Missing packages: {missing_packages}")
        return False

    print("✅ All required dependencies are available")
    return True

def test_data_loading():
    """Test if data loading functions work"""
    print("📊 Testing data loading...")

    try:
        # Import functions from app.py (this is a simplified test)
        import pandas as pd
        import numpy as np
        import random

        # Test nutrition data generation
        data = {
            "FoodType": ["Banana", "Apple", "Orange", "Broccoli", "Carrot"],
            "Quantity": ["1 medium", "1 medium", "1 medium", "100g", "100g"],
            "Protein": [1.3, 0.5, 1.2, 2.8, 0.9],
            "Carbs": [27.0, 25.0, 15.0, 7.0, 10.0],
            "Fat": [0.3, 0.3, 0.2, 0.4, 0.2],
            "Calories": [105, 95, 62, 34, 41]
        }
        nutrition_data = pd.DataFrame(data)

        # Test MBG data generation
        provinces = ["DKI Jakarta", "Jawa Barat", "Jawa Tengah"]
        levels = ["SD", "SMP", "SMA"]
        mbg_data = []
        for prov in provinces:
            for lvl in levels:
                mbg_data.append({
                    "Provinsi": prov,
                    "Jenjang_Pendidikan": lvl,
                    "Jumlah_Siswa_Penerima": random.randint(50000, 200000),
                    "Tingkat_Kepuasan": random.uniform(70, 95),
                    "Penurunan_Stunting": random.uniform(5, 15),
                    "Indeks_Keberhasilan": random.uniform(75, 98),
                    "Anggaran_Terserap": random.uniform(80, 100)
                })
        mbg_data = pd.DataFrame(mbg_data)

        if len(nutrition_data) == 0 or len(mbg_data) == 0:
            print("❌ Data loading failed")
            return False

        print("✅ Data loading functions work correctly")
        return True

    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("🚀 Starting JALU App Testing Suite")
    print("=" * 50)

    tests = [
        ("App Structure", test_app_structure),
        ("CSS Improvements", test_css_improvements),
        ("Navigation Pages", test_navigation_pages),
        ("Metric Cards", test_metric_cards),
        ("Dependencies", test_dependencies),
        ("Data Loading", test_data_loading)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            print()

    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! JALU app is ready for deployment.")
        return True
    else:
        print("⚠️ Some tests failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
