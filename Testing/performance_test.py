#!/usr/bin/env python3
"""
Performance Testing Suite - LLM Premier League
Compara rendimiento entre modo Claude AI (ON) vs modo Local (OFF)
"""

import requests
import time
import json
import statistics
from datetime import datetime
from typing import Dict, List, Tuple
import os
import sys

# Configuración
API_BASE_URL = "http://localhost:8080/api"
TEST_ITERATIONS = 5  # Número de iteraciones por test
TIMEOUT = 60  # Timeout en segundos

# Test cases predefinidos
PREDICTION_TESTS = [
    {"home_team": "Liverpool", "away_team": "Chelsea"},
    {"home_team": "Arsenal", "away_team": "Man City"},
    {"home_team": "Man United", "away_team": "Tottenham"},
    {"home_team": "Newcastle", "away_team": "Aston Villa"},
    {"home_team": "Brighton", "away_team": "West Ham"}
]

ANALYSIS_TESTS = [
    {"team": "Liverpool"},
    {"team": "Chelsea"}, 
    {"team": "Arsenal"},
    {"team": "Man City"},
    {"team": "Man United"}
]

CHAT_TESTS = [
    {"message": "¿Quién será el máximo goleador esta temporada?"},
    {"message": "¿Cómo va el Arsenal esta temporada?"},
    {"message": "¿Quién ganaría entre Liverpool y Chelsea?"},
    {"message": "¿Cuáles son los favoritos al título?"},
    {"message": "¿Qué tal los fichajes del Manchester United?"}
]

class PerformanceTester:
    def __init__(self):
        self.results = {
            'claude_ai_on': {},
            'claude_ai_off': {},
            'timestamp': datetime.now().isoformat(),
            'test_config': {
                'iterations': TEST_ITERATIONS,
                'timeout': TIMEOUT,
                'base_url': API_BASE_URL
            }
        }
    
    def check_server_status(self) -> bool:
        """Verificar que el servidor esté funcionando"""
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def toggle_ai_mode(self, enable: bool) -> bool:
        """Cambiar el modo AI del sistema"""
        try:
            payload = {"use_claude_ai": enable}
            response = requests.post(
                f"{API_BASE_URL}/toggle-ai", 
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Modo cambiado a: {'Claude AI' if enable else 'Local'}")
                return data.get('current_mode') == enable
            else:
                print(f"❌ Error cambiando modo: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error en toggle: {e}")
            return False
    
    def measure_endpoint_performance(self, endpoint: str, method: str, payload: Dict = None) -> Dict:
        """Medir rendimiento de un endpoint específico"""
        times = []
        success_count = 0
        responses = []
        
        for i in range(TEST_ITERATIONS):
            try:
                start_time = time.time()
                
                if method == 'GET':
                    response = requests.get(f"{API_BASE_URL}/{endpoint}", timeout=TIMEOUT)
                elif method == 'POST':
                    response = requests.post(f"{API_BASE_URL}/{endpoint}", json=payload, timeout=TIMEOUT)
                
                end_time = time.time()
                
                if response.status_code == 200:
                    success_count += 1
                    response_time = end_time - start_time
                    times.append(response_time)
                    responses.append(response.json())
                    print(f"  ✅ Iteración {i+1}: {response_time:.3f}s")
                else:
                    print(f"  ❌ Iteración {i+1}: Error {response.status_code}")
                    
            except requests.Timeout:
                print(f"  ⏱️ Iteración {i+1}: Timeout ({TIMEOUT}s)")
            except Exception as e:
                print(f"  ❌ Iteración {i+1}: Error - {e}")
        
        if times:
            return {
                'success_rate': success_count / TEST_ITERATIONS,
                'avg_time': statistics.mean(times),
                'min_time': min(times),
                'max_time': max(times),
                'median_time': statistics.median(times),
                'std_dev': statistics.stdev(times) if len(times) > 1 else 0,
                'total_tests': TEST_ITERATIONS,
                'successful_tests': success_count,
                'sample_responses': responses[:2]  # Primeras 2 respuestas como muestra
            }
        else:
            return {
                'success_rate': 0,
                'avg_time': 0,
                'min_time': 0,
                'max_time': 0,
                'median_time': 0,
                'std_dev': 0,
                'total_tests': TEST_ITERATIONS,
                'successful_tests': 0,
                'sample_responses': []
            }
    
    def test_predictions(self) -> Dict:
        """Test de predicciones de partidos"""
        print("📊 Testing Predictions...")
        results = {}
        
        for i, test_case in enumerate(PREDICTION_TESTS):
            print(f"  🏈 Test {i+1}: {test_case['home_team']} vs {test_case['away_team']}")
            results[f"prediction_{i+1}"] = self.measure_endpoint_performance(
                "predict", "POST", test_case
            )
        
        return results
    
    def test_analysis(self) -> Dict:
        """Test de análisis de equipos"""
        print("📋 Testing Team Analysis...")
        results = {}
        
        for i, test_case in enumerate(ANALYSIS_TESTS):
            print(f"  🏀 Test {i+1}: {test_case['team']}")
            results[f"analysis_{i+1}"] = self.measure_endpoint_performance(
                "analyze", "POST", test_case
            )
        
        return results
    
    def test_chat(self) -> Dict:
        """Test de chat conversacional"""
        print("💬 Testing Chat...")
        results = {}
        
        for i, test_case in enumerate(CHAT_TESTS):
            print(f"  💭 Test {i+1}: {test_case['message'][:50]}...")
            results[f"chat_{i+1}"] = self.measure_endpoint_performance(
                "chat", "POST", test_case
            )
        
        return results
    
    def test_basic_endpoints(self) -> Dict:
        """Test de endpoints básicos"""
        print("🔧 Testing Basic Endpoints...")
        results = {}
        
        endpoints = [
            ("health", "GET"),
            ("teams", "GET"),
            ("stats", "GET"),
            ("system", "GET")
        ]
        
        for endpoint, method in endpoints:
            print(f"  🌐 Testing /{endpoint}")
            results[endpoint] = self.measure_endpoint_performance(endpoint, method)
        
        return results
    
    def run_full_test_suite(self, mode: str):
        """Ejecutar suite completa de tests"""
        print(f"\n🚀 Ejecutando tests en modo: {mode}")
        print("=" * 60)
        
        mode_results = {}
        
        # Tests básicos (más rápidos)
        mode_results['basic'] = self.test_basic_endpoints()
        
        # Tests de predicciones
        mode_results['predictions'] = self.test_predictions()
        
        # Tests de análisis
        mode_results['analysis'] = self.test_analysis()
        
        # Tests de chat
        mode_results['chat'] = self.test_chat()
        
        return mode_results
    
    def calculate_summary_stats(self, mode_results: Dict) -> Dict:
        """Calcular estadísticas resumidas"""
        all_times = []
        all_success_rates = []
        
        for category in mode_results.values():
            for test_result in category.values():
                if test_result['success_rate'] > 0:
                    all_times.append(test_result['avg_time'])
                all_success_rates.append(test_result['success_rate'])
        
        if all_times:
            return {
                'overall_avg_time': statistics.mean(all_times),
                'overall_success_rate': statistics.mean(all_success_rates),
                'fastest_response': min(all_times),
                'slowest_response': max(all_times),
                'total_tests_run': sum(len(cat) * TEST_ITERATIONS for cat in mode_results.values())
            }
        else:
            return {
                'overall_avg_time': 0,
                'overall_success_rate': 0,
                'fastest_response': 0,
                'slowest_response': 0,
                'total_tests_run': 0
            }
    
    def run_comparative_tests(self):
        """Ejecutar tests comparativos completos"""
        print("🏆 LLM PREMIER LEAGUE - PERFORMANCE TESTING SUITE")
        print("=" * 80)
        
        if not self.check_server_status():
            print("❌ ERROR: Servidor no disponible en", API_BASE_URL)
            return False
        
        print("✅ Servidor conectado correctamente")
        
        # Test 1: Modo Claude AI OFF (Local)
        print("\n" + "="*80)
        print("🔄 FASE 1: Testing modo LOCAL (AI OFF)")
        print("="*80)
        
        if self.toggle_ai_mode(False):
            time.sleep(2)  # Esperar a que el cambio se propague
            self.results['claude_ai_off'] = self.run_full_test_suite("LOCAL")
            self.results['claude_ai_off']['summary'] = self.calculate_summary_stats(
                self.results['claude_ai_off']
            )
        else:
            print("❌ No se pudo cambiar al modo LOCAL")
            return False
        
        # Test 2: Modo Claude AI ON  
        print("\n" + "="*80)
        print("🔄 FASE 2: Testing modo CLAUDE AI (AI ON)")
        print("="*80)
        
        if self.toggle_ai_mode(True):
            time.sleep(2)  # Esperar a que el cambio se propague
            self.results['claude_ai_on'] = self.run_full_test_suite("CLAUDE AI")
            self.results['claude_ai_on']['summary'] = self.calculate_summary_stats(
                self.results['claude_ai_on']
            )
        else:
            print("❌ No se pudo cambiar al modo CLAUDE AI")
            return False
        
        return True
    
    def save_results(self, filename: str = None):
        """Guardar resultados en archivo JSON"""
        if not filename:
            filename = f"performance_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join('/Users/rios/Desktop/LLM-PREMIER/testing', filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Resultados guardados en: {filepath}")
        return filepath

def main():
    """Función principal"""
    print("Iniciando tests de rendimiento...")
    
    tester = PerformanceTester()
    
    if tester.run_comparative_tests():
        results_file = tester.save_results()
        
        print("\n" + "="*80)
        print("🎯 RESUMEN DE RESULTADOS")
        print("="*80)
        
        # Resumen rápido
        local_summary = tester.results['claude_ai_off']['summary']
        ai_summary = tester.results['claude_ai_on']['summary']
        
        print(f"📊 MODO LOCAL:")
        print(f"   • Tiempo promedio: {local_summary['overall_avg_time']:.3f}s")
        print(f"   • Éxito promedio: {local_summary['overall_success_rate']:.1%}")
        print(f"   • Respuesta más rápida: {local_summary['fastest_response']:.3f}s")
        print(f"   • Respuesta más lenta: {local_summary['slowest_response']:.3f}s")
        
        print(f"\n🤖 MODO CLAUDE AI:")
        print(f"   • Tiempo promedio: {ai_summary['overall_avg_time']:.3f}s")
        print(f"   • Éxito promedio: {ai_summary['overall_success_rate']:.1%}")
        print(f"   • Respuesta más rápida: {ai_summary['fastest_response']:.3f}s")
        print(f"   • Respuesta más lenta: {ai_summary['slowest_response']:.3f}s")
        
        # Comparación
        time_diff = ai_summary['overall_avg_time'] - local_summary['overall_avg_time']
        time_ratio = ai_summary['overall_avg_time'] / local_summary['overall_avg_time'] if local_summary['overall_avg_time'] > 0 else 0
        
        print(f"\n⚖️ COMPARACIÓN:")
        print(f"   • Claude AI es {time_diff:+.3f}s {'más lento' if time_diff > 0 else 'más rápido'}")
        print(f"   • Ratio: Claude AI es {time_ratio:.1f}x el tiempo del modo local")
        
        print(f"\n📄 Ver reporte completo ejecutando:")
        print(f"   python testing/generate_report.py {results_file}")
        
        return True
    else:
        print("❌ Error ejecutando tests")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
