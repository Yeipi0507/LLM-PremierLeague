#!/usr/bin/env python3
"""
Budget-Friendly Test Suite - LLM Premier League
Tests económicos que no consumen todos tus tokens 💸
"""

import subprocess
import sys
import time
from datetime import datetime

class BudgetTester:
    def __init__(self):
        self.tests = {
            'detailed_performance': {
                'script': 'quick_test.py',
                'duration': '6-8 min',
                'description': 'Test detallado de rendimiento con comparación ON/OFF',
                'cost': '~12 requests'
            },
            'detailed_quality': {
                'script': 'mini_quality_test.py', 
                'duration': '4-5 min',
                'description': 'Análisis detallado de calidad de respuestas',
                'cost': '~4 requests'
            }
        }
        
        self.results = {}
    
    def run_budget_test(self, test_name):
        """Ejecutar un test económico"""
        test_info = self.tests[test_name]
        
        print(f"\n🚀 EJECUTANDO: {test_info['description']}")
        print(f"⏱️  Duración: {test_info['duration']}")
        print(f"💰 Costo: {test_info['cost']}")
        print("-" * 50)
        
        try:
            result = subprocess.run([
                sys.executable, test_info['script']
            ], capture_output=True, text=True, timeout=600)  # 10 min max
            
            if result.returncode == 0:
                print(f"✅ {test_name.upper()} completado!")
                return True
            else:
                print(f"❌ Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Excepción: {e}")
            return False
    
    def run_budget_suite(self):
        """Suite económica completa"""
        print("💸 LLM PREMIER LEAGUE - DETAILED BUDGET TESTING SUITE")
        print("=" * 70)
        print("🎯 Objetivo: Análisis detallado con consumo moderado")
        print("⏱️  Duración total: ~12 minutos")
        print("💰 Costo total: ~16 requests (vs 200+ de la suite completa)")
        print("🔍 Comparaciones precisas: Toggle ON vs OFF con métricas detalladas")
        
        success_count = 0
        start_time = time.time()
        
        for test_name in self.tests.keys():
            if self.run_budget_test(test_name):
                success_count += 1
            
            # Pausa corta entre tests
            if test_name != list(self.tests.keys())[-1]:
                time.sleep(5)
        
        total_time = time.time() - start_time
        
        print("\n" + "=" * 70)
        print("🏆 RESUMEN DETAILED BUDGET SUITE")
        print("=" * 70)
        print(f"✅ Tests exitosos: {success_count}/{len(self.tests)}")
        print(f"⏱️  Tiempo real: {total_time/60:.1f} minutos")
        print(f"💰 Tokens eficientes: ~92% ahorro vs suite completa")
        print(f"🔍 Análisis detallado: Comparaciones ON/OFF con métricas precisas")
        
        if success_count == len(self.tests):
            print(f"\n🎉 ¡Suite detallada completada exitosamente!")
            print(f"📊 Tienes análisis completo para decisiones informadas")
            print(f"⚖️  Balance perfecto: detalle profesional + costo moderado")
            print(f"🎯 Comparación completa toggle ON vs OFF disponible")
        else:
            print(f"\n⚠️  Algunos tests fallaron, pero tienes datos útiles")
            print(f"🔧 Revisa los logs individuales para más detalles")
        
        return success_count == len(self.tests)

def main():
    print("💡 DETAILED BUDGET SUITE: Análisis profesional con costo moderado")
    print("🎯 Comparaciones detalladas ON vs OFF con métricas específicas")
    print("⚖️  Balance perfecto entre insight y eficiencia")
    print()
    
    tester = BudgetTester()
    tester.run_budget_suite()

if __name__ == "__main__":
    main()
